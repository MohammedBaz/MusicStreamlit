import streamlit as st
st.title("Interactive Music Composition Using Artifical Intelligence")
SubtitleofThePage=st.empty()
DescriptionofThePage=st.empty()
PrevoiusNextFooter=st.empty()
if 'PageNumebr' not in st.session_state:
    st.session_state['PageNumebr'] = '1'
    
SubtitleofThePage.write("Warm Welcome from our app!")


