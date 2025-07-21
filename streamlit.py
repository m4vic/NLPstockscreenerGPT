import streamlit as st
import asyncio
from Nlp_stocks import NLPStockScreener  # Your class in a separate file
import time
# Config
API_KEY = "********************************" # <--- paste gemini api key here
DB_PATH = "*****" # <--- db path here after running the scraper.py
# Streamlit page config
st.set_page_config(page_title="NLP Stock Screener", layout="wide")
# Session state to store screener instance
if 'screener' not in st.session_state:
    st.session_state.screener = NLPStockScreener(API_KEY, DB_PATH)
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
screener = st.session_state.screener
st.title("📈 Natural Language Stock Screener")
st.write("Ask questions like:")
st.write("- Find me some good value stocks")
st.write("- Show me high growth companies")
st.write("- What are the best dividend stocks?")
st.write("- Find safe stocks with low debt")
# Sidebar commands
with st.sidebar:
    st.header("Commands")
    if st.button("Clear Context"):
        screener.clear_conversation()
        st.session_state.chat_history = []
        st.success("Context cleared")
    
    if st.button("Show Current Stocks"):
        if screener.current_stocks:
            st.subheader("Current Stocks")
            for i, stock in enumerate(screener.current_stocks[:10], 1):
                st.write(f"{i}. {stock.get('name', 'N/A')} ({stock.get('symbol', 'N/A')})")
            if len(screener.current_stocks) > 10:
                st.write(f"... and {len(screener.current_stocks) - 10} more")
        else:
            st.info("No stocks currently loaded")
# Display chat history first (in reverse order for most recent at top)
if st.session_state.chat_history:
    st.divider()
    for user_msg, assistant_msg in reversed(st.session_state.chat_history):
        st.chat_message("user").markdown(user_msg)
        st.chat_message("assistant").markdown(assistant_msg)
# User input
user_input = st.chat_input("Type to find Best Indian stocks 🚀")
if user_input:
    with st.spinner("Analyzing..."):
        # Show user message in chat
        st.chat_message("user").markdown(user_input)
        
        # Get assistant response using your existing method
        response = screener.process_user_message(user_input)
        
        # Stream the response word by word
        assistant_placeholder = st.chat_message("assistant")
        message_placeholder = assistant_placeholder.empty()
        
        # Split response into words and display progressively
        words = response.split()
        displayed_text = ""
        
        for word in words:
            displayed_text += word + " "
            message_placeholder.markdown(displayed_text + "▌")  # Add cursor effect
            time.sleep(0.02)  # Adjust speed here (0.05 = 50ms between words)
        
        # Remove cursor and show final response
        message_placeholder.markdown(displayed_text)
        
        # Save to chat history
        st.session_state.chat_history.append((user_input, response))
        
        # Small delay before rerun
        time.sleep(0.5)
        st.rerun()
# Show previous chat history in expandable format
if st.session_state.chat_history:
    st.divider()
    st.write("📜 Previous Messages:")
    for user_msg, assistant_msg in st.session_state.chat_history:
        with st.expander(f"💬 {user_msg}"):
            st.markdown(assistant_msg)   
