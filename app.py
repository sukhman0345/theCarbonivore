import streamlit as st
import time
import json
from streamlit_lottie import st_lottie
from signin import signin
from signup import signup
from menuBar import main_app

# Function to load local Lottie JSON
def load_lottiefile(filepath: str):
    with open(filepath, "r") as file:
        return json.load(file)

# Splash screen
def splash_screen():
    lottie_data = load_lottiefile("splash.json")
    st_lottie(lottie_data, speed=1, loop=True, quality="high")
    st.markdown("<h2 style='text-align:center;'>Loading The Carbonivore...</h2>", unsafe_allow_html=True)

# Main app logic
def main():
    if "splash_start" not in st.session_state:
        st.session_state.splash_start = time.time()

    # Show splash for 2 seconds
    if time.time() - st.session_state.splash_start < 2:
        splash_screen()
    else:
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
