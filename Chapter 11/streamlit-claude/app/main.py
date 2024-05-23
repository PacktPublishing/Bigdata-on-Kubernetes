import streamlit as st
import boto3
from langchain_community.chat_models import BedrockChat
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

bedrock = boto3.client(service_name='bedrock-runtime', region_name="us-east-1")

inference_modifier = {
    "max_tokens": 4096,
    "temperature": 0.5,
    "top_k": 250,
    "top_p": 1,
    "stop_sequences": ["\n\nHuman:"],
}

def choose_model(option):
    modelId = ""
    if option == "Claude 3 Haiku":
        modelId = "anthropic.claude-3-haiku-20240307-v1:0"
    elif option == "Claude 3 Sonnet":
        modelId = "anthropic.claude-3-sonnet-20240229-v1:0"
    
    model = BedrockChat(
        model_id=modelId,
        client=bedrock,
        model_kwargs=inference_modifier,
        streaming=True,
        callbacks=[StreamingStdOutCallbackHandler()],
    )
    return model

def reset_conversation():
    st.session_state.messages = []

# Streamlit app
def main():
    # Side bar with model selection
    with st.sidebar:
        option = st.selectbox(
            "What model do you want to talk to?",
            ("Claude 3 Haiku", "Claude 3 Sonnet")
        )
        st.write(f"You are talking to **{option}**")
        
        st.button('Reset Chat', on_click=reset_conversation)
        
    # Initialize Bedrock client with model of choice
    model = choose_model(option)
    
    st.title("Chat with Claude 3")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Enter your prompt here"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = st.write_stream(model.stream(prompt))
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()