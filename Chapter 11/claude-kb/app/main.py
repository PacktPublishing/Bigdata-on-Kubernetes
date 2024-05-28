import streamlit as st
import boto3
import os
from botocore.client import Config
from langchain.prompts import PromptTemplate
from langchain.retrievers.bedrock import AmazonKnowledgeBasesRetriever
from langchain.chains import RetrievalQA
from langchain_community.chat_models import BedrockChat

kb_id = os.getenv("KB_ID")
bedrock_config = Config(connect_timeout=120, read_timeout=120, retries={'max_attempts': 0})
bedrock_agent_client = boto3.client(
    "bedrock-agent-runtime",config=bedrock_config, region_name = "us-east-1"
)
bedrock = boto3.client(service_name='bedrock-runtime', region_name="us-east-1")

PROMPT_TEMPLATE = """
Human: You are a friendly AI assistant and provide answers to questions about AWS competency program for partners.
Use the following pieces of information to provide a concise answer to the question enclosed in <question> tags.
Don't use tags when you generate an answer. Answer in plain text, use bullets or lists if needed.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
<context>
{context}
</context>

<question>
{question}
</question>

The response should be specific and use statistics or numbers when possible.

Assistant:"""
claude_prompt = PromptTemplate(template=PROMPT_TEMPLATE, 
                               input_variables=["context","question"])

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
    )
    return model

def reset_conversation():
    st.session_state.messages = []

retriever = AmazonKnowledgeBasesRetriever(
        knowledge_base_id=kb_id,
        retrieval_config={
            "vectorSearchConfiguration": {
                "numberOfResults": 4
            }
        },
        client=bedrock_agent_client
    )

# Streamlit app
def main():
    # Side bar with model selection
    with st.sidebar:
        option = st.selectbox(
            "What model do you want to talk to?",
            ("Claude 3 Haiku", "Claude 3 Sonnet")
        )
        
        st.button('Reset Chat', on_click=reset_conversation)

        st.write(f"You are talking to **{option}**")
        st.write("**Competency information available:**")
        st.write("""
            - Conversational AI
            - Data & Analytics
            - DevOps
            - Education
            - Energy
            - Financial Services
            - Machine Learning
            - Security"""
                 )
        
    # Initialize Bedrock client with model of choice
    model = choose_model(option)

    qa = RetrievalQA.from_chain_type(
        llm=model,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=False,
        chain_type_kwargs={"prompt": claude_prompt}
    )
    
    st.title("RAG with Claude 3")
    st.subheader("AWS Competency Program", divider="grey")

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
            response = qa.invoke(prompt)['result']
            st.write(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()