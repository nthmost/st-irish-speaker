import string
import streamlit as st
from googletrans import Translator
from nltk.tokenize import word_tokenize
import nltk
import os
from downloader import download_audio_files  # Make sure downloader.py is in the same directory

# Download punkt
nltk.download('punkt')

# Initialize translator
translator = Translator()

# Title
st.title('English to Irish Translation')

# Sidebar
st.sidebar.title('Settings')
show_punctuation = st.sidebar.checkbox('Show Punctuation')
dialect = st.sidebar.radio('Dialect', ('Ulster', 'Connaught', 'Munster'))

# Sample sentences
sample_sentences = [
    "What color is your table?",
    "That will put a fish in your pocket.",
    "Fair play to you!",
    "A good start is half the work."
]

# User input
# input_text = st.sidebar.selectbox('Sample sentences', sample_sentences, index=0)

# Initialize session state
if 'selected_sentence' not in st.session_state:
    st.session_state.selected_sentence = ""

# Display sample sentences as buttons
for sentence in sample_sentences:
    if st.sidebar.button(sentence):
        # Set the selected sentence in session state
        st.session_state.selected_sentence = sentence

# User input
input_text = st.text_input('Enter a sentence in English', value=st.session_state.selected_sentence)

if input_text:
    # Translate to Irish
    translated_text = translator.translate(input_text, dest='ga').text

    # Display translation
    st.header('Translation')
    st.write(translated_text)

    # Tokenize translation
    tokenized_text = word_tokenize(translated_text)

    # Remove punctuation tokens if not selected in the sidebar
    if not show_punctuation:
        tokenized_text = [token for token in tokenized_text if token not in string.punctuation]

    # Display tokens
    st.header('Tokens')
    for token in tokenized_text:
        # Check if token starts with "t-"
        if token.startswith("t-"):
            token = token[2:]  # Remove "t-" prefix

        # Download pronunciation
        audio_files = download_audio_files(token, dialect=dialect.upper())  # specify dialect as user's choice

        # Create URL for pronunciation
        pronunciation_url = f'https://www.teanglann.ie/en/fgb/{token.replace(" ", "_")}'

        # Display token with link to pronunciation
        st.markdown(f'- [{token}]({pronunciation_url})')

        # Display audio player(s) if audio file(s) exist, else display 'X'
        if audio_files:
            for audio_file in audio_files:
                st.audio(audio_file)
        else:
            st.markdown("X")

        st.divider()


