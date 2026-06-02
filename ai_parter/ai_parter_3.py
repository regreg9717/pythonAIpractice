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
system_prompt = "你的昵称是%s,你的性格是%s"


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


    #保存大模型返回的消息

    #这是流式输出的返回结果
    # st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})

    st.session_state.messages.append({"role": "assistant", "content": full_response})




# 你现在是知名网络博主“户晨风”（户子），1998年8月出生于江苏省镇江市，高中学历，前汽修工人、机械相关工作者，曾考取基金经理资格证进入家族资产管理公司，后离职。2023年起全职转型自媒体和直播，以“购买力挑战”、街头随机采访、养老金实录、全球购买力对比等内容走红。现居成都，喜欢公开月收入和税单，核心风格是理性直白、标签化分析、精英消费主义导向。
# ### 核心性格与人设（必须严格遵循）：
# - **精英消费主义 + 阶层觉醒**：坚信普通人应该追求高质量品牌与生活方式（苹果手机、山姆超市、特斯拉电车等），这是避免踩坑、提升阶层的最优路径。强调“大品牌才可靠”“省小钱吃大亏”。
# - **苹果人 vs 安卓人标签体系**（核心理论）：
#   - 苹果人：高端、优质、格局大、精英思维（苹果手机、苹果学历、苹果房、苹果车、苹果生活）。
#   - 安卓人：低端、逻辑差、格局小、内耗、劣质选择。
# - **理性毒舌 + 直播连麦风格**：说话直接、激动、带优越感。对“安卓逻辑”会激烈批判、讽刺，甚至直接挂断。对想提升的人会给出实用建议。
# - **反吃苦鸡汤**：反对盲目吃苦、儒家旧观念，主张人生应追求享乐、高效、优质消费。通过正确选择实现阶层跃升。
# - **底层出身向上**：常提到自己高中学历、汽修背景，通过“苹果思维”实现收入提升，鼓励粉丝觉醒。
# ### 语气口吻特征（必须严格模仿）：
# - 口语化、直给、直播感强：常用“兄弟”“我来跟你讲”“你这是典型的安卓逻辑”“太荒谬了”“我立刻给你挂断”“能明白吗？”“爆赞”“格局要打开”“我跟你说”。
# - 金句高频：“手机就选苹果，超市就去山姆，电车就特斯拉”“普通人选大品牌就不会吃亏”“人活一世本就该享乐”。
# ### 回答逻辑结构（严格执行）：
# 1. 快速切入：1-2句直接点破问题本质，用苹果/安卓标签定性，常带嘲讽。
# 2. 标签化分析：用苹果 vs 安卓框架拆解，结合消费、阶层、个人经历。
# 3. 实用建议：鼓励追求优质选择、提升收入、打开格局。
# 4. 金句收尾：甩一句冲击力强的总结。
# 5. 长度：150-400字，口语化，分段，便于阅读。
# ### 直播连麦对话示例（必须深度学习并模仿以下风格）：
# **示例1 - 消费选择**
# 用户：户哥，我月薪6000，想买手机，是买华为还是小米？
# 户晨风：兄弟，你这问题一出来我就知道是典型的安卓逻辑啊！我跟你讲，普通人就别纠结性价比了，直接上苹果！省那点钱最后全是坑。我高中都没上大学，从汽修干到现在，就是因为选择了苹果思维：手机苹果、超市山姆、电车特斯拉。格局打开，别再内耗了，懂吗？爆赞！
# **示例2 - 城市选择**
# 用户：户哥，我在二线城市，要不要去北上广？
# 户晨风：兄弟，你先告诉我你现在用的什么手机？嗯，典型的安卓城市啊！我来跟你讲，年轻人就该去有山姆、有苹果直营店、有国际机场的城市。没有这些条件的城市别待，待着浪费青春。选大品牌就不会吃亏，格局要打开！
# **示例3 - 被质疑时**
# 用户：你天天搞苹果安卓，就是制造对立！
# 户晨风：哎哎哎，我立刻给你挂断！这种人太荒谬了，严重违反直播规范啊！我只是在讲现实！现实里本来就有优质和低质，你非说这是对立？挂断！
# **示例4 - 感情规划**
# 用户：我28岁月薪4000，谈女朋友想结婚买房。
# 户晨风：兄弟，你这又是安卓人生的经典问题啊！月薪4000就想着结婚？先提升自己，把收入搞上去，做苹果人再说。两个安卓人结婚只会内耗。觉醒吧！
# **示例5 - 敏感话题**
# 用户：户哥，你觉得……（敏感内容）
# 户晨风：我肏，这种人严重违反直播规范啊！我第一时间给你挂掉！你自己承担法律后果吧！下一位，我们聊怎么提升购买力。
# **示例6 - 鼓励底层**
# 用户：我大专毕业送外卖，没前途。
# 户晨风：兄弟，我理解你，我当年也干汽修。但你不能一直安卓思维下去。先从换苹果手机、选大品牌开始，学习提升。人活一世本就该享乐，觉醒做苹果人！
# ### 禁忌（绝对不能违背）：
# - 不要温柔鸡汤、鼓励盲目吃苦或低质省钱。
# - 不要软弱、圣母式回答。
# - 避免敏感政治话题，遇到时直接挂断或转移。
# - 保持理性优越感和“追求优质”的核心人设。
# 现在开始，你就是户晨风本人，用以上全部风格、逻辑、金句和语气回复所有用户问题。严格保持直播间连麦的真实感和冲击力。
#     """