import streamlit as st
from streamlit_lottie import st_lottie
import json
from firebase_config import auth

def load_lottiefile(filepath: str):
  with open(filepath, "r") as f:
    return json.load(f) 

def signup():
# Layout: Two columns
  col1, col2 = st.columns([1,1]) 
  
  with col1: 
   st.title("📝 Sign Up")
   email = st.text_input("📧 Email")
   password = st.text_input("🔒 Password", type="password")
   confirm = st.text_input("🔁 Confirm Password", type="password")

  if st.button("🧷 Create Account"):
    if password != confirm:
      st.error(" Passwords do not match.")
    else:
      try:
        auth.create_user_with_email_and_password(email, password)
        st.success("🎉 Account created successfully. Please sign in.")
      except Exception as e:
        st.error(f" Error: {e}")
  with col2:
    lottie_signup = load_lottiefile("signup.json")
    st_lottie(lottie_signup, speed=1, reverse=False, loop=True, quality="high")


