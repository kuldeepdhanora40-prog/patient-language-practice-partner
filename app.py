import streamlit as st
import random

st.set_page_config(
    page_title="Patient Language Practice Partner",
    page_icon="🗣️",
    layout="centered"
)

LANGUAGES = {
    "English": {
        "greeting": "Hello! 😊 I'm your patient language practice partner.",
        "questions": [
            "What did you do today?",
            "What is your favorite food?",
            "Tell me about your hometown.",
            "What do you like to do in your free time?",
            "What is your dream job?"
        ],
        "tips": [
            "Try using complete sentences.",
            "Add a little more detail to your answer.",
            "Try using new vocabulary.",
            "Don't worry about mistakes. Keep practicing!"
        ]
    },
    "Spanish": {
        "greeting": "¡Hola! 😊 Soy tu compañero paciente para practicar idiomas.",
        "questions": [
            "¿Cómo estuvo tu día?",
            "¿Cuál es tu comida favorita?",
            "Háblame de tu ciudad.",
            "¿Qué haces en tu tiempo libre?",
            "¿Cuál es el trabajo de tus sueños?"
        ],
        "tips": [
            "Intenta usar frases completas.",
            "Practica nuevas palabras todos los días.",
            "Añade más detalles a tu respuesta.",
            "No tengas miedo de cometer errores."
        ]
    },
    "Hindi": {
        "greeting": "नमस्ते! 😊 मैं आपका धैर्यवान भाषा अभ्यास साथी हूँ।",
        "questions": [
            "आपका दिन कैसा रहा?",
            "आपका पसंदीदा खाना क्या है?",
            "अपने शहर के बारे में बताइए।",
            "आप खाली समय में क्या करना पसंद करते हैं?",
            "आपका सपना क्या है?"
        ],
        "tips": [
            "पूरे वाक्य में जवाब देने की कोशिश करें।",
            "हर दिन नए शब्द सीखें।",
            "अपने उत्तर में थोड़ा और विवरण जोड़ें।",
            "गलतियों से डरने की जरूरत नहीं है।"
        ]
    }
}

if "messages" not in st.session_state:
    st.session_state.messages = []

if "score" not in st.session_state:
    st.session_state.score = 0

if "questions_answered" not in st.session_state:
    st.session_state.questions_answered = 0

st.sidebar.title("⚙️ Practice Settings")

language = st.sidebar.selectbox("Choose a language", list(LANGUAGES.keys()))
level = st.sidebar.selectbox(
    "Your level",
    ["Beginner", "Intermediate", "Advanced"]
)

st.sidebar.divider()
st.sidebar.metric("Practice Score", st.session_state.score)
st.sidebar.metric("Questions Answered", st.session_state.questions_answered)

if st.sidebar.button("🔄 Start New Practice"):
    st.session_state.messages = []
    st.session_state.score = 0
    st.session_state.questions_answered = 0
    st.rerun()

st.title("🗣️ Patient Language Practice Partner")
st.write(
    "Practice a new language in a friendly and patient environment. "
    "Make mistakes, learn from them, and keep speaking! 🌱"
)

st.info(f"Language: **{language}**  |  Level: **{level}**")

if not st.session_state.messages:
    st.session_state.messages.append({
        "role": "assistant",
        "content": LANGUAGES[language]["greeting"]
    })
    st.session_state.messages.append({
        "role": "assistant",
        "content": random.choice(LANGUAGES[language]["questions"])
    })

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Type your answer here...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    word_count = len(user_input.split())

    if word_count >= 8:
        points = 10
        feedback = "Excellent! 🌟 Your answer has good detail."
    elif word_count >= 4:
        points = 7
        feedback = "Good job! 👍 Try adding a little more detail."
    elif word_count >= 2:
        points = 5
        feedback = "Nice attempt! 😊 Try making a longer sentence."
    else:
        points = 2
        feedback = "That's okay! Take your time and try a longer sentence."

    st.session_state.score += points
    st.session_state.questions_answered += 1

    st.session_state.messages.append({
        "role": "assistant",
        "content": (
            f"{feedback}\n\n"
            f"💡 **Practice tip:** "
            f"{random.choice(LANGUAGES[language]['tips'])}"
        )
    })

    st.session_state.messages.append({
        "role": "assistant",
        "content": random.choice(LANGUAGES[language]["questions"])
    })

    st.rerun()

st.divider()
st.caption(
    "🌱 Making mistakes is part of learning. "
    "Keep practicing and don't give up!"
)
