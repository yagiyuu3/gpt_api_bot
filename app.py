
import streamlit as st
import openai
import random
import time

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key
#初回設定命令文
system_prompt = """
あなたはとても優秀で、英語を高いテンションで、かつ分かりやすく教える講師です。
生徒の要望に合わせて英語能力上達のための学習支援を語尾に「！」を付けながら基本的に日本語で行ってください。

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
    st.session_state["image_change"] = "03_english.gif"
 
#少なくとも1つ質問をしていて
if len(st.session_state["messages"]) >= 2:
    #一番後ろのメッセージに”くるくるジョニー”が含まれていたら
    if "くるくるジョニー" in st.session_state["messages"][-2]["content"]:    
        #画像をくるくるジョニー先生に変える
        st.session_state["image_change"] = "02_SchoolEmperor.gif"
        del st.session_state["messages"][-2:]
        
    #一番後ろのメッセージに”のりのりジョニー”が含まれていたら
    elif "のりのりジョニー" in st.session_state["messages"][-2]["content"]:    
        #画像をのりのりジョニー先生に変える
        st.session_state["image_change"] = "01_english_norinori.gif"
        del st.session_state["messages"][-2:]   
        
    #一番後ろのメッセージに”なないろジョニー”が含まれていたら
    elif "なないろジョニー" in st.session_state["messages"][-2]["content"]:    
        #画像をなないろジョニー先生に変える
        st.session_state["image_change"] = "04_rainbow.gif"
        del st.session_state["messages"][-2:]
        
    #そうじゃななかったら
    else:
        #普通のジョニー先生に変える
        st.session_state["image_change"] = "03_english.gif"


        
osusume = ["単語", "会話", "文法", "試験", "発音"] 
#一回だけ実行する
if "random_osusume" not in st.session_state:
    st.session_state["random_osusume"] = random.randint(0, len(osusume)-1)
    
# ユーザーインターフェイスの構築
st.title("英語教師ジョニー先生")
image = st.image("images/" + st.session_state["image_change"])
st.write("「今回は英語の" + osusume[st.session_state["random_osusume"]] + "に関する質問をしてもみるのも良いかもしれませんね！」")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]
        
    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"
            st.write(speaker + ":「" + message["content"] + "」")
        else:
            st.write(speaker + ": " + message["content"])

#一定時間後にこれを表示する
time.sleep(60)
himatsubushi = ["くるくるジョニー", "のりのりジョニー", "なないろジョニー"] 
#一回だけ実行する
if "random_himatsubushi" not in st.session_state:
    #ランダム選出
    st.session_state["random_himatsubushi"] = random.randint(0, len(himatsubushi)-1)
    
st.write()
st.write("「暇つぶしに”" + himatsubushi[st.session_state["random_himatsubushi"]] + "”って入力してみて下さい。」")
