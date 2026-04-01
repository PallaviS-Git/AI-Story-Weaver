# app.py
import streamlit as st
from story_manager import call_groq_api
from prompts import STORY_SYSTEM_PROMPT
from utils import extract_characters, export_markdown

st.set_page_config(page_title="AI Story Weaver", layout="wide")
st.title("🖋️ AI-Powered Story Weaver")

if "story" not in st.session_state:
    st.session_state.story = ""
if "genre" not in st.session_state:
    st.session_state.genre = ""
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7

# --- Story Setup ---
with st.expander("📖 Story Setup", expanded=True):
    title = st.text_input("Story Title")
    genre = st.selectbox("Genre", ["Fantasy", "Sci-Fi", "Mystery", "Romance", "Horror", "Comedy"])
    hook = st.text_area("Initial Hook / Setting", height=100)

    if st.button("Start the Story"):
        st.session_state.genre = genre
        prompt = f"{STORY_SYSTEM_PROMPT}\nGenre: {genre}\nHook: {hook}\nWrite the opening paragraph."
        opening = call_groq_api(prompt, temperature=st.session_state.temperature)
        st.session_state.story = f"# {title}\n\n{opening}"

# --- Main Storytelling View ---
st.subheader("📜 Story So Far")
story_area = st.empty()
story_area.text_area("Story", value=st.session_state.story, height=300, key="story_display")

# User input
user_input = st.text_area("Your Contribution", height=80)
col1, col2, col3 = st.columns([1,1,1])

with col1:
    if st.button("Continue with AI"):
        prompt = f"{STORY_SYSTEM_PROMPT}\nGenre: {st.session_state.genre}\nStory so far:\n{st.session_state.story}\nUser addition:\n{user_input}\nContinue the story with 1-2 paragraphs."
        ai_output = call_groq_api(prompt, temperature=st.session_state.temperature)
        st.session_state.story += f"\n\n{user_input}\n\n{ai_output}"
        story_area.text_area("Story", value=st.session_state.story, height=300, key="story_display")

with col2:
    if st.button("Give Me Choices"):
        prompt = f"{STORY_SYSTEM_PROMPT}\nGenre: {st.session_state.genre}\nStory so far:\n{st.session_state.story}\nUser addition:\n{user_input}\nSuggest 3 branching options for the story continuation."
        choices_text = call_groq_api(prompt, temperature=st.session_state.temperature)
        st.session_state.story += f"\n\n{user_input}\n\nChoices:\n{choices_text}"
        story_area.text_area("Story", value=st.session_state.story, height=300, key="story_display")

with col3:
    if st.button("Export Story as Markdown"):
        export_markdown(st.session_state.story)

# --- Creativity Slider ---
st.sidebar.subheader("🎨 Creativity / Temperature")
st.session_state.temperature = st.sidebar.slider("Adjust AI Creativity", 0.0, 1.0, st.session_state.temperature, 0.05)

# --- Character Tracker ---
st.sidebar.subheader("🧙 Characters")
characters = extract_characters(st.session_state.story)
st.sidebar.write(", ".join(characters))