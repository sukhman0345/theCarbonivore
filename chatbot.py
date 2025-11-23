import streamlit as st
import pandas as pd
import google.generativeai as genai

genai.configure(api_key=st.secrets["google"]["apikey"])
model = genai.GenerativeModel("gemini-2.5-flash-lite")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("the_Carbonivore.csv")

df = load_data()

# Chatbot logic
def handle_query(query):
    query_lower = query.lower()

    # Structured dataset answers
    if "rows" in query_lower or "shape" in query_lower or "size" in query_lower:
        rows, cols = df.shape
        return f" Your dataset has {rows} rows and {cols} columns."

    elif "columns" in query_lower or "features" in query_lower:
        return f" The dataset has {df.shape[1]} columns:\n\n{', '.join(df.columns)}"

    elif "missing" in query_lower:
        missing = df.isnull().sum()
        missing = missing[missing > 0]
        if missing.empty:
            return " There are no missing values in the dataset."
        return f" Missing values per column:\n\n{missing.to_string()}"
    elif "describe" in query_lower or "summary" in query_lower:
        return " Statistical summary:\n\n" + df.describe().to_string()

    elif "correlation" in query_lower:
        corr = df.corr(numeric_only=True)
        return " Correlation matrix:\n\n" + corr.to_string()

    elif "project" in query_lower or "overview" in query_lower:
        return " This project analyzes CO₂ emissions using the_Carbonivore.csv dataset to uncover environmental patterns."

    elif "insight" in query_lower or "conclusion" in query_lower:
        return " Higher agricultural activity and fuel transport are correlated with increased CO₂ emissions."

    elif "show data" in query_lower or "dataset" in query_lower:
        return " Here's a preview of your dataset:\n\n" + df.head().to_string()
    # Fallback: Gemini for open-ended questions
    else:
        try:
            response = model.generate_content(
                f"""
                The user asked: {query}
                Dataset columns: {', '.join(df.columns)}

                You are a helpful data science tutor.
                - Explain in simple terms.
                - Use examples if relevant.
                - Keep it beginner-friendly.
                """
            )
            return response.text
        except Exception as e:
            return f" Gemini API error: {str(e)}"

def show_chatbot():
    st.set_page_config(page_title="CO₂ Emission Chatbot", layout="centered")

    st.markdown("<h1> CO₂ Emission Project Chatbot</h1>", unsafe_allow_html=True)
    st.markdown("<p>Ask me anything about the_Carbonivore.csv dataset!</p>", unsafe_allow_html=True)

    user_input = st.text_input(" Your question:")

    if user_input:
        response = handle_query(user_input)
        st.markdown(f"<div class='chatbox'>{response}</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("""
        <p style="text-align: center; color: gray;">
            Made with ❤️ by sukhman.singh.codes
        </p>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_chatbot()