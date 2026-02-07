import streamlit as st
import uuid
import time
from langchain_core.messages import HumanMessage, AIMessage
from core.assistant import (
    chatbot, 
    get_all_chats, 
    delete_chat,
    get_chat_title, 
    generate_chat_title, 
    update_chat_title
)
from core.logger import get_logger

logger = get_logger(__name__)

# -------------------------------------------------
# UTILS
# -------------------------------------------------
def generate_thread_id():
    return str(uuid.uuid4())

def add_thread(thread_id):
    # No longer needed as we rely on DB for list
    pass

def load_conversation(thread_id):
    try:
        # Checkpoint retrieval
        state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
        return state.values.get('messages', [])
    except Exception as e:
        logger.error(f"Error loading conversation {thread_id}: {e}")
        return []

def reset_chat():
    new_id = generate_thread_id()
    st.session_state['thread_id'] = new_id
    st.session_state['message_history'] = []
    # Create entry in DB so it shows up
    update_chat_title(new_id, "New Chat")

# -------------------------------------------------
# RENDER FUNCTION
# -------------------------------------------------
def render_chatbot_page():
    
    # Initialize Session State
    if 'message_history' not in st.session_state:
        st.session_state['message_history'] = []
    
    if 'thread_id' not in st.session_state:
        reset_chat() # Starts a new chat if none selected

    # -------------------------------------------------
    # SIDEBAR: Threads
    # -------------------------------------------------
    with st.sidebar.expander("💬 Chat History", expanded=True):
        if st.button("➕ New Conversation", use_container_width=True):
            reset_chat()
            st.rerun()
            
        st.markdown("---")
        
        # Fetch latest chats from DB
        threads = get_all_chats() # [(id, title), ...]
        
        if not threads:
            st.caption("No history yet.")
        
        for thread_id, title in threads:
            # Highlight active
            is_active = (thread_id == st.session_state.get('thread_id'))
            
            # Layout for button + delete
            col_chat, col_del = st.columns([4, 1])
            
            with col_chat:
                # Truncate title
                display_title = (title[:20] + '..') if len(title) > 20 else title
                btn_type = "primary" if is_active else "secondary"
                
                if st.button(f"{display_title}", key=f"sel_{thread_id}", use_container_width=True, type=btn_type, help=title):
                    st.session_state['thread_id'] = thread_id
                    # Load messages
                    raw_msgs = load_conversation(thread_id)
                    formatted_msgs = []
                    for msg in raw_msgs:
                        role = "user" if isinstance(msg, HumanMessage) else "assistant"
                        if isinstance(msg, (HumanMessage, AIMessage)):
                            formatted_msgs.append({'role': role, 'content': msg.content})
                    
                    st.session_state['message_history'] = formatted_msgs
                    st.rerun()
            
            with col_del:
                if st.button("🗑️", key=f"del_{thread_id}", help="Delete Chat"):
                    if delete_chat(thread_id):
                        if is_active:
                            reset_chat()
                        st.rerun()


    # -------------------------------------------------
    # MAIN CHAT AREA
    # -------------------------------------------------
    col_title, col_warn = st.columns([3, 1])
    with col_title:
        st.title("🤖 Investment Companion")
        st.caption("Powered by Google Gemini • Real-time Data • Calculations")
    with col_warn:
        st.warning("⚠️ Don't use unnecessarily", icon="💡")
    
    # Display History
    for message in st.session_state['message_history']:
        role = message['role']
        avatar = "👤" if role == "user" else "🤖"
        with st.chat_message(role, avatar=avatar):
            st.markdown(message['content'])
            
    # Input
    user_input = st.chat_input("Ask about market trends, specific stocks, or calculations...")
    
    if user_input:
        # Add User Message to History
        st.session_state['message_history'].append({'role': 'user', 'content': user_input})
        with st.chat_message('user', avatar="👤"):
            st.markdown(user_input)
            
        # Generate Response
        config = {
            'configurable': {'thread_id': st.session_state['thread_id']},
            "run_name": "chat_turn"
        }
        
        with st.chat_message('assistant', avatar="🤖"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                # Use invoke for robustness
                # Show a thinking spinner
                with st.spinner("Thinking..."):
                     response_generator = chatbot.stream(
                        {'messages': [HumanMessage(content=user_input)]},
                        config=config,
                        stream_mode='values'
                    )
                
                got_response = False
                
                for event in response_generator:
                    if 'messages' in event:
                        last_msg = event['messages'][-1]
                        if isinstance(last_msg, AIMessage):
                            # Extract text from content (handle both string and list formats)
                            content = last_msg.content
                            if isinstance(content, list):
                                # Extract text from list of content blocks
                                full_response = ""
                                for block in content:
                                    if isinstance(block, dict) and block.get('type') == 'text':
                                        full_response += block.get('text', '')
                                    elif isinstance(block, str):
                                        full_response += block
                            else:
                                full_response = str(content)
                            
                            message_placeholder.markdown(full_response)
                            got_response = True
                
                if not got_response:
                     full_response = "I apologize, but I couldn't generate a response. Please check the logs or API keys."
                     message_placeholder.markdown(full_response)
                     
            except Exception as e:
                logger.error(f"Chat Error: {e}")
                err_str = str(e)
                if "API_KEY" in err_str or "400" in err_str:
                     full_response = """
                     ⚠️ **Configuration Error**: 
                     Google API Key is invalid or missing. 
                     
                     **How to fix:**
                     1. Get a key from [Google AI Studio](https://aistudio.google.com/).
                     2. Open `.env` file.
                     3. Add `GOOGLE_API_KEY=your_key`.
                     4. Restart the App.
                     """
                else:
                     full_response = f"⚠️ I encountered an error: {e}"
                message_placeholder.error(full_response)

        st.session_state['message_history'].append({'role': 'assistant', 'content': full_response})
        
        # Generate Title lazy load check
        current_title = get_chat_title(st.session_state['thread_id'])
        if current_title == "New Chat" or not current_title:
             msgs = [HumanMessage(content=m['content']) if m['role']=='user' else AIMessage(content=m['content']) 
                     for m in st.session_state['message_history']]
             # We assume generate_chat_title handles errors internally (it does)
             generate_chat_title(st.session_state['thread_id'], msgs)
