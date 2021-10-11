import streamlit as st
import pretty_midi
import numpy as np 
import pandas
import os
import base64
from typing import List

st.title("AIMC")
st.header("Artificial Intelligence Music Composer")
from BackEndPrediction import Prediction
Trainingdataset=[]
#uploaded_file = st.file_uploader("upload your mid file or leave blank for random startup", type="mid") #Add file uploader to take the user's input. limited to .png files only

import pydub
from pathlib import Path
uploaded_file = st.file_uploader("upload", type=['wav'], accept_multiple_files=False, key=123456)
if uploaded_file is not None:
    audio = uploaded_file.read()
    st.audio(audio, format='audio/wav')

