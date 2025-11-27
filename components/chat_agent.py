import streamlit as st

def chat_agent():

    # Initialize states
    if "chat_open" not in st.session_state:
        st.session_state.chat_open = False

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # ====== CSS ======
    st.markdown("""
        <style>
        /* Floating Chat Bubble */
        .chat-bubble {
            position: fixed;
            bottom: 25px;
            right: 25px;
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg,#818cf8,#c084fc);
            border-radius: 50%;
            display:flex;
            justify-content:center;
            align-items:center;
            font-size:32px;
            color:white;
            cursor:pointer;
            box-shadow:0 4px 15px rgba(0,0,0,0.3);
            transition:0.25s;
            z-index:9999;
        }
        .chat-bubble:hover {
            transform: scale(1.08);
            box-shadow:0 6px 18px rgba(129,140,248,0.45);
        }

        /* Chat Window */
        .chat-window {
            position: fixed;
            bottom: 100px;
            right: 25px;
            width: 330px;
            background:#0f172a;
            border:1px solid #1e293b;
            border-radius:12px;
            padding:10px;
            box-shadow:0 4px 20px rgba(0,0,0,0.4);
            animation: fadeIn 0.4s ease;
            z-index:9999;
        }

        @keyframes fadeIn {
            from { opacity:0; transform:translateY(20px); }
            to { opacity:1; transform:translateY(0); }
        }
        </style>
    """, unsafe_allow_html=True)

    # ====== CHAT BUBBLE BUTTON (Streamlit button) ======

    bubble_col = st.empty()
    with bubble_col:
        if st.button("💬", key="bubble", help="Chat with AI"):
            st.session_state.chat_open = not st.session_state.chat_open

    # ====== RENDER CHAT WINDOW ======
    if st.session_state.chat_open:
        with st.container():
            st.markdown("<div class='chat-window'>", unsafe_allow_html=True)

            st.markdown("### 🤖 AI Chat Assistant")

            # SHOW CHAT HISTORY
            for chat in st.session_state.chat_history:
                role = "🧑 You" if chat["role"] == "user" else "🤖 AI"
                st.markdown(f"**{role}:** {chat['text']}")

            user_input = st.text_input("Message", key="chat_message")

            if st.button("Send", key="send_message"):
                if user_input.strip():
                    st.session_state.chat_history.append(
                        {"role": "user", "text": user_input}
                    )

                    # Dummy response (you can replace with your AI API)
                    response = f"I received: **{user_input}**"
                    st.session_state.chat_history.append(
                        {"role": "assistant", "text": response}
                    )

            st.markdown("</div>", unsafe_allow_html=True)
