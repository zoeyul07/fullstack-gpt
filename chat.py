import streamlit as st
import time

#session_state는 데이터를 넣기 위해 필요하며, 다시 실행되더라도 없어지지 않는다. 

if "messages" not in st.session_state:
  st.session_state["messages"] = []

def send_message(message, role, save=True):
  with st.chat_message(role):
    st.write(message)
  if save:
    st.session_state["messages"].append(({"message":message, "role":role}))
    

for message in st.session_state["message"]:
  send_message(message["message"], message["role"], save=False)


message = st.chat_input("send a message to the ai")

if message:
  send_message(message, "human")
  time.sleep(2)
  send_message("You said: {message}", "ai")

  with st.sidebar:
    st.write(st.session_state)
