import streamlit as st
from huggingface_hub import InferenceClient

# Setup the page
st.set_page_config(page_title="My AI Assistant")
st.title("🤖 My Global AI")

# Enter your Hugging Face Token here
api_key = st.sidebar.text_input("Enter Hugging Face Token", type="password")

if api_key:
    # We are using a high-quality open-source model (Mistral)
    client = InferenceClient("mistralai/Mistral-7B-Instruct-v0.2", token=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me anything!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response from Hugging Face
        response = ""
        for message in client.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            stream=True,
        ):
            token = message.choices[0].delta.content
            response += token

        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.warning("Please enter your Hugging Face Token in the sidebar to start.")
