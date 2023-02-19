import os.path
import random
import streamlit as st
import pandas as pd
import pickle


m3u_filepaths_file = 'playlists/streamlit.m3u8'
path = 'data/data.jsonl.pickle'
ESSENTIA_ANALYSIS_PATH = 'data/files_essentia_effnet-discogs.jsonl.pickle'


def load_essentia_analysis():
    return pandas.read_pickle(path)

# Leer archivo .pickle
with open(path, 'rb') as f:
    data = pickle.load(f)
#st.write(data)
primer_elemento = data[0]

df= pd.DataFrame(columns=["Filename", "Tempo", "Music style", "Instrumental", "Danceability", "Arousal", "Valence"])

for filename, d in primer_elemento.items():
    df.loc[len(df.index)] = [filename, d['Tempo'], d['Music style'], d['Instrumental'], d['Danceability'], d['Arousal'], d['Valence']]
   
audio_analysis_styles = df['Music style'].unique
st.write(audio_analysis_styles)

#st.dataframe(audio_analysis)

st.write('# Audio analysis playlists example')
st.write(f'Using analysis data from `{path}`.')

st.write('Loaded audio analysis for', len(df), 'tracks.')

style_select = st.multiselect('Select by style activations:', audio_analysis_styles)
if style_select:
    # Show the distribution of activation values for the selected styles.
    st.write(audio_analysis[style_select].describe())

    #style_select_str = ', '.join(style_select)
    #style_select_range = st.slider(f'Select tracks with', `{style_select_str}`)
    style_select_str = ", ".join([f"'{style}'" for style in styles])
    style_select_range = st.slider(f'Select tracks with {style_select_str}', 1, len(styles), (1, len(styles)))



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



