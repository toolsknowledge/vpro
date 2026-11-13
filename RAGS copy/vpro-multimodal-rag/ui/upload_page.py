from __future__ import annotations

import time

import pandas as pd
import streamlit as st

from backend.document_loader import validate_upload
from backend.errors import AppError
from backend.indexer import index_file
from config.settings import SUPPORTED_EXTENSIONS
from ui.common import (Services, cards, cfg, get_embedder, hero, pipeline_html, setup_banner, show_error,
                       store_ready)

ICON = {"indexed": "✅", "reindexed": "🔁", "skipped_duplicate": "⏭️", "failed": "❌"}


def render(svc: Services) -> None:
    hero("Upload Documents", "PDF · Word · Excel · TXT  -  drag, drop, index.")
    can_use_api = setup_banner(svc)
    store_ready(svc)
    c = cfg()

    st.info("🔒 **Privacy:** when you index, the text of your documents is sent to OpenAI to create embeddings. "
            "Questions and retrieved passages are also sent to OpenAI to generate answers.")
    with st.expander("Chunking settings", expanded=False):
        a, b = st.columns(2)
        c["chunk_size"] = int(a.number_input("Chunk size (tokens)", 50, 8000, c["chunk_size"], 50))
        c["chunk_overlap"] = int(b.number_input("Chunk overlap (tokens)", 0, 4000, c["chunk_overlap"], 10))
        if c["chunk_overlap"] >= c["chunk_size"]:
            st.error("Overlap must be smaller than chunk size.")

    files = st.file_uploader(f"Drop files here ({', '.join(SUPPORTED_EXTENSIONS)}; max {svc.settings.max_upload_mb} MB each)",
                             type=[e.lstrip(".") for e in SUPPORTED_EXTENSIONS], accept_multiple_files=True)
    samples = sorted(p.name for p in svc.settings.sample_dir.glob("*") if p.suffix.lower() in SUPPORTED_EXTENSIONS) \
        if svc.settings.sample_dir.exists() else []
    picked = st.multiselect("…or pick bundled sample files", samples, help="Files from the sample_files/ folder")
    force = st.checkbox("Re-index files that are already indexed (same content)", value=False)

    queue: list[tuple[str, bytes]] = [(f.name, f.getvalue()) for f in files or []]
    queue += [(n, (svc.settings.sample_dir / n).read_bytes()) for n in picked]

    ready = []
    if queue:
        rows = []
        for name, data in queue:
            try:
                validate_upload(name, data, svc.settings.max_upload_bytes)
                rows.append({"File": name, "Size (KB)": round(len(data) / 1024, 1), "Check": "✅ OK"})
                ready.append((name, data))
            except AppError as exc:
                rows.append({"File": name, "Size (KB)": round(len(data) / 1024, 1), "Check": f"❌ {exc}"})
        st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)

    if st.button("🚀 Start indexing", type="primary", disabled=not ready or not can_use_api):
        _run(svc, ready, force)
    _summary(svc)


def _run(svc: Services, files: list[tuple[str, bytes]], force: bool) -> None:
    c = cfg()
    try:
        embedder = get_embedder(svc)
    except AppError as exc:
        show_error(exc)
        return
    bar, status = st.progress(0.0), st.empty()
    results, t0 = [], time.perf_counter()
    for i, (name, data) in enumerate(files):
        def progress(stage: str, frac: float, i=i, name=name):
            bar.progress(min((i + frac) / len(files), 1.0))
            status.write(f"**{name}** → {stage}")
        results.append(index_file(name, data, settings=svc.settings, registry=svc.registry, store=svc.store,
                                  embedder=embedder, chunk_size=c["chunk_size"], chunk_overlap=c["chunk_overlap"],
                                  force=force, progress=progress))
    bar.progress(1.0)
    status.empty()
    st.session_state["last_run"] = {"results": [r.to_dict() for r in results],
                                    "seconds": round(time.perf_counter() - t0, 2),
                                    "records": svc.store.count(), "model": embedder.model,
                                    "retries": embedder.retries, "retry_log": embedder.retry_log}


def _summary(svc: Services) -> None:
    run = st.session_state.get("last_run")
    if not run:
        return
    res = run["results"]
    ok = [r for r in res if r["status"] in ("indexed", "reindexed")]
    st.subheader("Indexing summary")
    cards([("Files uploaded", len(res)), ("Pages / sheets / sections", sum(r["units"] for r in ok)),
           ("Chunks created", sum(r["chunks"] for r in ok)), ("Embeddings generated", sum(r["embeddings"] for r in ok)),
           ("Vector dimensions", max([r["dimension"] for r in ok], default=0) or "—")])
    st.write("")
    cards([("Records in ChromaDB", run["records"]), ("Processing time", f"{run['seconds']} s"),
           ("Succeeded", len(ok)), ("Skipped (duplicates)", sum(r["status"] == "skipped_duplicate" for r in res)),
           ("Failed", sum(r["status"] == "failed" for r in res))])
    if run.get("retries"):
        st.warning(f"{run['retries']} transient API error(s) were retried: " + "; ".join(run["retry_log"][-3:]))
    st.write("")
    for r in res:
        label = f"{ICON.get(r['status'], '•')} {r['filename']} - {r['status'].replace('_', ' ')}"
        with st.expander(label, expanded=r["status"] == "failed"):
            if r["status"] == "failed":
                st.error(r["message"])
            else:
                st.write(r["message"])
                st.markdown(pipeline_html({"Extract": f"{r['units']} {r['unit_label']}", "Clean": f"{r['sections']} sections",
                                           "Chunk": f"{r['chunks']} chunks", "Embed": f"{r['embeddings']} × {r['dimension']}d",
                                           "Store": f"{r['stored']} records"} if r["embeddings"] else {}),
                            unsafe_allow_html=True)
                st.caption(f"Time: {r['seconds']} s · Open **Indexing Pipeline** to inspect the extracted text and chunks.")
