import streamlit as st
from googletrans import Translator
from nltk.tokenize import word_tokenize

# Initialize translator
translator = Translator()

# Title
st.title('English to Irish Translation')

# User input
input_text = st.text_input('Enter a sentence in English')

if input_text:
    # Translate to Irish
    translated_text = translator.translate(input_text, dest='ga').text
    
    # Display translation
    st.header('Translation')
    st.write(translated_text)

    # Tokenize translation
    tokenized_text = word_tokenize(translated_text)
    
    # Display tokens
    st.header('Tokens')
    for token in tokenized_text:
        # Create URL for pronunciation
        pronunciation_url = f'https://www.teanglann.ie/en/fuaim/{token.replace(" ", "_")}'
        # Display token with link to pronunciation
        st.markdown(f'- [{token}]({pronunciation_url})')


