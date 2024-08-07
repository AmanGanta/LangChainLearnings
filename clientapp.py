###FRONT END REQUESTS TO API
import requests
import streamlit as st

def get_openai_response(ip):
    res=requests.post(" http://localhost:8000/essay/invoke",json={"input":{'topic':ip}})
    return res.json()["output"]['content']


def get_ollama_response(ip):
    res=requests.post(" http://localhost:8000/poem/invoke",json={"input":{'topic':ip}})
    return res.json()["output"]

st.title("mutillm")
input_text1=st.text_input("Give essay topic")
input_text2=st.text_input("Give poem topic")

if input_text1:
    st.write(get_openai_response(input_text1))

if input_text2:
    st.write(get_ollama_response(input_text2))