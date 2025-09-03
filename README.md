# 📧 AI-Powered Cold Email Generator with ChromaDB & Groq

An AI-powered tool that generates **personalized cold emails for job applications**.  
It uses:  
- **LangChain** for LLM workflow  
- **Groq API** (LLaMA models) for natural language generation  
- **ChromaDB** for semantic search over your portfolio/resume  
- **Streamlit** for an interactive UI  

---

## 🚀 Features
- ✅ Upload your **resume (PDF)** and store embeddings in ChromaDB  
- ✅ Paste a **job description** to get a tailored cold email  
- ✅ Uses **Groq LLaMA models** for fast, optimized text generation  
- ✅ Deployable on **Hugging Face Spaces** or run locally  

---

## 📂 Project Structure
Cold-email-gen/
│── app.py # Main Streamlit app
│── chroma_setup.py # Script to process resume & create ChromaDB
│── requirements.txt # Dependencies
│── README.md # Documentation
