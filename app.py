import streamlit as st
st.title("Interactive Music Composition Using Artifical Intelligence")
SubtitleofThePage=st.empty()
DescriptionofThePage=st.empty()
PrevoiusNextFooter=st.empty()
if 'PageNumebr' not in st.session_state:
    st.session_state['PageNumebr'] = '1'
    
SubtitleofThePage.write("Warm Welcome from our app!")
DescriptionofThePage.write("""This is a beta version for an ambitious project aiming to promote the interactivity of 
         generate some musical pieces using Artificial Intelligence (AI) algorithms.
         Several AI models have been built and trained to match the variety of musical inputs ; furthermore, 
         the interface has been optimised to allow a user to add personal toutches and then to download the cratfed musical peices. 
         Wish this can aid the users to recogenise the potential rules that AI can play in art making. Source code is at:
         https://github.com/MohammedBaz/MusicStreamlit/blob/main/BackEndPrediction.py  
         """)
with PrevoiusNextFooter:
    col1, col2, col3,col4, col5, col6,col7, col8, col9,col10 = st.columns(10)
    go=col10.button('Go',key="go")

if(go):
    st.session_state.PageNumebr='2'
    SubtitleofThePage.write("The fist step is to listen to you")
    add_selectbox=DescriptionofThePage.radio("you can upload your audio samples or use ours:",
                                             ("Upload some audio files", "Use some random Notes", "Use pretrainned Audios"),index=1)
    if(add_selectbox=="Upload some audio files"):       
        uploaded_file = DescriptionofThePage.file_uploader("Uplod AudioFile Here or leave it blank if other options are selected",
                                     type=['wav','mp3','mid'], accept_multiple_files=False, key=123456) 
        if uploaded_file is not None:                               # Just to check that the user has its own input to the filed_uploader
            if (uploaded_file.name.endswith('wav')):              # if the file is not mid, i.e., it is .wav or.mp3 then
                FileLocation=StoretheUpoldedFile(uploaded_file)         # Store the file and get its location information 
                FileType=FileLocation.split(".")[-1]
                PlayBackMusicFile(FileLocation,FileLocation.split(".")[-1]) # pass the locaiona and extension to PlayBackMusicFile to replay its contents
    with PrevoiusNextFooter:
        col1, col2, col3,col4, col5, col6,col7, col8, col9,col10 = st.columns(10)
        col10.button('Next',key="MoveToAnalysis")
        col1.button('Prevoius',key="ReturnToHome")


