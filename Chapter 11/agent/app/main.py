import streamlit as st
import boto3
import uuid
import json
import os
from botocore.client import Config

agent_alias_id = os.getenv("AGENT_ALIAS_ID")
agent_id = os.getenv("AGENT_ID")
bedrock_config = Config(connect_timeout=120, read_timeout=120, retries={'max_attempts': 0})
bedrock_agent_client = boto3.client(
    "bedrock-agent-runtime",config=bedrock_config, region_name = "us-east-1"
)

## create a random id for session initiator id
session_id:str = str(uuid.uuid1())
enable_trace:bool = True
end_session:bool = False

def reset_conversation():
    st.session_state.messages = []


# Streamlit app
def main():
    # Side bar with model selection
    with st.sidebar:
        st.write(f"You are talking to **Bedrock Agent**")
        
        st.button('Reset Chat', on_click=reset_conversation)

        show_rationale = st.checkbox(label="Show Agent's rationale")
        
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
    
    
    st.title("Chat with Bedrock Agent")
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
            agentResponse = bedrock_agent_client.invoke_agent(
                inputText=prompt,
                agentId=agent_id,
                agentAliasId=agent_alias_id, 
                sessionId=session_id,
                enableTrace=enable_trace, 
                endSession= end_session
            )
            # Getting agents rationale from response events
            event_stream = agentResponse['completion']
            
            complete_answer = ""
            try:
                for event in event_stream:        
                    if 'chunk' in event:
                        data = event['chunk']['bytes']
                        agent_answer = data.decode('utf8')
                        end_event_received = True
                        # End event indicates that the request finished successfully
                    elif 'trace' in event:
                        if 'rationale' in event['trace']['trace']['orchestrationTrace']:
                            if event['trace']['trace']['orchestrationTrace']['rationale']['text'] == "":
                                continue
                            else:
                                if show_rationale:
                                    mid_rationale = "**Rationale:** " + event['trace']['trace']['orchestrationTrace']['rationale']['text']
                                    st.write(mid_rationale)
                                    complete_answer = complete_answer + mid_rationale + "\n\n"
                                else:
                                    continue
                    else:
                        raise Exception("unexpected event.", event)
            except Exception as e:
                raise Exception("unexpected event.", e)
            
            final_answer = "**Final answer:** " + agent_answer
            st.write(final_answer)
            complete_answer +=final_answer
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": complete_answer})

if __name__ == "__main__":
    main()