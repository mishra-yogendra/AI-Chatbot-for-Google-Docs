import streamlit as st

from services.google_doc_loader import load_google_doc
from services.text_chunker import chunk_text
from services.retriever import retrieve_docs_with_scores
from services.llm import generate_answer
from config import TOP_K
from services.vector_store import create_vector_store
st.set_page_config(page_title="Google Doc RAG Chatbot", layout="centered")

st.title("📄 AI Chatbot for Google Docs")

# ---------- Session State ----------
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------- Document Ingestion ----------
doc_url = st.text_input("🔗 Enter public Google Doc URL")

if st.button("Ingest Document"):
    with st.spinner("Ingesting document..."):
        text = load_google_doc(doc_url)
        chunks = chunk_text(text)
        st.session_state.vector_store = create_vector_store(chunks)
        st.session_state.chat_history = []
    st.success("Document ingested successfully!")

st.divider()

# ---------- Chat ----------
query = st.text_input("💬 Ask a question")

if st.button("Ask"):
    if not st.session_state.vector_store:
        st.warning("Please ingest a document first.")
    else:
        with st.spinner("Thinking..."):
            docs_with_scores = retrieve_docs_with_scores(
                st.session_state.vector_store,
                query,
                TOP_K
            )

            docs = [d[0] for d in docs_with_scores]
            scores = [d[1] for d in docs_with_scores]

            answer = generate_answer(
                docs,
                query,
                st.session_state.chat_history
            )

            st.session_state.chat_history.append({
                "user": query,
                "assistant": answer
            })

        # ---------- Confidence ----------
        avg_score = sum(scores) / len(scores)
        confidence = max(0, min(100, int((1 - avg_score) * 100)))

        # ---------- UI ----------
        st.markdown("### ✅ Answer")
        st.write(answer)

        st.markdown("### 📊 Confidence")
        st.progress(confidence)
        st.write(f"**Confidence Score:** {confidence}%")

        st.markdown("### 📚 Sources Used")
        for i, doc in enumerate(docs):
            st.markdown(f"**Section {i+1}:**")
            st.caption(doc.page_content[:300] + "...")
