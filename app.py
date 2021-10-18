import streamlit as st
import pretty_midi
import numpy
import pandas
import base64
from InputHandlingandDisplay import StoretheUpoldedFile
import music21
from PIL import Image
from MidiFeatures import GetMidFeatures,GetNameofAllInstruments,aGenerateMidFile,ConvertMiditoWave,DisplayGeneralFeatrues
import matplotlib.pyplot as plt
from BackEndPrediction import Prediction

if 'LocationofUploadedorGeneratedFile' not in st.session_state:
    st.session_state['LocationofUploadedorGeneratedFile'] = None
    
def PlayBackMusicFile(FileLocation):
  # This function generate st.audio widget, replay the contents found in FileLocation
  # full specficaion for this widget can be found https://docs.streamlit.io/en/stable/api.html
  # This function pass the file to the widget directly, the extension extracted only as it is 
  # needed by tehs second argument of the st.audio widget  
    audio_file = open(FileLocation, 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/'+FileLocation.split(".")[-1])
  
def DisplayMusicalNotes(music): 
  # This function is used to render the musical sheet of the argument music
  # it is adopted from the idea presented in https://groups.google.com/g/music21list/c/kjjt3QucVFM
  # it is simply cast the music into strings and then to image.   
  streamingNotes=str(music.write('lily.png'))
  image = Image.open(streamingNotes)
  #Then the st.image widget is used to display the image
  st.image(image, caption='Musical sheet')

def ChecktheCorrectnessofUploadedFile(uploaded_file):
    return
  

  
def PlotTempoChanges(InputFile):
  pm= pretty_midi.PrettyMIDI(InputFile)
  times, tempo_changes = pm.get_tempo_changes()
  fig, ax = plt.subplots()
  ax.plot(times, tempo_changes, '.')
  st.pyplot(fig)
  
def PlotPitchDistribution(InputFile):
  pm= pretty_midi.PrettyMIDI(InputFile)
  fig, ax = plt.subplots()
  plt.bar(numpy.arange(12), pm.get_pitch_class_histogram());
  ax.set_xticks(numpy.arange(12))
  ax.set_xticklabels(['C', '', 'D', '', 'E', 'F', '', 'G', '', 'A', '', 'B'])
  ax.set_xlabel('Musical Notes')
  ax.set_ylabel('Proportion')
  st.pyplot(fig)
  
 


#################################################### page layout start here #########################################################

#st.set_page_config(layout="wide") just change the page to wide mode
st.markdown(""" <style> #MainMenu {visibility: hidden;} footer {visibility: hidden;} </style> """, unsafe_allow_html=True)

st.title("Interactive Music Composition Using Artifical Intelligence")
st.header("                                                   ")
#One of the good widgets presented in streamlit is empty. it is a place holder so that we can consider it as template. 
MainPageDescription = st.empty() # The main canvas where the input/output is displayed 
MainPageDescription.write("""This is a beta version for an ambitious project aiming to promote the interactivity of 
         generate some musical pieces using Artificial Intelligence (AI) algorithms.
         Several AI models have been built and trained to match the variety of musical inputs ; furthermore, 
         the interface has been optimised to allow a user to add personal toutches and then to download the cratfed musical peices. 
         Wish this can aid the users to recogenise the potential rules that AI can play in art making. 
         Suggestions and comments are welcomed at: mdbaz01@gmail.com 
         """)
SubMainPageDescription=st.empty() # subcanvas where the inputs/outputs are handled 
Sub2MainPageDescription=st.empty() # same as above
Sub3MainPageDescription=st.empty() # same as above

########################################### The first step is listen to you ####################################################

with st.sidebar.expander("The first step is listen to you"):
    add_selectbox=st.radio("We can aid you to compete your piece or generate one for you: ",
                           ("Upload your audio files", "Generate musical Notes"),index=0)
    if(add_selectbox=="Upload your audio files"):
        uploaded_file = MainPageDescription.file_uploader("Uplod AudioFile Here or leave it blank if other options are selected",type=['mid'], accept_multiple_files=False) 
        if uploaded_file is not None:                              # Just to check that the user has its own input to the filed_uploader
            FileLocation=StoretheUpoldedFile(uploaded_file)
            duration,NotesNumbers,InstrumentsList= DisplayGeneralFeatrues(FileLocation)
            SubMainPageDescription.markdown('It is interesting truck of `'+str(duration)+'`'+' seconds '+
                                        'that comprises`'+str(NotesNumbers)+'`'+' notes '+
                                        'and played with the follwoing instrument(s)`'+str(InstrumentsList)+'`'+
                                        '**'+'Offcorse you can get more detailes using the follwoing:'+'**'
                                       )  
            # The options that a user can select amongest: 
            option = Sub2MainPageDescription.selectbox(label='',
                                                   options=("Plot Tempo changes",
                                                            "Plot pitch distributions",
                                                            "Render musical sheet, please wait it may take some times",
                                                            "Replay the uplodaed file, please wait it may take some times"))
            if (option=="Plot Tempo changes"):
                with Sub3MainPageDescription:
                    PlotTempoChanges(FileLocation)
            if (option=="Plot pitch distributions"):
                with Sub3MainPageDescription:
                    PlotPitchDistribution(FileLocation)
            if (option=="Render musical sheet, please wait it may take some times"):
                with Sub3MainPageDescription:
                    musictrack=music21.converter.parse(FileLocation)
                    DisplayMusicalNotes(musictrack)
            if (option=="Replay the uplodaed file, please wait it may take some times"):
                with Sub3MainPageDescription:
                    PlayBackMusicFile(FileLocation)
        
        if FileLocation is not None :
          st.session_state.LocationofUploadedorGeneratedFile = FileLocation
            
    if(add_selectbox=="Generate musical Notes"):
      FileLocation= None
      MainPageDescription.empty()
      SubMainPageDescription.empty()
      Sub2MainPageDescription.empty()
      Sub3MainPageDescription.empty()
      Tempos = [['Larghissimo', 0, 20], ['Grave', 20, 40], ['Slow', 40, 60],['Larghetto', 60, 66],['Adagio', 66, 76],['Adagietto', 70, 80],['Andante', 76, 108],
                ['Moderato',108, 120],['Allegro moderato', 112, 127],['Allegro', 120, 168],['Vivace', 168, 176],['Presto', 168, 200],['Prestissimo', 200, 176]]
      Tempos = pandas.DataFrame(Tempos, columns = ['TempoName', 'MinValue','MaxValue'])

      with MainPageDescription.container():
        Instruments = st.multiselect('Instruments you wish to use:',GetNameofAllInstruments(),default=['Electric Piano 1'])
        MinTempo, MaxTempo = st.select_slider('Select a range of tempos',options=Tempos['TempoName'],value=('Adagio', 'Moderato'))
        lenghtofMelody = st.slider('length of melody in seconds', 0, 30, 2)
        FileLocationofGeneraedMelody=aGenerateMidFile(MinTempo=MinTempo,MaxTempo=MaxTempo, lenghtofMelody=lenghtofMelody,listofInstruments=Instruments)
        
        PlayBackMusicFile(FileLocationofGeneraedMelody)
        PlotPitchDistribution(FileLocationofGeneraedMelody)
        #musictrack=music21.converter.parse(FileLocation)
        #DisplayMusicalNotes(musictrack)
        if FileLocationofGeneraedMelody is not None :
          st.session_state.LocationofUploadedorGeneratedFile = FileLocationofGeneraedMelody
        
with st.sidebar.expander("Here you can add personalise generation process:"): 
    if st.session_state.LocationofUploadedorGeneratedFile is not None: 
        InputShape=st.slider("Select the Inputshape, in sec",0,300,120) #here should be changed in accordnace with the inputs
        FrequecyDomain = st.checkbox('Using frequecy domain')
        PredictionHorizontal = st.number_input("Select the Prediction Horizonal, in seconds",min_value=60, max_value =300,value=120,step=10)
   
  #if (FileLocationofGeneraedMelody is None):
  #  SuppliedFileLocations=FileLocation
  #else:
  #  SuppliedFileLocations=FileLocationofGeneraedMelody
  #Trainingdataset=GetMidFeatures(SuppliedFileLocations)['pitch']
  #Prediction(Trainingdataset=Trainingdataset,modelname='StreamlitModel.h5',TrainingStep=InputShape,PredicitonHorizontal=PredictionHorizontal)      
        
        
      
      
        #MainPageDescription.write('It is interesting truck of'+a+ 'second'+
        #                          'It consists of'+b+'notes'+ 
        #                          'and played with the follwoing instrument(s)'+ c)
        
        
        #DisplayGeneralFeatrues(FileLocation)
        #with st.expander("Plot Tempo Changes"):
        #  PlotTempoChanges(FileLocation)
        #with st.expander("Plot Pitch Distrbution"):   
        #  PlotPitchDistribution(FileLocation)
        #with st.expander("Musical Sheet"):
        #  musictrack=music21.converter.parse(FileLocation)
        #  DisplayMusicalNotes(musictrack)
      
      
      
    #with st.expander("Harmony analysis"):
    #with st.expander("See explanation"):
    
    
    
  #    st.write(parsemidfile(uploaded_file))
      
    #FileLocation=StoretheUpoldedFile(uploaded_file)         # Store the file and get its location information 
    #PlayBackMusicFile(FileLocation) # pass the locaiona and extension to PlayBackMusicFile to replay its contents
    #ChecktheCorrectnessofUploadedFile(uploaded_file)
    #GetWavFeatures(ConvertMiditoWave(FileLocation),false)

















