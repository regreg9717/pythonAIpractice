import streamlit as st
import os
from openai import OpenAI

# 设置页面的配置项
st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="📦",
    # 布局
    layout="wide",
    # 控制的是侧边栏的状态
    initial_sidebar_state="expanded",
    menu_items={}
)

# 标题
st.title("AI智能伴侣")

# logo
st.logo("../resource/logo.png")

#系统提示词
system_prompt="You are a helpful assistant"

#初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = []

#展示聊天信息
for message in st.session_state.messages:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        st.chat_message("assistant").write(message["content"])

# 创建与AI大模型进行交互的客户端对象
client = OpenAI(
#这里直接用环境变量的方式获取API密钥，防止泄露密钥
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

#获取用户输入
prompt=st.chat_input("请输入你的问题")
#此时字符串会自动转化为布尔值，非空即为真
if prompt:
    st.chat_message("user").write(prompt)
    print("-----调用AI大模型，提示词为：",prompt)
    #保存用户输入的消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    #调用AI大模型
    with st.spinner("思考中..."):
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[{"role": "system", "content": system_prompt}]+ st.session_state.messages,
            stream=False,
            reasoning_effort="high",
            extra_body={"thinking": {"type": "enabled"}}
        )
    print("-----大模型返回的结果：",response.choices[0].message.content)
    st.chat_message("assistant").write(response.choices[0].message.content)
    #保存大模型返回的消息
    st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})