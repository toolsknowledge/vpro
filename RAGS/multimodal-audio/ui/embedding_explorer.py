"""Embedding Explorer: see the real vectors stored in ChromaDB and a 2D PCA map of them."""

from __future__ import annotations

import html

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from backend.openai_client import OpenAIServiceError
from backend.vector_store import IncompatibleEmbeddingError
from ui.components import page_header, vector_preview


def _explain() -> None:
    st.markdown(
        """
**What is an embedding?** A list of numbers (a *vector*) that represents the **meaning** of a piece of text.
The embedding model reads a chunk and outputs, for `text-embedding-3-small`, 1,536 numbers.
Chunks about similar topics get vectors that point in similar directions, even when they use different words
("fee" vs "cost").

**Why store vectors?** To answer a question, the app embeds the question too, then asks ChromaDB for the stored
vectors closest to it. Pre-computing and storing chunk vectors once means each question needs only **one**
new embedding call instead of re-embedding every document.
"""
    )


def render(services) -> None:
    page_header("Embedding Explorer", "Look inside the vectors that represent your chunks.", "🔢")
    _explain()

    records = services.store.get_records(include_embeddings=True)
    records = [r for r in records if r.embedding]
    if not records:
        st.info("ChromaDB has no vectors yet. Index a document first.")
        return

    model = records[0].metadata.get("embedding_model", services.store.stored_embedding_model or "?")
    c1, c2, c3 = st.columns(3)
    c1.metric("Stored vectors", f"{len(records):,}")
    c2.metric("Dimension", len(records[0].embedding))
    c3.metric("Embedding model", model)

    # ------------------------------------------------------- single vector
    st.subheader("Inspect one chunk's vector")
    files = sorted({r.metadata.get("source_file", "?") for r in records})
    file_choice = st.selectbox("Document", files)
    doc_records = sorted(
        (r for r in records if r.metadata.get("source_file") == file_choice),
        key=lambda r: r.metadata.get("chunk_index", 0),
    )
    idx = st.number_input("Chunk index", 0, len(doc_records) - 1, 0) if len(doc_records) > 1 else 0
    record = doc_records[int(idx)]
    vector = np.array(record.embedding)

    st.markdown(f'<div class="vp-chunk">{html.escape(record.text[:1500])}{"…" if len(record.text) > 1500 else ""}</div>', unsafe_allow_html=True)
    st.caption(f"Chunk ID `{record.chunk_id}`")
    v1, v2, v3 = st.columns(3)
    v1.metric("Vector length (dimensions)", len(vector))
    v2.metric("L2 norm", f"{np.linalg.norm(vector):.4f}", help="OpenAI embeddings are normalised to length ≈ 1.")
    v3.metric("Min / max value", f"{vector.min():+.3f} / {vector.max():+.3f}")
    st.markdown("**First 10 values:**")
    st.code(vector_preview(record.embedding, 10))
    if st.toggle("Show the complete vector"):
        st.dataframe(pd.DataFrame({"dimension": range(len(vector)), "value": vector}), hide_index=True, height=300)

    # ---------------------------------------------------------- PCA plot
    st.subheader("2D map of all chunks (PCA)")
    st.caption(
        "⚠️ This squeezes 1,536 dimensions into 2 with Principal Component Analysis, purely as a picture. "
        "Distances on this chart are only a rough hint; retrieval uses the full vectors."
    )
    if len(records) < 3:
        st.info("At least 3 stored chunks are needed for a meaningful 2D projection.")
        return

    from sklearn.decomposition import PCA

    matrix = np.array([r.embedding for r in records])
    pca = PCA(n_components=2, random_state=0)
    points = pca.fit_transform(matrix)
    frame = pd.DataFrame(
        {
            "x": points[:, 0],
            "y": points[:, 1],
            "source": [r.metadata.get("source_file", "?") for r in records],
            "chunk_id": [r.chunk_id for r in records],
            "preview": [r.text[:90].replace("\n", " ") for r in records],
            "kind": "chunk",
        }
    )

    question = st.text_input("Optional: place a question on the map", placeholder="What is the course fee?")
    if question.strip():
        if services.embedder is None:
            st.warning("OpenAI is not configured, so the question cannot be embedded.")
        else:
            try:
                services.store.check_compatible(services.embedder.model)
                q_point = pca.transform(np.array([services.embedder.embed_query(question)]))[0]
                frame.loc[len(frame)] = [q_point[0], q_point[1], "❓ your question", "question", question[:90], "question"]
            except (OpenAIServiceError, IncompatibleEmbeddingError, ValueError) as exc:
                st.error(str(exc))

    fig = px.scatter(
        frame, x="x", y="y", color="source", symbol="kind", hover_data={"chunk_id": True, "preview": True, "x": False, "y": False},
        labels={"x": "PCA component 1", "y": "PCA component 2"}, height=520,
    )
    fig.update_traces(marker=dict(size=11, line=dict(width=1, color="white")))
    st.plotly_chart(fig, width="stretch")
    explained = pca.explained_variance_ratio_.sum()
    st.caption(f"These two components capture {explained:.1%} of the variance in the full vectors; the rest is not shown.")
