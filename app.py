import streamlit as st
from src.pipeline import ask

st.set_page_config(
    page_title="Ather RAG Assistant",
    layout="wide"
)

st.title("Ather RAG Assistant")
st.write("Ask questions about the Ather documents.")

# Store conversation history
if "history" not in st.session_state:
    st.session_state.history = []

# User enters a question
q = st.chat_input("Ask a question about the Ather manuals...")

if q:
    with st.spinner("Searching the documents..."):
        answer = ask(q)

    st.session_state.history.append((q, answer))

# Display previous questions and answers
for question, answer in reversed(st.session_state.history):

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        st.write(answer)

        c1, c2 = st.columns(2)
        c1.button("Helpful", key=f"yes_{question}")
        c2.button("Not helpful", key=f"no_{question}")