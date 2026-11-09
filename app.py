
import streamlit as st

st.set_page_config(
    page_title="Real Gas Property Predictor",
    page_icon="⚗️",
    layout="wide"
)

st.title("Real Gas Property Predictor")

st.subheader(
    "Prediction of PVT Behaviour of Real Gases "
    "Using Cubic Equations of State"
)

st.write("Select an Equation of State below.")

eos = st.selectbox(
    "Choose Equation of State",
    [
        "van der Waals",
        "Redlich-Kwong",
        "Soave-Redlich-Kwong",
        "Peng-Robinson"
    ]
)

st.success(f"Selected Equation: {eos}")

st.write("Our thermodynamic calculation software is ready for development.")
