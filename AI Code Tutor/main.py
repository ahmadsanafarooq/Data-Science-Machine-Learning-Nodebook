import streamlit as st
from agent.tutor_agent import run_agent

st.title("🧠 AI Code Tutor")

user_input = st.text_area("Enter your code or question here", height=300)

if st.button("Submit"):
    if user_input.strip():
        response = run_agent(user_input)
        st.markdown("### Response:")
        st.code(response, language='python' if 'def' in user_input else 'text')
