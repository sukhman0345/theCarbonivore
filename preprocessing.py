import streamlit as st
import pandas as pd
import os
import json
from streamlit_lottie import st_lottie

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

def show_preprocessing():
    st.title("🧼 Pre-processing Overview")
    lottie_preprocessing = load_lottiefile("data_preprocessing.json")
    st_lottie(lottie_preprocessing, speed=1, reverse=False, loop=True, quality="high", width=300)

    st.markdown("---")

    try:
        df = pd.read_csv("the_Carbonivore.csv")

        st.subheader("🔎 First 5 Rows of Data")
        st.dataframe(df.head())

        st.markdown("---")
        
        st.subheader("🔎 last 5 Rows of Data")
        st.dataframe(df.tail())

        st.markdown("---")

        st.subheader("📏 Duplicate Rows")
        st.write(f"Total Duplicates: {df.duplicated().sum()}")

        st.markdown("---")

        st.subheader("🚨 Null Value Count")
        st.dataframe(df.isnull().sum().reset_index().rename(columns={0: 'Missing Count', 'index': 'Column'}))

        st.markdown("---")

        st.subheader("📊 Data Types & Non-Null Count")
        summary = pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.values,
            "Non-Null Count": df.notnull().sum().values
        })
        st.dataframe(summary)

        st.markdown("---")

         # Footer
        st.markdown("""
        <p style="text-align: center; color: gray;">
            Made with ❤️ by sukhman.singh.codes
        </p>
    """, unsafe_allow_html=True)


        #st.success("✅ Pre-processing successfully displayed.")
    except FileNotFoundError:
        st.error("⚠️ 'Agrofood_co2_emission.csv' file not found.")
        st.write("📂 Current directory files:", os.listdir())
