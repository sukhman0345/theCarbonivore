import streamlit as st
from datetime import datetime
from streamlit_lottie import st_lottie
import json
import sqlite3

# Function to load Lottie animation from file
def load_lottiefile(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

# Main function to display the Get in Touch form
def get_in_touch():
    # Load Lottie animation
    lottie_contact = load_lottiefile("contact us.json")
    st_lottie(
        lottie_contact,
        speed=1,
        reverse=False,
        loop=True,
        quality="high",
        height=300,
    )

    # Page title
    st.title("Get in Touch")

    # Input fields
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    message = st.text_input("Your Message")

    # Dropdown for feedback type
    feedback_type = st.selectbox(
        "Type of Feedback",
        ["Suggestion", "Bug Report", "Compliment", "Question", "Others"]
    )

    # Submit button logic
    if st.button("Submit"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current timestamp

        # Connect to SQLite database (creates if doesn't exist)
        conn = sqlite3.connect("contacts.db")
        c = conn.cursor()

        # Create table if not exists
        c.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                name TEXT,
                email TEXT,
                message TEXT,
                feedback_type TEXT,
                timestamp TEXT
            )
        ''')

        # Insert data into table
        c.execute(
            "INSERT INTO contacts (name, email, message, feedback_type, timestamp) VALUES (?, ?, ?, ?, ?)",
            (name, email, message, feedback_type, timestamp)
        )

        # Commit changes and close connection
        conn.commit()
        conn.close()

        # Success message
        st.success("Thanks for your feedback! It's been recorded.")

        # Footer
        st.markdown("""
            <p style="text-align: center; color: gray;">
                Made with ❤️ by sukhman.singh.codes
            </p>
        """, unsafe_allow_html=True)

# Call the function to run the form
if __name__ == "__main__":
 get_in_touch()
