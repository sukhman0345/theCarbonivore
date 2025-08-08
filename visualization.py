import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from streamlit_lottie import st_lottie
import io

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

def show_visualization():
    st.title("📊 Visualization of Data")
    lottie_preprocessing = load_lottiefile("analytics.json")
    st_lottie(lottie_preprocessing, speed=1, reverse=False, loop=True, quality="high", width=300, height=300)

    # Load CSV directly
    try:
        df = pd.read_csv("the_Carbonivore.csv")
    except FileNotFoundError:
        st.error("⚠️ The file 'the_Catbonivore.csv' was not found. Please place it in the same directory as your Streamlit script.")
        return
    

    df = df.fillna(0)  
    st.subheader("Cleaned Null Values")
    st.write(df.isnull().sum())

    st.subheader("Data preview")
    st.dataframe(df)

    st.subheader("Summary Status")
    st.write(df.describe())

    st.markdown("---")
    st.subheader("Head Data")
    st.write(df.head())

    st.markdown("---")
    st.subheader("Tail Data")
    st.write(df.tail())

    st.markdown("---")
    st.subheader("Dataset Shape")
    st.write(df.shape)

    st.markdown("---")
    st.subheader("Dataset Info")
    buffer = io.StringIO()
    df.info(buf=buffer)
    st.text(buffer.getvalue())

    st.markdown("---")

    # Choropleth
    st.subheader("Choropleth: Total emissions by Area")
    fig = px.choropleth(
        df,
        locations="Area",
        locationmode="country names",
        color="total_emission",
        hover_name="Area",
        animation_frame="Year",
        title="Area-wise Total Emissions"
    )
    fig.update_layout(title_x=0.3, width=1100, height=700)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Line Chart
    st.subheader("Line Chart: Year Trend of Rice Cultivation Emission")
    fig = px.line(
        df,
        x="Year",
        y="Rice Cultivation",
        color="Area",
        title="Rice Cultivation Emissions over Time"
    )
    fig.update_layout(width=1100, height=700, title_x=0.2)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Bar Chart
    st.subheader("Bar Chart: Top 50 Areas by Fire-Based Emissions")
    fire_df = df[["Area", "Forest fires", "Savanna fires", "Fires in humid tropical forests"]].groupby("Area").mean().reset_index()
    fire_df["Total Emissions"] = fire_df[["Forest fires", "Savanna fires", "Fires in humid tropical forests"]].sum(axis=1)
    top_fire_df = fire_df.sort_values("Total Emissions", ascending=False).head(50)
    fire_melted = top_fire_df.drop(columns="Total Emissions").melt(id_vars="Area", var_name="Fire Type", value_name="Emissions")
    fig = px.bar(
        fire_melted,
        x="Area",
        y="Emissions",
        color="Fire Type",
        title="Top 10 Areas by Fire-Based Emissions",
        labels={"Emissions": "Emissions (Kilotons)"}
    )
    fig.update_layout(xaxis_tickangle=-45, width=1100, height=600, title_x=0.3)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Pie Chart
    st.subheader("Pie Chart: Industrial Emission Composition")
    year_df = df[df["Year"] == df["Year"].max()]
    ind_emissions = year_df[["IPPU", "On-farm Electricity Use", "Food Processing"]].sum()
    fig = px.pie(
        values=ind_emissions.values,
        names=ind_emissions.index,
        title=f"Industrial Emission Proportion in {year_df['Year'].max()}"
    )
    fig.update_layout(title_x=0.2, width=1000, height=500)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Heatmap
    st.subheader("HeatMap: Correlation with Total Emission")
    columns_to_check = [
        "total_emission",
        "Rural population",
        "Urban population",
        "Total Population - Male",
        "Total Population - Female",
        "On-farm energy use"
    ]
    corr_df = df[columns_to_check].corr()
    fig = px.imshow(corr_df, text_auto=True, title="Correlation with Total Emission", width=800, height=700)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Sunburst Chart
    st.subheader("SunBurst Chart: Gender-wise Population Distribution Across TOP 500 Areas")
    df["Total Population"] = df["Total Population - Male"] + df["Total Population - Female"]
    top500_df = df.sort_values("Total Population", ascending=False).head(500)
    population_melted = top500_df[["Area", "Total Population - Male", "Total Population - Female"]].melt(
        id_vars="Area",
        var_name="Gender",
        value_name="Population"
    )
    fig = px.sunburst(
        population_melted,
        path=["Area", "Gender"],
        values="Population",
        title="Top 500 Population Records by Area and Gender"
    )
    fig.update_layout(width=900, height=600, title_x=0.3)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Scatter Plot
    st.subheader("Scatter Plot: Top Mid Areas by Agricultural Emissions")
    df["Agri_total_Emission"] = (
        df["Pesticides Manufacturing"] +
        df["Fertilizers Manufacturing"] +
        df["Food Transport"]
    )
    top40_df = df.sort_values("Agri_total_Emission", ascending=True).head(3000).reset_index()
    fig = px.scatter(
        top40_df,
        x="Pesticides Manufacturing",
        y="Fertilizers Manufacturing",
        size="Food Transport",
        color="Area",
        hover_name="Area",
        title="Top 40 Areas by Agricultural Emissions",
        labels={
            "Pesticides Manufacturing": "Pesticides CO₂ (kt)",
            "Fertilizers Manufacturing": "Fertilizers CO₂ (kt)",
            "Food Transport": "Transport CO₂ (kt)"
        }
    )
    fig.update_layout(width=1000, height=500, title_x=0.3)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("<p style='text-align: center; color: gray;'>Made with ❤️ by sukhman.singh.codes</p>", unsafe_allow_html=True)
