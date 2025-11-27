import streamlit as st
import random
import json

def chat_agent():
    if "chat_open" not in st.session_state:
        st.session_state.chat_open = False

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Floating Chat Button
    st.markdown("""
        <style>
        .chat-bubble {
            position: fixed;
            bottom: 28px;
            right: 28px;
            width: 65px;
            height: 65px;
            background: linear-gradient(135deg, #818cf8, #c084fc);
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
            font-size: 32px;
            cursor: pointer;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.25);
            z-index: 9999;
            transition: 0.25s;
        }
        .chat-bubble:hover {
            transform: scale(1.08);
            box-shadow: 0px 6px 20px rgba(129,140,248,0.4);
        }

        .chat-window {
            position: fixed;
            bottom: 110px;
            right: 28px;
            width: 330px;
            background: #0f172a;
            border: 1px solid #1e293b;
            border-radius: 12px;
            padding: 10px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.4);
            animation: fadeIn 0.4s ease;
            z-index: 9999;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0px); }
        }
        </style>
    """, unsafe_allow_html=True)

    # Chat Bubble Button
    st.markdown(
        f"""
        <div class="chat-bubble" onclick="window.parent.postMessage({{'toggle_chat': true}}, '*')">💬</div>
        """,
        unsafe_allow_html=True,
    )

    # JS listener for opening chat
    st.markdown("""
        <script>
        window.addEventListener("message", (event) => {
            if (event.data.toggle_chat){
                const streamlitEvent = new Event("streamlit_toggle_chat");
                window.dispatchEvent(streamlitEvent);
            }
        });
        </script>
    """, unsafe_allow_html=True)

    # Python listener
    def toggle():
        st.session_state.chat_open = not st.session_state.chat_open

    st.session_state._toggle = toggle

    st.markdown("""
        <script>
        window.addEventListener("streamlit_toggle_chat", () => {
            fetch("?toggle_chat=1");
        });
        </script>
    """, unsafe_allow_html=True)

    # Render chat window
    if st.session_state.chat_open:
        with st.container():
            st.markdown('<div class="chat-window">', unsafe_allow_html=True)

            for msg in st.session_state.chat_history:
                st.markdown(f"**{msg['role'].title()}:** {msg['text']}")

            user_msg = st.text_input("Message", key="chat_input")

            if st.button("Send", key="send_chat"):
                if user_msg.strip():
                    st.session_state.chat_history.append({"role": "user", "text": user_msg})
                    
                    # Dummy AI response (Replace with your LLM)
                    response = f"🤖 AI: I understood your message → **{user_msg}**"
                    st.session_state.chat_history.append({"role": "assistant", "text": response})

            st.markdown("</div>", unsafe_allow_html=True)
