import streamlit as st
from InputHandlingandDisplay import StoretheUpoldedFile
if 'PageNumebr' not in st.session_state:
    st.session_state['PageNumebr'] = '1'

st.title("Interactive Music Composition Using Artifical Intelligence")

SubtitleofThePage=st.empty()
DescriptionofThePage=st.empty() 
PrevoiusNextFooter=st.empty()    

def WelcomPage():
    SubtitleofThePage.st.write("Warm Welcome from our app!")
    DescriptionofThePage.st.write(write("""This is a beta version for an ambitious project aiming to promote the interactivity of 
         generate some musical pieces using Artificial Intelligence (AI) algorithms.
         Several AI models have been built and trained to match the variety of musical inputs ; furthermore, 
         the interface has been optimised to allow a user to add personal toutches and then to download the cratfed musical peices. 
         Wish this can aid the users to recogenise the potential rules that AI can play in art making. Source code is at:
         https://github.com/MohammedBaz/MusicStreamlit/blob/main/BackEndPrediction.py  
         """)
    with PrevoiusNextFooter:
        col1, col2, col3,col4, col5, col6,col7, col8, col9,col10 = st.columns(10)
        col10.button('Let us strat',key="next", on_click=IncreasePageNumber)
                                  
def IncreasePageNumber():
    if  (st.session_state.PageNumebr=='1'):
        st.session_state.PageNumebr='2'
    elif(st.session_state.PageNumebr=='2'):
        st.session_state.PageNumebr='3'
    elif(st.session_state.PageNumebr=='3'):
        st.session_state.PageNumebr='4'
    else:
        st.session_state.PageNumebr='PositiveInf'
    st.write(st.session_state.PageNumebr)
    
def DecreasePageNumber():
    if  (st.session_state.PageNumebr=='4'):
        st.session_state.PageNumebr='3'
    elif(st.session_state.PageNumebr=='3'):
        st.session_state.PageNumebr='2'
    elif(st.session_state.PageNumebr=='2'):
        WelcomPage()
        st.session_state.PageNumebr='1'                          
    else:
        st.session_state.PageNumebr='NegtiveInf'
    st.write(st.session_state.PageNumebr)    
            
WelcomPage() 
                                  
#with PrevoiusNextFooter:
#    col1, col2, col3,col4, col5, col6,col7, col8, col9,col10 = st.columns(10)
#    col10.button('Next',key="next", on_click=IncreasePageNumber)
#    col1.button('Prevoius',key="Prevoius", on_click=DecreasePageNumber)  


