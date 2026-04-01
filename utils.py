# utils.py
import re
import streamlit as st

def extract_characters(story_text):
    """
    Very basic character extraction: look for capitalized words (names)
    """
    words = re.findall(r'\b[A-Z][a-z]+\b', story_text)
    return list(set(words))

def export_markdown(story_text, filename="story.md"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(story_text)
    st.success(f"Story exported to {filename}")