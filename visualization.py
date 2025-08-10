import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from streamlit_lottie import st_lottie
import io

# Load Lottie animation
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# Main visualization function
def show_visualization():
    st.set_page_config(page_title="Carbonivore Dashboard", layout="wide")
    st.title("📊 Visualization of Data")

    # Load animation
    lottie_preprocessing = load_lottiefile("analytics.json")
    st_lottie(
        lottie_preprocessing,
        speed=1,
        reverse=False,
        loop=True,
        quality="high",
        width=300,
        height=300
    )

    # Load CSV
    DATA_FILE = "cleaned_data.csv"
    try:
        df = pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        st.error(f"⚠️ The file '{DATA_FILE}' was not found. Please place it in the same directory as your Streamlit script.")
        return
    
    st.markdown("---")


    # Sidebar Filters
    st.sidebar.header("🔍 Filter Options")
    area_list = df["Area"].unique().tolist()
    selected_areas = st.sidebar.multiselect("Select Area(s)", area_list, default=area_list)

    year_list = sorted(df["Year"].unique())
    selected_years = st.sidebar.multiselect("Select Year(s)", year_list, default=year_list)

    # Apply filters
    filtered_df = df[df["Area"].isin(selected_areas) & df["Year"].isin(selected_years)]

    # Data Overview
    st.subheader("Cleaned Null Values")
    st.write(filtered_df.isnull().sum())

    st.subheader("Data Preview")
    st.dataframe(filtered_df)

    st.subheader("Summary Statistics")
    st.write(filtered_df.describe())

    st.subheader("Head & Tail")
    st.write("🔼 Head")
    st.write(filtered_df.head())
    st.write("🔽 Tail")
    st.write(filtered_df.tail())

    st.subheader("Dataset Shape")
    st.write(filtered_df.shape)

    st.subheader("Dataset Info")
    buffer = io.StringIO()
    filtered_df.info(buf=buffer)
    st.text(buffer.getvalue())

    st.markdown("---")
    df.isnull().sum()
    st.markdown("---")
    # Choropleth
    st.subheader("🌍 Choropleth: Total Emissions by Area")
    fig = px.choropleth(
        filtered_df,
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
    st.subheader("📈 Line Chart: Rice Cultivation Emissions Over Time")
    fig = px.line(
        filtered_df,
        x="Year",
        y="Rice Cultivation",
        color="Area",
        title="Rice Cultivation Emissions over Time"
    )
    fig.update_layout(width=1100, height=700, title_x=0.2)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Fire-Based Emissions Bar Chart
    st.subheader("🔥 Bar Chart: Top 50 Areas by Fire-Based Emissions")
    fire_df = filtered_df[["Area", "Forest fires", "Savanna fires", "Fires in humid tropical forests"]]\
        .groupby("Area").mean().reset_index()
    fire_df["Total Emissions"] = fire_df[["Forest fires", "Savanna fires", "Fires in humid tropical forests"]].sum(axis=1)
    top_fire_df = fire_df.sort_values("Total Emissions", ascending=False).head(50)
    fire_melted = top_fire_df.drop(columns="Total Emissions")\
        .melt(id_vars="Area", var_name="Fire Type", value_name="Emissions")

    fig = px.bar(
        fire_melted,
        x="Area",
        y="Emissions",
        color="Fire Type",
        title="Top 50 Areas by Fire-Based Emissions",
        labels={"Emissions": "Emissions (Kilotons)"}
    )
    fig.update_layout(xaxis_tickangle=-45, width=1100, height=600, title_x=0.3)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Pie Chart
    st.subheader("🏭 Pie Chart: Industrial Emission Composition")
    if not filtered_df.empty:
        year_df = filtered_df[filtered_df["Year"] == filtered_df["Year"].max()]
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
    st.subheader("🌡️ HeatMap: Correlation with Total Emission")
    columns_to_check = [
        "total_emission",
        "Rural population",
        "Urban population",
        "Total Population - Male",
        "Total Population - Female",
        "On-farm energy use"
    ]
    corr_df = filtered_df[columns_to_check].corr()
    fig = px.imshow(corr_df, text_auto=True, title="Correlation with Total Emission", width=800, height=700)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Sunburst Chart
    st.subheader("🌞 SunBurst Chart: Gender-wise Population Distribution Across TOP 500 Areas")
    filtered_df["Total Population"] = filtered_df["Total Population - Male"] + filtered_df["Total Population - Female"]
    top500_df = filtered_df.sort_values("Total Population", ascending=False).head(500)
    population_melted = top500_df[["Area", "Total Population - Male", "Total Population - Female"]]\
        .melt(id_vars="Area", var_name="Gender", value_name="Population")

    fig = px.sunburst(
        population_melted,
        path=["Area", "Gender"],
        values="Population",
        title="Top 500 Population Records by Area and Gender"
    )
    fig.update_layout(width=900, height=600, title_x=0.3)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Stacked Bar Chart
    st.subheader("🏘️ Bar Chart: Top 50 Areas by Rural vs Urban Population")
    df_grouped = df.groupby("Area")[["Rural population", "Urban population"]].sum().reset_index()
    df_grouped["total"] = df_grouped["Rural population"] + df_grouped["Urban population"]
    df_top = df_grouped.sort_values(by="total", ascending=False).head(50)

    fig = px.bar(
        df_top,
        x="Area",
        y=["Rural population", "Urban population"],
        barmode="stack",
        title="Top 50 Areas by Rural vs Urban Population",
        labels={"value": "Population", "Area": "Area/Region"},
    )
    fig.update_layout(height=700, title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Scatter Plot
    st.subheader("🚜 Scatter Plot: Top Mid Areas by Agricultural Emissions")
    filtered_df["Agri_total_Emission"] = (
        filtered_df["Pesticides Manufacturing"] +
        filtered_df["Fertilizers Manufacturing"] +
        filtered_df["Food Transport"]
    )
    top40_df = filtered_df.sort_values("Agri_total_Emission", ascending=True).head(3000).reset_index()

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
    st.markdown(
        "<p style='text-align: center; color: gray;'>Made with ❤️ by sukhman.singh.codes</p>",
        unsafe_allow_html=True
    )

# # Run the app
# if __name__ == "__main__":
#     show_visualization()