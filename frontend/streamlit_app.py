import streamlit as st
import requests

API_URL = "http://localhost:8000/chat"

st.set_page_config(page_title="EchoMind", page_icon="🧠", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "model" not in st.session_state:
    st.session_state.model = "llama3.2:3b"

with st.sidebar:
    st.title("EchoMind")
    st.divider()
    st.subheader("Model")
    model = st.selectbox(
        "Choose model",
        [
            "llama3.2:3b",
            "llama3.2:1b",
        ],
        index=0,
    )
    st.session_state.model = model
    st.divider()
    st.subheader("Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload files for RAG", type=["pdf", "txt", "docx"], accept_multiple_files=True
    )

    if uploaded_files:
        st.success(f"{len(uploaded_files)} file(s) ready")
    st.divider()
    st.subheader("Chat Settings")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.3)
    st.divider()
    if st.button("Reset Chat"):
        st.session_state.messages = []
        st.rerun()

st.title("EchoMind Assistant")

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask something...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"message": prompt, "model": st.session_state.model},
                    timeout=None,
                )

                response.raise_for_status()
                result = response.json()
                answer = result.get("response", "No response")
            except Exception as e:
                answer = f"API Error: {e}"
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
