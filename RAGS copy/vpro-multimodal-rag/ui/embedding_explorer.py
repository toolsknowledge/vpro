from __future__ import annotations

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from ui.common import Services, fmt_location, hero


def render(svc: Services) -> None:
    hero("Embedding Explorer", "What is an embedding, and what does ours look like?")
    st.markdown(
        "An **embedding** is a long list of numbers that represents the *meaning* of a piece of text. Text with similar meaning gets "
        "similar numbers, so the computer can find related text by comparing lists of numbers instead of matching words. "
        "We **store the vectors in ChromaDB** so we only pay to embed each chunk once and can search them quickly later.")
    problem = svc.store.compatibility_problem()
    if problem:
        st.error(problem)
        return
    n = svc.store.count()
    if n == 0:
        st.info("No embeddings stored yet.")
        return
    recs = svc.store.get_records(limit=1000)
    labels = {f"{r['metadata']['source_file']} · #{r['metadata']['chunk_index']} · {fmt_location(r['metadata'])}": r["id"] for r in recs}
    cid = labels[st.selectbox("Choose a chunk", list(labels))]
    rec = svc.store.get_records(where={"chunk_id": cid}, include_embeddings=True)[0]
    vec = np.array(rec["embedding"])
    st.markdown("**Chunk text**")
    st.code(rec["document"], language=None, wrap_lines=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Embedding model", svc.store.stored_model or svc.settings.embedding_model)
    c2.metric("Vector dimension", len(vec))
    c3.metric("Vector length (L2 norm)", f"{np.linalg.norm(vec):.4f}")
    st.markdown("**First 10 values**")
    st.dataframe(pd.DataFrame({"dimension": range(10), "value": vec[:10]}), width="stretch", hide_index=True)
    key = f"full_vec_{cid}"
    if st.button("Inspect the complete vector"):
        st.session_state[key] = not st.session_state.get(key, False)
    if st.session_state.get(key):
        st.dataframe(pd.DataFrame({"dimension": range(len(vec)), "value": vec}), width="stretch", height=300, hide_index=True)

    st.subheader("2-D map of stored chunks (PCA)")
    st.caption("⚠️ PCA squeezes hundreds of dimensions into 2. It is only a **visualisation**: distances on this map are approximate and do not "
               "represent the full embedding space.")
    if n < 3:
        st.info("Index at least 3 chunks to draw the map.")
        return
    from sklearn.decomposition import PCA
    cap = 400
    pts = svc.store.get_records(limit=cap, include_embeddings=True)
    X = np.array([p["embedding"] for p in pts])
    pca = PCA(n_components=2).fit(X)
    xy = pca.transform(X)
    df = pd.DataFrame({"x": xy[:, 0], "y": xy[:, 1], "chunk": [p["id"] for p in pts],
                       "source": [p["metadata"]["source_file"] for p in pts],
                       "preview": [p["document"][:80].replace("\n", " ") for p in pts]})
    show_ids = st.checkbox("Print chunk IDs next to points", value=False)
    base = alt.Chart(df).encode(x="x:Q", y="y:Q")
    layers = base.mark_circle(size=90, opacity=0.8).encode(color="source:N", tooltip=["chunk", "source", "preview"])
    if show_ids:
        layers = layers + base.mark_text(dx=8, dy=-6, fontSize=9).encode(text="chunk:N")
    st.altair_chart(layers.interactive(), width="stretch")
    st.caption(f"{len(pts)} of {n} chunks plotted · the two axes explain {pca.explained_variance_ratio_.sum() * 100:.1f}% of the variance.")
