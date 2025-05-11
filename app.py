import streamlit as st

# Assuming this is your conversational agent function
from agent import conversational_agent  # Replace with actual import

# Set up the app
st.set_page_config(page_title="WikiArxiv-Enhanced Conversational Agent", layout="centered")
st.title("🤖 WikiArxiv-Enhanced Conversational Agent")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Take user input
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.spinner("Thinking..."):
    # Call the agent
        try:
            response = conversational_agent(user_input)
            output_text = response.get("output", "Sorry, I couldn't find a good answer.")

            st.session_state.messages.append({"role": "assistant", "content": output_text})
            with st.chat_message("assistant"):
                st.markdown(output_text)
        except Exception as e:
            error_text = f"Error: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": error_text})
            with st.chat_message("assistant"):
                st.markdown(error_text)

with st.expander("ℹ️ How to use this agent"):
    st.markdown("""
    ### Example queries you can try:
    - "What is quantum computing?"
   
    - "Who was Marie Curie?"
    - "Tell me about the history of artificial intelligence"
    - "arXiv:2505.05452 "
    
    The agent will automatically determine when to use Wikipedia or ArXiv to enhance its responses!
    """)

