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
   
st.write(df['Music style'].unique)

#st.dataframe(audio_analysis)

st.write('# Audio analysis playlists example')
st.write(f'Using analysis data from `{path}`.')

st.write('Loaded audio analysis for', len(df), 'tracks.')

style_select = st.multiselect('Select by style activations:', audio_analysis_styles)
if style_select:
    # Show the distribution of activation values for the selected styles.
    st.write(audio_analysis[style_select].describe())

    style_select_str = ', '.join(style_select)
    style_select_range = st.slider(f'Select tracks with `{style_select_str})


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



if st.button("RUN"):
    st.write('## 🔊 Results')
    mp3s = list(df.index)

    if style_select:
        audio_analysis_query = audio_analysis.loc[mp3s][style_select]

        #for style in style_select:
        #    fig, ax = plt.subplots()
        #    ax.hist(audio_analysis_query[style], bins=100)
        #    st.pyplot(fig)

        result = audio_analysis_query
        for style in style_select:
            result = result.loc[result[style] >= style_select_range[0]]
        st.write(result)
        mp3s = result.index

    if style_rank:
        audio_analysis_query = audio_analysis.loc[mp3s][style_rank]
        audio_analysis_query['RANK'] = audio_analysis_query[style_rank[0]]
        for style in style_rank[1:]:
            audio_analysis_query['RANK'] *= audio_analysis_query[style]
        ranked = audio_analysis_query.sort_values(['RANK'], ascending=[False])
        ranked = ranked[['RANK'] + style_rank]
        mp3s = list(ranked.index)

        st.write('Applied ranking by audio style predictions.')
        st.write(ranked)

    if max_tracks:
        mp3s = mp3s[:max_tracks]
        st.write('Using top', len(mp3s), 'tracks from the results.')

    if shuffle:
        random.shuffle(mp3s)
        st.write('Applied random shuffle.')
