import streamlit as st
import os
import time
from modules.pdf_loader import extract_text_from_pdf
from modules.vector_store import create_vector_store
from modules.rag_chain import get_qa_chain
from dotenv import load_dotenv
load_dotenv()

# Check API Key
if "GOOGLE_API_KEY" not in os.environ:
    st.error("⚠ GOOGLE_API_KEY is not set in the environment variables!")
    st.info("Please set your Google API key in the .env file or directly in your environment.")
    st.stop()

st.set_page_config(page_title="PDF Q&A Bot", layout="centered")
st.title("📄 Ask Questions About Your PDF")

# Sidebar controls
debug_mode = st.sidebar.checkbox("Debug Mode", value=False)
custom_prompt = st.sidebar.text_area(
    "Custom Prompt Template",
    value="""You are a helpful assistant. Answer the question based on the following document context.\n\nContext:\n{context}\n\nQuestion: {question}""",
    height=200
)

# Session state
if "chain" not in st.session_state:
    st.session_state.chain = None
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = None

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    st.success("PDF uploaded successfully.")
    with st.spinner("Reading PDF and creating knowledge base..."):
        try:
            text = extract_text_from_pdf(uploaded_file)
            st.session_state.pdf_text = text

            if debug_mode:
                st.write(f"Extracted {len(text)} characters of text")

            vector_store = create_vector_store(text)
            if debug_mode:
                st.write("Vector store created successfully")

            try:
                chain = get_qa_chain(vector_store)
                st.session_state.chain = chain
                if debug_mode:
                    st.write("Chain created successfully")
            except Exception as e:
                st.error(f"Error creating RAG chain: {str(e)}")
                if debug_mode:
                    st.exception(e)
                st.stop()

        except Exception as e:
            st.error(f"Error processing PDF: {str(e)}")
            if debug_mode:
                st.exception(e)
            st.stop()

    st.success("Ready to answer your questions!")

# Ask questions
if "chain" in st.session_state and st.session_state.chain:
    question = st.text_input("Ask a question about the PDF:")

    if question:
        with st.spinner("Thinking..."):
            try:
                start_time = time.time()
                response = None

                # Pass question in structured input
                try:
                    response = st.session_state.chain.invoke({"query": question})
                except Exception as e:
                    st.error(f"Error generating response: {str(e)}")
                    if debug_mode:
                        st.exception(e)
                    st.stop()

                end_time = time.time()
                if debug_mode:
                    st.write(f"Response time: {end_time - start_time:.2f} seconds")

                if response:
                    result = response.get("result", response)
                    st.markdown(f"Answer: {result}")
                else:
                    st.error("No response returned.")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                if debug_mode:
                    st.exception(e)

    # Debug output
    if debug_mode:
        st.subheader("Debug Information")
        if st.session_state.pdf_text:
            with st.expander("Show PDF Text Sample"):
                st.text(st.session_state.pdf_text[:1000] + "...")