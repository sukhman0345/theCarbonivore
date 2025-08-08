import streamlit as st
from firebase_config import auth
from streamlit_lottie import st_lottie
import json

# Load Lottie animation from file
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

#  Sign-in function
def signin():
    # Layout: Two columns
    col1, col2 = st.columns([1, 1])

    with col1:
        st.title("🔐 Sign In")
        email = st.text_input("📧 Email").strip()
        password = st.text_input("🔒 Password", type="password").strip()

        # Initialize session state flags
        if "login_attempted" not in st.session_state:
            st.session_state["login_attempted"] = False
        if "login_successful" not in st.session_state:
            st.session_state["login_successful"] = False

        # Buttons: Login and Forgot Password
        btn_col1, btn_col2 = st.columns([2, 1])
        login_clicked = btn_col1.button("🔓 Login")
        forgot_clicked = btn_col2.button("❔ Forgot Password?")

        # Handle login attempt
        if login_clicked:
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                st.session_state["user"] = user
                st.session_state["login_successful"] = True
                st.session_state["login_attempted"] = True
                st.success("✅ Login successful! Redirecting...")
                st.rerun()
            except Exception as e:
                st.session_state["login_successful"] = False
                st.session_state["login_attempted"] = True
                st.error(f"❌ Login failed: {e}")

        # Tip if login failed
        if st.session_state["login_attempted"] and not st.session_state["login_successful"]:
            st.info("💡 Tip: Check your email or password again, or sign up if you haven't.")

        #  Handle password reset
        if forgot_clicked:
            if email:
                try:
                    auth.send_password_reset_email(email)
                    st.info("📧 Password reset email sent.")
                except Exception as e:
                    st.error(f"❌ Error sending reset email: {e}")
            else:
                st.warning("⚠️ Please enter your email to reset password.")

    with col2:
        # Display Lottie animation
        lottie_signin = load_lottiefile("signin.json")
        st_lottie(lottie_signin, speed=1, reverse=False, loop=True, quality="high")