import streamlit as st
from InputHandlingandDisplay import StoretheUpoldedFile
if 'PageNumebr' not in st.session_state:
    st.session_state['PageNumebr'] = '1'

TitleofThePage=st.empty()
DescriptionofThePage=st.empty() 
PrevoiusNextFooter.empty()    
    
def IncreasePageNumber():
    if  (st.session_state.PageNumebr=='1'):
        st.session_state.PageNumebr='2'
        TakeUserInputPage.app()
    elif(st.session_state.PageNumebr=='2'):
        st.session_state.PageNumebr='3'
        AnalysisUserInput.app()
    elif(st.session_state.PageNumebr=='3'):
        st.session_state.PageNumebr='4'
        GetResults.app()
    else:
        st.session_state.PageNumebr='PositiveInf'
    st.write(st.session_state.PageNumebr)
    
def DecreasePageNumber():
    if  (st.session_state.PageNumebr=='4'):
        st.session_state.PageNumebr='3'
    elif(st.session_state.PageNumebr=='3'):
        st.session_state.PageNumebr='2'
    elif(st.session_state.PageNumebr=='2'):
        st.session_state.PageNumebr='1'    
    else:
        st.session_state.PageNumebr='NegtiveInf'
    st.write(st.session_state.PageNumebr)    
            
            
col1, col2, col3,col4, col5, col6,col7, col8, col9,col10 = st.columns(10)
PrevoiusNextFooter.col10.button('Next',key="next", on_click=IncreasePageNumber)
PrevoiusNextFooter.col1.button('Prevoius',key="Prevoius", on_click=DecreasePageNumber)  


