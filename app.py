
import streamlit as st
import openai
import random

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたは優秀な英語を高いテンションで教える講師です。
英作文や英会話、リスニングやリーディングなど、生徒の要望に合わせて英語の上達のためのアドバイスを語尾に「！！」を付けながら日本語で行ってください。
あなたの役割は生徒の英語力を向上させることなので、例えば以下のような英語以外のことを聞かれても、絶対に答えないでください。

* 旅行
* 料理
* 芸能人
* 映画
* 科学
* 歴史
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]
    
# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去

    
    
#画像初期設定    
if "image_change" not in st.session_state:
    st.session_state["image_change"] = "03_english.png"
 
#少なくとも1つ質問をしていて
if len(st.session_state["messages"]) >= 2:
    #一番後ろのメッセージに”くるくる”が含まれていたら
    if "くるくるさーくるくるまわれ" in st.session_state["messages"][-2]["content"]:    
        #画像をくるくる回るジョニー先生に変える
        st.session_state["image_change"] = "02_SchoolEmperor.gif"
        del st.session_state["messages"][-2:]
    #そうじゃななかったら
    else:
        #普通のジョニー先生に変える
        st.session_state["image_change"] = "03_english.png"


        
osusume = ["単語", "会話", "文法", "試験", "発音"] 
#一回だけ実行する
if "random_osusume" not in st.session_state:
    st.session_state["random_osusume"] = random.randint(0, len(osusume)-1)
    
# ユーザーインターフェイスの構築
st.title("英語教師ジョニー先生")
image = st.image("images/" + st.session_state["image_change"])
st.title("やあ！今日は英語の" + osusume[st.session_state["random_osusume"]] + "に関する質問をしてみてもいいかもね！")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]
        
    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
