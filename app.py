import streamlit as st
import boto3
import json

st.set_page_config(page_title="Nova AI Chatbot", page_icon="🤖")
st.title("🚀 Amazon Nova 2 Lite Chatbot")

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

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        formatted_messages = [
            {"role": m["role"], "content": [{"text": m["content"]}]} 
            for m in st.session_state.messages
        ]
        
        try:
            response = client.converse(
                modelId=MODEL_ID,
                messages=formatted_messages,
                inferenceConfig={"maxTokens": 512, "temperature": 0.7}
            )
            
           
            full_response = response["output"]["message"]["content"][0]["text"]
            st.markdown(full_response)
            
           
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Bedrock Error: {e}")