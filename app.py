import streamlit as st
import json
import time
from streamlit_lottie import st_lottie
from signin import signin
from signup import signup
from menuBar import main_app

# Load local Lottie file
def load_lottiefile(filepath: str):
    with open(filepath, "r") as file:
        return json.load(file)

# Splash screen
def splash_screen():
    lottie_data = load_lottiefile("splash.json")
    st_lottie(lottie_data, speed=1, loop=True, quality="high")
    st.markdown("<h2 style='text-align:center;'>Loading The Carbonivore...</h2>", unsafe_allow_html=True)
    st.markdown("""
        <p style="text-align: center; color: gray;">
            Made with ❤️ by sukhman.singh.codes
        </p>
    """, unsafe_allow_html=True)
    time.sleep(2)  # Show for 2 seconds
    st.session_state.splash_done = True
    st.rerun()  # Move on automatically

def main():
    if "splash_done" not in st.session_state:
        splash_screen()

    # After splash, go to app
    if st.session_state.get('user'):
        main_app()
    else:
        st.sidebar.title("Signin/Signup")
        auth_choice = st.sidebar.radio("Select", ["Sign In", "Sign Up"])
        if auth_choice == "Sign In":
            signin()
        else:
            signup()

if __name__ == "__main__":
    main()
