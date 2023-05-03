import streamlit as st
from src.engine import Chat
import time
def text(text, tag='h1', align='left', color=None):
    assert tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'strong', 'u', 'i', 'p'], "Invalid Tag"
    if color is None:
        st.markdown(f"<{tag} style='text-align: {align}'>{text}</{tag}>", unsafe_allow_html=True)
    else:
        st.markdown(f"<{tag} style='text-align: {align}; color: {color}'>{text}</{tag}>", unsafe_allow_html=True)

def header():
    st.title("NikhilLinguist")
    st.markdown("Made by **[Nikhil](https://twitter.com/nikhil__xb)** 🤗")
    text("Lets's brew some awesome conversation & let's see how better Nikhil knows you!😎")
    st.caption("Please not it might give some irrelevant answers, since it has been trained on a limited corpus")


def app():
    while True:
        user_input= st.text_input("You:", "")
        start= time.time()
        chat= []
        HISTORY= []
        if user_input:
            chat.append(("You", user_input))
            prompt= user_input
            try:
                answer, HISTORY = model.lets_prompt(prompt, HISTORY)
                chat.append(("NikhilGPT",answer ))
            except BaseException as e:
                text(f"Error occured-> {e}",
                     'strong',
                     'left',
                     'red')
        for sender, message in chat:
            if sender == "You":
                css_class= "you-message"
            else: 
                css_class= "nikhilgpt"
            st.markdown(f'<div class="{css_class}"><p>{sender}: {message}</p></div>', unsafe_allow_html= True)
        if st.button("STOP!"):
            time_taken= time.time()-start
            st.caption(f"(Chat Duration= {time_taken:.4f} seconds)")
            break

if __name__=="__main__":
    st.set_page_config(page_title= "NikhilLinguist - By Nikhil")
    model= Chat()
    header()
    app()




    


        