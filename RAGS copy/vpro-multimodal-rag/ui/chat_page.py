from __future__ import annotations

import streamlit as st

from backend.errors import AppError
from backend.rag_chain import RagChain
from backend.retrieval import Retriever
from backend.embeddings import get_client
from ui.common import Services, cfg, get_embedder, hero, setup_banner, show_error, store_ready


def _render_answer(msg: dict) -> None:
    st.markdown(msg["text"])
    if msg.get("not_found"):
        st.caption("No supporting passage was found, so no sources are cited.")
    if msg["cited"]:
        st.markdown("**Sources**")
        for c in msg["cited"]:
            sim = f" · similarity {c['similarity']:.3f}" if c["similarity"] is not None else ""
            with st.expander(f"[{c['rank']}] {c['citation']}{sim}"):
                st.code(c["text"], language=None, wrap_lines=True)
    elif msg["retrieved"] and not msg.get("not_found"):
        st.caption("The answer did not cite specific passages; inspect the retrieved chunks below.")
    if msg["retrieved"]:
        with st.expander(f"Retrieved chunks ({len(msg['retrieved'])})"):
            for c in msg["retrieved"]:
                sim = f"{c['similarity']:.3f}" if c["similarity"] is not None else "n/a"
                st.markdown(f"**[{c['rank']}]** `{c['chunk_id']}` · {c['citation']} · similarity {sim} (distance {c['distance']:.3f})")
                st.code(c["text"][:1500], language=None, wrap_lines=True)


def render(svc: Services) -> None:
    hero("Ask Your Documents", "Answers are grounded in retrieved chunks and cite their sources.")
    can_use_api = setup_banner(svc)
    ready = store_ready(svc)
    c = cfg()
    docs = svc.registry.all()
    with st.expander("Retrieval options"):
        a, b = st.columns(2)
        c["top_k"] = int(a.number_input("Top K chunks", 1, 30, c["top_k"]))
        use_t = b.checkbox("Apply a similarity threshold", value=c["threshold"] is not None)
        c["threshold"] = b.slider("Minimum cosine similarity", 0.0, 1.0, c["threshold"] or 0.2, 0.05) if use_t else None
        only = st.multiselect("Limit to files", [d["filename"] for d in docs])
    if "chat" not in st.session_state:
        st.session_state.chat = []
    if st.button("🧹 Clear chat"):
        st.session_state.chat = []
    st.caption("Each question is answered on its own (earlier turns are not sent to the model), so make follow-up questions self-contained.")

    for m in st.session_state.chat:
        with st.chat_message(m["role"]):
            st.markdown(m["text"]) if m["role"] == "user" else _render_answer(m)

    question = st.chat_input("Ask a question about your documents…", disabled=not (can_use_api and ready))
    if question is None:
        return
    if not question.strip():
        st.warning("Please type a question.")
        return
    if svc.store.count() == 0:
        st.warning("Nothing is indexed yet. Upload and index a document first.")
        return
    st.session_state.chat.append({"role": "user", "text": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        try:
            with st.spinner("Searching your documents and writing an answer…"):
                embedder = get_embedder(svc)
                result = Retriever(svc.store, embedder).retrieve(question, c["top_k"], c["threshold"], only or None)
                ans = RagChain(get_client(svc.settings), svc.settings.chat_model).answer(question, result)
            pack = lambda h: {"rank": h.rank, "chunk_id": h.chunk_id, "text": h.text, "citation": h.citation,
                              "similarity": h.similarity, "distance": h.distance}
            msg = {"role": "assistant", "text": ans.text, "not_found": ans.not_found,
                   "cited": [pack(h) for h in ans.cited], "retrieved": [pack(h) for h in result.hits]}
            _render_answer(msg)
            st.session_state.chat.append(msg)
        except AppError as exc:
            show_error(exc)
        except Exception as exc:
            show_error(exc)
