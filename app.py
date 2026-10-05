import os, random
import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="Patient Language Practice Partner", page_icon="🗣️")
LANGUAGES = {
 "English": {"hello":"Hi! 😊 I'm your patient practice partner. Mistakes are welcome here!","questions":["What did you do today?","Tell me about a food you love.","What do you enjoy doing in your free time?"]},
 "Spanish": {"hello":"¡Hola! 😊 Practiquemos juntos. ¡Los errores están bien!","questions":["¿Cómo estuvo tu día?","Háblame de una comida que te encanta.","¿Qué te gusta hacer en tu tiempo libre?"]},
 "Hindi": {"hello":"नमस्ते! 😊 मैं आपका धैर्यवान भाषा अभ्यास साथी हूँ। गलतियाँ करना ठीक है!","questions":["आपका दिन कैसा रहा?","अपने पसंदीदा खाने के बारे में बताइए।","आप खाली समय में क्या करना पसंद करते हैं?"]}
}
def token_value():
    try: return st.secrets.get("HF_TOKEN", os.environ.get("HF_TOKEN",""))
    except Exception: return os.environ.get("HF_TOKEN","")
def ai_reply(token, language, level, history):
    client=InferenceClient(model="openai/gpt-oss-20b", token=token)
    messages=[{"role":"system","content":f"You are a kind, patient language tutor. Help the learner practice {language} at {level} level. Reply mainly in {language}. Gently correct errors, briefly explain one useful point, encourage the learner, and ask one follow-up question. Keep replies concise and never shame the learner."}]+history
    result=client.chat_completion(messages=messages, max_tokens=350, temperature=0.7)
    return result.choices[0].message.content or "Nice try! Let's keep practicing."

if "messages" not in st.session_state: st.session_state.messages=[]
if "score" not in st.session_state: st.session_state.score=0
if "sent" not in st.session_state: st.session_state.sent=0
if "chosen_language" not in st.session_state: st.session_state.chosen_language="English"

st.sidebar.title("⚙️ Practice Settings")
language=st.sidebar.selectbox("Choose a language",list(LANGUAGES))
level=st.sidebar.selectbox("Your level",["Beginner","Intermediate","Advanced"])
st.sidebar.metric("Practice score",st.session_state.score)
st.sidebar.metric("Messages sent",st.session_state.sent)
if language != st.session_state.chosen_language:
    st.session_state.messages=[]; st.session_state.chosen_language=language
if st.sidebar.button("🔄 Start New Practice"):
    st.session_state.messages=[]; st.session_state.score=0; st.session_state.sent=0; st.rerun()

st.title("🗣️ Patient Language Practice Partner")
st.write("Practice a new language with a friendly AI partner. Make mistakes, learn, and keep going! 🌱")
st.info(f"Language: **{language}** · Level: **{level}**")
token=token_value()
if not token:
    st.warning('To enable AI, add `HF_TOKEN = "hf_your_token_here"` under your Streamlit app Settings → Secrets.')
if not st.session_state.messages:
    st.session_state.messages=[{"role":"assistant","content":LANGUAGES[language]["hello"]},
      {"role":"assistant","content":random.choice(LANGUAGES[language]["questions"])}]
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])
user_input=st.chat_input("Type your answer here...")
if user_input:
    st.session_state.messages.append({"role":"user","content":user_input})
    st.session_state.sent+=1
    st.session_state.score+=min(10,max(2,len(user_input.split())))
    with st.chat_message("user"): st.markdown(user_input)
    with st.chat_message("assistant"):
        if token:
            try:
                with st.spinner("Thinking patiently..."):
                    reply=ai_reply(token,language,level,st.session_state.messages[-12:])
                st.markdown(reply)
            except Exception as e:
                reply="I couldn't reach the model just now. Please check your Hugging Face token, model access, and provider availability."
                st.error(reply)
                st.caption(str(e)[:250])
        else:
            reply="Thanks for practicing! 🌱 Once the Hugging Face token is configured, I'll give you personalized corrections. For now, try writing a complete sentence with a little detail."
            st.markdown(reply)
    st.session_state.messages.append({"role":"assistant","content":reply})
st.divider()
st.caption("🌱 Every attempt counts. Keep practicing!")
