import streamlit as st
import os 
import time
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

"""The st.session_state in the given code is used to store and manage data that needs to persist across different runs or interactions within a Streamlit app.

In simple terms:

st.session_state is like a storage box that remembers data and objects (like embeddings, documents, or a database) even as the user interacts with the app, allowing you to reuse or update them without reloading or recalculating every time.

This way, the code doesn't need to rerun expensive operations, like loading a website, splitting text, or creating embeddings, on every interaction. Instead, it checks if these are already in the "box" (st.session_state) and uses them directly if they are, saving time and resources.

So, st.session_state is essential for efficiently handling data and keeping the app's performance smooth and responsive."""
if "vector" not in st.session_state:
    st.session_state.embeddings=OpenAIEmbeddings()
    #When you use a WebBaseLoader with a URL like "https://machinelearningguider.blogspot.com/", it typically reads and loads only the content on that specific webpage, not the content from other sublinks or pages that the main page links to.
    st.session_state.loader=WebBaseLoader("https://machinelearningguider.blogspot.com/")
    st.session_state.docs=st.session_state.loader.load()
    st.session_state.txtspl=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    st.session_state.dc=st.session_state.txtspl.split_documents(st.session_state.docs)
    st.session_state.db=FAISS.from_documents(st.session_state.dc,st.session_state.embeddings)
st.title("RAG GROQ")
llm=ChatGroq(model="Gemma-7b-It")
from langchain_core.prompts import ChatPromptTemplate 
prompt1=ChatPromptTemplate.from_template("""Use this feedback to <context> {context} </context> answer the following question Question: {input}""")
re=st.session_state.db.as_retriever()
from langchain.chains.combine_documents import create_stuff_documents_chain
dcc=create_stuff_documents_chain(llm,prompt1)
from langchain.chains import create_retrieval_chain
retc=create_retrieval_chain(re,dcc)
p=st.text_input("Ask what ever you need")

if p:
    stm=time.process_time()
    resp=retc.invoke({"input":p})
    print("res time", time.process_time()-stm)
    st.write(resp['answer'])
    with st.expander("Document sim"):
        for i,d in enumerate(resp['context']):
            st.write(d.page_content)
            st.write("---------------------------------------------------")
