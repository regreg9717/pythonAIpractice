import streamlit as st
import os
from openai import OpenAI
from datetime import datetime
import json

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
#生成会话标识函数
def generate_session_name():
    return datetime.now().strftime("%Y-%m-%d %H-%M-%S")

#保存会话信息的函数
def save_session():
    if st.session_state.current_session:
        session_data = {
            "nick_name": st.session_state.nick_name,
            "nature": st.session_state.nature,
            "current_session": st.session_state.current_session,
            "messages": st.session_state.messages
        }

        if not os.path.exists("sessions"):
            os.mkdir("sessions")
        with open(f"sessions/{st.session_state.current_session}.json", "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)


#加载所有会话信息
def load_sessions():
    session_list = []
    #加载sessions目录下的文件
    if os.path.exists("sessions"):
        file_list = os.listdir("sessions")
        for filename in file_list:
            if filename.endswith(".json"):
                session_list.append(filename[:-5])
    session_list.sort(reverse=True) #排序, 降序排列
    return session_list

#加载指定会话信息
def load_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            # 读取会话信息
            with open(f"sessions/{session_name}.json", "r", encoding="utf-8") as f:
                session_data = json.load(f)
                st.session_state.messages = session_data["messages"]
                st.session_state.nick_name = session_data["nick_name"]
                st.session_state.nature = session_data["nature"]
                st.session_state.current_session = session_name
    except Exception:
        st.error("加载会话失败!")

#删除指定会话信息
def delete_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            os.remove(f"sessions/{session_name}.json")
            #如果删除的是当前的会话，删除后，应该不会再显示会话内容
            if session_name==st.session_state.current_session:
                st.session_state.messages = []
                st.session_state.current_session = generate_session_name()
    except:
        st.error("删除会话失败!")
# 标题
st.title("AI智能体")

# logo
st.logo("../resource/logo.png")

#系统提示词
system_prompt = "你的昵称是%s,你的性格是%s,每次和用户对话时都只能用一句话回复，像微信聊天一样。"


#初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = []

if "nick_name" not in st.session_state:
    st.session_state.nick_name = "苹果人"
if "nature" not in st.session_state:
    st.session_state.nature = "苹果性格"

#会话标识
if "current_session" not in st.session_state:
    # print(datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
    st.session_state.current_session = datetime.now().strftime("%Y-%m-%d %H-%M-%S")


#展示聊天信息
st.text(f"当前会话：{st.session_state.current_session}")
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
    st.subheader("AI控制面板")

    if st.button("新建会话",width="stretch",icon="😀"):
        save_session()

        if st.session_state.messages:#如果聊天信息非空，则创建下一个json，否则不建
            st.session_state.messages = []
            st.session_state.current_session = generate_session_name()
            save_session()
            st.rerun()  # 重新运行当前页面

    #加载会话历史
    st.text("会话历史")
    session_list=load_sessions()
    for session in session_list:
        col1,col2=st.columns([4,1])
        with col1:
            if st.button(session,width="stretch",icon="🤡",key=f"load_{session}",type="primary" if session==st.session_state.current_session else "secondary"):
                load_session( session)
                st.rerun()
        with col2:
            if st.button("",width="stretch",icon="😂",key=f"delete_{session}"):
                delete_session(session)
                st.rerun ()
        # st.button(session,width="stretch")

    #分割线
    st.divider()

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
            model="deepseek-chat",
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

    #保存会话信息
    save_session()


