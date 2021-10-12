import streamlit as st
from InputHandlingandDisplay import StoretheUpoldedFile

st.title("Interactive Music Composition Artifical Intelligence")
WhichStep = st.empty()
WhichStep.write("Step1: How would you like to start")
Contents = st.empty()
add_selectbox=WhichStep.radio("you can upload your audio samples or use ours:",
                                 ("Upload some audio files", "Use some random Notes", "Use pretrainned Audios"),index=1)
if(add_selectbox=="Upload some audio files"):
    uploaded_file = st.file_uploader("Uplod AudioFile Here or leave it blank if other options are selected",
                                     type=['wav','mp3','mid'], accept_multiple_files=False, key=123456) 
    if uploaded_file is not None:                               # Just to check that the user has its own input to the filed_uploader
        if (uploaded_file.name.endswith('wav')):              # if the file is not mid, i.e., it is .wav or.mp3 then
            FileLocation=StoretheUpoldedFile(uploaded_file)         # Store the file and get its location information 
            FileType=FileLocation.split(".")[-1]
            #PlayBackMusicFile(FileLocation,FileLocation.split(".")[-1]) # pass the locaiona and extension to PlayBackMusicFile to replay its contents
            from WaveFeatures import GetWavFeatures
            WavFeatures=GetWavFeatures(FileLocation)
            st.write(WavFeatures['NumberofSamples'])
        elif (uploaded_file.name.endswith('mp3')):
            FileLocation=StoretheUpoldedFile(uploaded_file)
            FileType=FileLocation.split(".")[-1]
            #PlayBackMusicFile(FileLocation,FileLocation.split(".")[-1])

col1, col2, col3 = st.columns(3)
if col2.button('Click'):
    st.write('hello')
st.button("Next")
button_alignment="""<style> #the-title {text-align: left}</style>"""
st.markdown(button_alignment, unsafe_allow_html=True)
