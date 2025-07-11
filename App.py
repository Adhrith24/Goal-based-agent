import streamlit as st
from openai import OpenAI
import os

GROQ_API_KEY="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"

client=OpenAI(api_key=GROQ_API_KEY,base_url="https://api.groq.com/openai/v1")

st.set_page_config(page_title="goal based medical agent",layout="centered")
st.title("goal based medical triage assistant")
st.markdown("describe your medical condition or symptoms. they AI will decide whether you need rest, a doctor, or emergency care")

user_input=st.text_area("describe your symptoms or how you are feeling")
if "chat_history" not in st.session_state:
    st.session_state.chat_history=[]

if user_input:
    st.session_state.chat_history.append({"role":"user","content":user_input})
    with st.spinner("analysing your condition"):
        try:
            messages=[{"role":"system","content":
                       "you are a goal based medical assistant. your goal is to analyse user symptoms and advise one of the following:"
                       "(1) rest at home,(2) consult a doctor,(3) go to emergency. be cautious ask follow up questions if needed"
                       "be cleared and structured in response"}
                       ] + st.session_state.chat_history
            
            response=client.chat.completions.create(
                model="llama3-8b-8192",messages=messages,temperature=0.5,max_tokens=800)
            
            ai_reply=response.choices[0].message.content
            st.session_state.chat_history.append({"role":"assistant","content":ai_reply})
            st.success("recommendations:")
            st.markdown(ai_reply)
        except Exception as e:
            st.error(f"error:{str(e)}") 

