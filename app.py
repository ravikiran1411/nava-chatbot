import streamlit as st
import boto3
import json

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Nova AI Chatbot", page_icon="🤖")
st.title("🚀 Amazon Nova 2 Lite Chatbot")

# --- 2. SECURE AWS CLIENT INITIALIZATION ---
# This pulls from your .streamlit/secrets.toml file automatically
try:
    client = boto3.client(
        "bedrock-runtime",
        aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
        region_name=st.secrets["AWS_DEFAULT_REGION"]
    )
    MODEL_ID = "us.amazon.nova-2-lite-v1:0"
except Exception as e:
    st.error("Credential Error: Please check your .streamlit/secrets.toml file.")
    st.stop()

# --- 3. CHAT HISTORY MANAGEMENT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. USER INPUT & AI RESPONSE ---
if prompt := st.chat_input("Ask me anything..."):
    # Add user message to state and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI Response
    with st.chat_message("assistant"):
        # Format the chat history for the Amazon Nova Converse API
        formatted_messages = [
            {"role": m["role"], "content": [{"text": m["content"]}]} 
            for m in st.session_state.messages
        ]
        
        try:
            # Call Amazon Bedrock
            response = client.converse(
                modelId=MODEL_ID,
                messages=formatted_messages,
                inferenceConfig={"maxTokens": 512, "temperature": 0.7}
            )
            
            # Extract the text output
            full_response = response["output"]["message"]["content"][0]["text"]
            st.markdown(full_response)
            
            # Save assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Bedrock Error: {e}")