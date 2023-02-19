import os.path
import random
import streamlit as st
import pandas as pd
import pickle


m3u_filepaths_file = 'playlists/streamlit.m3u8'
ESSENTIA_ANALYSIS_PATH = 'data/data.jsonl.pickle'


def load_essentia_analysis():
    return pandas.read_pickle(ESSENTIA_ANALYSIS_PATH)



# Leer archivo .pickle
with open('data/data.jsonl.pickle', 'rb') as f:
    data = pickle.load(f)

# Utilizar la variable audio_analysis
#audio_analysis_styles = audio_analysis.columns

# Convertir a DataFrame
audio_analysis = pd.DataFrame(data)

# Obtener las columnas
audio_analysis_styles = audio_analysis.columns


st.write('# Audio analysis playlists example')
st.write(f'Using analysis data from `{ESSENTIA_ANALYSIS_PATH}`.')
#audio_analysis = load_essentia_analysis()
#audio_analysis_styles = audio_analysis.columns
st.write('Loaded audio analysis for', len(audio_analysis), 'tracks.')

st.write('## ⌛️ Tempo')
tempo = st.slider('Choose a tempo', 60, 180, 25)
st.write("The following tempo is selected:", tempo)

st.write('## 🪗 Type of song: instrumental or vocal tune')
instrument = st.checkbox('🎙️ 🎻 Instrumental or vocal tune')

if instrument:
    st.write('Instrumental song is selected!🎺')
else:
    st.write('Vocal song is selected! 🎤')
    
st.write('## 🩰 Danceability')
danceability = st.slider('Choose how danceable you want the song to be:', 0, 3)
st.write("Danceability value is...💃🏽", danceability)

st.write('## 🤨🤩 Arousal and valence')
arousal = st.slider('Choose the arousal:', 1,9)
st.write("🐢 Arousal value is...", arousal)
valence = st.slider('Choose the valence:', 1,9)
st.write("🥹 Valence value is...", valence)
