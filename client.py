import requests
import streamlit as st

def get_response(input):

    response = requests.post("http://localhost:8000/invoke",
                             json = {'input' : {'input':input}})

    return response.json()['output']['output']

st.title("Ask the Agent")
input_text = st.text_input("Ask any math questions or news around the world")
if input_text:
    st.write(get_response(input_text))