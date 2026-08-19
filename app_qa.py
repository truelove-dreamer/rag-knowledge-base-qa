import streamlit as st
import time
from rag import RagService
import config_data as config

#标题
st.title("智能客服")
st.divider()       #分隔符

if "message" not in st.session_state:
    st.session_state["message"] = [{"role": "assistant","content": "你好啊，有什么能帮助你的？"}]

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])
#在页面最下端提供用户输入栏
prompt = st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})
    with st.spinner("AI思考中..."):
        res_stream = st.session_state["rag"].chain.stream({"input": prompt},config.session_config)

        res = st.chat_message("assistant").write_stream(res_stream)
        st.session_state["message"].append({"role": "assistant", "content": res})