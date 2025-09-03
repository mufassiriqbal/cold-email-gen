import os
import streamlit as st
import chromadb
from chromadb.utils import embedding_functions
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq   # Groq API wrapper

# 🔑 Load Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
embedding_func = embedding_functions.DefaultEmbeddingFunction()
collection = chroma_client.get_or_create_collection(
    name="portfolio",
    embedding_function=embedding_func
)

# Initialize Groq LLM via LangChain
llm = ChatGroq(
    temperature=0.7,
    groq_api_key=GROQ_API_KEY,
    model="llama-3.3-70b-versatile"   # You can switch to Mixtral or other Groq-supported models
)

# Prompt template for generating cold email
template = """
You are an AI assistant that generates personalized cold emails for job applications.

Job Description:
{job_description}

Relevant Portfolio Matches:
{portfolio_matches}

Generate a professional cold email that highlights the candidate's strengths and aligns with the job description.
The email should be concise, formal, and impactful.
"""

prompt = PromptTemplate(
    input_variables=["job_description", "portfolio_matches"],
    template=template,
)

chain = LLMChain(llm=llm, prompt=prompt)

# --- STREAMLIT UI ---
st.set_page_config(page_title="AI Cold Email Generator", page_icon="📧")

st.title("📧 Wellcome to Cold Email Generator")


job_desc = st.text_area("Paste Job Description Here", height=200)

if st.button("Generate Email"):
    if not job_desc.strip():
        st.warning("⚠️ Please enter a job description first.")
    else:
        # Query ChromaDB for relevant portfolio entries
        results = collection.query(
            query_texts=[job_desc],
            n_results=3
        )
        portfolio_matches = "\n".join(results["documents"][0])

        # Run LangChain
        with st.spinner("Generating your tailored cold email..."):
            email = chain.run({
                "job_description": job_desc,
                "portfolio_matches": portfolio_matches
            })

        st.subheader("✉️ Generated Cold Email")
        st.write(email)
        st.success("✅ Email generated successfully!")
