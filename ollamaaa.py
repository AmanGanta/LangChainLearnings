# OPEN SOURCE LLM IN LOCAL MACHINE USING OLLAMA DESKTOP     note that before we use it we need to run "Ollama run 'model_name'" 

from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import StrOutputParser 
from langchain_community.llms import Ollama 
import streamlit as st 
import os 
from dotenv import load_dotenv
load_dotenv()
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
prompt = ChatPromptTemplate.from_messages([
    ('system', "please assist the user based on his needs and never go beyond 30 words with your answer."),
    ('user', "Question:{question}")
])

st.title("demochat")
input_text=st.text_input("Ask based on your Need")

llm=Ollama(model="llama2")
output_parser=StrOutputParser()
chain=prompt|llm|output_parser 

if input_text:
    st.write(chain.invoke({'question':input_text}))