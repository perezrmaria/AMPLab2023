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
#st.dataframe(df)
   
audio_analysis_styles = df['Music style'].unique()
#st.write(audio_analysis_styles)

#st.dataframe(audio_analysis)

st.write('# Audio analysis playlists example')
st.write(f'Using analysis data from `{path}`.')

st.write('Loaded audio analysis for', len(df), 'tracks.')

style_select = st.multiselect('Select by style activations:', audio_analysis_styles)
st.write(style_select[0])
#if style_select:
    # Show the distribution of activation values for the selected styles.
    #st.write(audio_analysis[style_select].describe())

    #style_select_str = ', '.join(style_select)
    #style_select_range = st.slider(f'Select tracks with', `{style_select_str}`)
    #style_select_str = ", ".join([f"'{style}'" for style in styles])
    #style_select_range = st.slider(f'Select tracks with {style_select_str}', 1, len(styles), (1, len(styles)))

if style_select:
    st.write('Audio with the following style(s):', style_select)
else:
    st.write("No style selected")

st.write('## ⌛️ Tempo')
tempo = st.slider('Choose a tempo', 60, 180, (60,180))
st.write("The following tempo is selected:", tempo)

st.write('## 🪗 Type of song: instrumental or vocal tune')
instrument = st.checkbox('🎙️ 🎻 Instrumental or vocal tune')

if instrument:
    st.write('Instrumental song is selected!🎺')
else:
    st.write('Vocal song is selected! 🎤')
    
st.write('## 🩰 Danceability')
danceability = st.slider('Choose how danceable you want the song to be:', 0, 3, (0,3))
st.write("Danceability value is...💃🏽", danceability)

st.write('## 🤨🤩 Arousal and valence')
arousal = st.slider('Choose the arousal:', 1,9, (1,9))
st.write("🐢 Arousal value is...", arousal)
valence = st.slider('Choose the valence:', 1,9, (1,9))
st.write("🥹 Valence value is...", valence)

df['Tempo'] = pd.to_numeric(df['Tempo'], errors='coerce')
df['Danceability'] = pd.to_numeric(df['Danceability'], errors='coerce')
df['Arousal'] = pd.to_numeric(df['Arousal'], errors='coerce')
df['Valence'] = pd.to_numeric(df['Valence'], errors='coerce')

max_tracks = st.number_input('Maximum number of tracks (0 for all):', value=0)
shuffle = st.checkbox('Random shuffle')


if st.button("RUN"):
    st.write('## 🔊 Results')
    #st.write(df.loc[0,'Tempo'], type(df.loc[0,'Tempo']), tempo[0], type(tempo[0]))
    result=df.loc[(df['Tempo'] >= tempo[0]) & (df['Tempo'] <= tempo[1])]
    result=result.loc[(result['Danceability'] >= danceability[0]) & (result['Danceability'] <= danceability[1])]
    if instrument:
        result = result.loc[result["Instrumental"] == 1]
    else:
        result = result.loc[result["Instrumental"] == 0]
    result = result.loc[(result["Arousal"] >= arousal[0]) & (result["Arousal"] <= arousal[1])]
    result = result.loc[(result["Valence"] >= valence[0]) & (result["Valence"] <= valence[1])]

    audio_analysis = result
    mp3s = list(audio_analysis.index)
        
    if style_select:
        #audio_analysis_query = audio_analysis.loc[mp3s].isin(style_select)
        styles = []
        for style in style_select:
            styles.append(style)
        st.write(styles)
        audio_analysis_query = audio_analysis.loc[audio_analysis["Music style"].isin(style_select)]
        st.write(audio_analysis["Music style"].isin(style_select))
        st.write(style_select)
        st.write(audio_analysis_query)
        #for style in style_select:
        #    fig, ax = plt.subplots()
        #    ax.hist(audio_analysis_query[style], bins=100)
        #    st.pyplot(fig)

        result = audio_analysis_query
        #for style in style_select:
            #result = result.loc[result[style] >= style_select_range[0]]
        #st.write(result)
        mp3s = result.index

    if max_tracks:
        mp3s = mp3s[:max_tracks]
        st.write('Using top', len(mp3s), 'tracks from the results.')

    if shuffle:
        random.shuffle(mp3s)
        st.write('Applied random shuffle.')

    # Store the M3U8 playlist.
    with open(m3u_filepaths_file, 'w') as f:
        # Modify relative mp3 paths to make them accessible from the playlist folder.
        mp3_paths = [os.path.join('..', mp3) for mp3 in mp3s]
        f.write('\n'.join(mp3_paths))
        st.write(f'Stored M3U playlist (local filepaths) to `{m3u_filepaths_file}`.')

    st.write('Audio previews for the first 10 results:')
    for mp3 in mp3s[:10]:
        st.audio(mp3, format="audio/mp3", start_time=0)

