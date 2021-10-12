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

col1, col2, col3,col4, col5, col6,col7, col8, col9,col10 = st.columns(10)
col10.button('Click')
    
st.markdown("""div.stButton > button:first-child {
background-color: #00cc00;color:white;font-size:20px;height:3em;width:50%;border-radius:10px 10px 10px 10px;}""", unsafe_allow_html=True)
st.button("the notice you want to show")
