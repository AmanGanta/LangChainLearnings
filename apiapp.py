### FAST API CREATION


from fastapi import FastAPI
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate 
from langserve import add_routes
import uvicorn
import os 
from langchain_community.llms import Ollama 

from dotenv import load_dotenv
load_dotenv()
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")

app=FastAPI(title="lang",
            version="1.0",
            description="api runner")

add_routes(app,ChatOpenAI(),path="/openai")
model=ChatOpenAI()
llm=Ollama(model="llama2")

prompt1=ChatPromptTemplate.from_template("Write me essay on {topic} with in 50 words")
prompt2=ChatPromptTemplate.from_template("Write me poem on {topic} with in 50 words")

add_routes(app,prompt1|model,path="/essay")
add_routes(app,prompt2|llm,path="/poem")

if __name__=="__main__":
    uvicorn.run(app,host='localhost',port=8000)
 