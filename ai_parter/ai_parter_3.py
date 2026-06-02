import streamlit as st
import os
from openai import OpenAI

# 设置页面的配置项
st.set_page_config(
    page_title="AI智能体",
    page_icon="📦",
    # 布局
    layout="wide",
    # 控制的是侧边栏的状态
    initial_sidebar_state="expanded",
    menu_items={}
)

# 标题
st.title("AI智能体设置")

# logo
st.logo("../resource/logo.png")

#系统提示词
system_prompt = "你的昵称是%s,你的性格是%s,每次和用户对话时都只能用一句话回复，像微信对话一样"


#初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = []

if "nick_name" not in st.session_state:
    st.session_state.nick_name = "苹果人"
if "nature" not in st.session_state:
    st.session_state.nature = "苹果性格"

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

#设置左侧侧边栏
with st.sidebar:
    st.subheader("智能体信息")
    nick_name = st.text_input("请输入你的昵称",placeholder="请输入你的昵称",value=st.session_state.nick_name)
    if nick_name:
        st.session_state.nick_name = nick_name
    nature=st.text_area("请输入你的性格",placeholder="请输入你的性格",value=st.session_state.nature)
    if nature:
        st.session_state.nature = nature

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
            messages=[{"role": "system", "content": system_prompt % (st.session_state.nick_name,st.session_state.nature)},
                *st.session_state.messages
            ],
            stream=True,
            reasoning_effort="high",
            extra_body={"thinking": {"type": "enabled"}}
        )
    #非流式输出的解析方式
    # print("-----大模型返回的结果：",response.choices[0].message.content)
    # st.chat_message("assistant").write(response.choices[0].message.content)

    #流式输出的解析方式
    response_message = st.empty()# 创建一个空的组件, 用于展示大模型返回的结果
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content
            response_message.chat_message("assistant").write(full_response)


    #保存大模型返回d消息

    #这是流式输出的返回结果
    # st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})

    st.session_state.messages.append({"role": "assistant", "content": full_response})




