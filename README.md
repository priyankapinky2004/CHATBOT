# 📚 PDF Question-Answering Chatbot

A smart chatbot that allows users to upload PDF files and ask questions related to the content. It reads, understands, and responds to queries using Natural Language Processing and context-aware search.

## 🚀 Features

- 📄 Upload any PDF file
- 🤖 Ask questions based on the PDF content
- 🔍 Contextual search and intelligent answers
- ⚡ Fast, interactive, and user-friendly interface
- 💬 Chat-based UI for seamless experience

## 🛠️ Tech Stack

- **Frontend**: Python
- **Backend**: Python (Flask / FastAPI)
- **PDF Parsing**: PyMuPDF / pdfplumber
- **NLP Engine**: OpenAI GPT / LangChain / HuggingFace Transformers
- **Vector Database**: FAISS / Chroma / Pinecone (optional)
- **Deployment**: Streamlit / Gradio / Flask app / Render / HuggingFace Spaces

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/priyankapinky2004/CHATBOT.git
cd pdf-chatbot

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
