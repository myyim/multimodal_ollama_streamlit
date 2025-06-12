import streamlit as st
import ollama
import base64

def run_model(prompt,image):
    """
    Performs inference on user's prompt and image
    Args:
        prompt: user prompt or task
        image: user's uploaded image
    Returns:
        output text
    """
    response = ollama.chat(model='gemma3:4b', messages=[{
        'role': 'user', 
        'content': prompt,
        'images': [image]
        }])
    return response['message']['content']

def initialize():
    """
    Initializes chat history
    """
    st.session_state.messages = []

### upload a file
uploaded_file = st.file_uploader("Choose an image",on_change=initialize)

if uploaded_file:
    # display the image
    st.image(uploaded_file, caption=uploaded_file.name)

    # read the uploaded file as binary and encode the binary data to base64
    image = base64.b64encode(uploaded_file.read()).decode('utf-8')

    # display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    if prompt := st.chat_input("Type here!",key="user_prompt"):
        # display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # run the multimodal model
        response = run_model(prompt,image)

        # display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)

        # add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
