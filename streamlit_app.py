import streamlit as st
import pandas as pd
import pickle
import os
import yaml
import requests

API_URL = "https://fast-317097237537.europe-west1.run.app/predict"

st.title("🦠 Microorganisms Classification")

st.info("This app allows you to classify microorganisms based on their features.")

model = pickle.load(open('models/microbe_model.pkl', 'rb'))
df = pd.read_csv('data/microbes.csv')
with open('static/microorganism.yaml', 'r') as file:
    microbe_data = yaml.safe_load(file)

features = {
    'Area': 'Total area of the microorganism',
    'Perimeter': 'Length of the boundary of the microorganism',
    'MajorAxisLength': 'Length of the major axis of the ellipse that best fits the microorganism',
    'MinorAxisLength': 'Length of the minor axis of the ellipse that best fits the microorganism'
}
images_path = 'static/img'
image_files = [f for f in os.listdir(images_path) if f.endswith('.png')][:10]

cols = st.columns(5)
for i, image_file in enumerate(image_files):
    row = i // 5
    col = i % 5
    with cols[col]:
        st.image(os.path.join(images_path, image_file), caption=image_file.replace('.png',''))


with st.form("microbe_form"):
    st.write("Enter microorganism features:")
    
    input_values = {}
    col1, col2 = st.columns(2)
    
    for i, feature in enumerate(features):
        with col1 if i % 2 == 0 else col2:
            input_values[feature] = st.number_input(
                label=feature,
                value=float(df[feature].mean()),
                help=f"Enter value for {features[feature]}"
            )
    
    submitted = st.form_submit_button("Classify")
    
if submitted:
    response = requests.post(API_URL, json=input_values)
    prediction = response.json()
    microbe_name = prediction['class_predicted'][0]
    st.balloons()
    st.success(f"**Predicted Microorganism:** {microbe_name}")
    st.subheader(f"This is a {microbe_name} !")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(f"{images_path}/{microbe_name}.png", caption=microbe_name)
    
    with col2:
        microbe_info = microbe_data['microorganisms'].get(microbe_name, {})
        if microbe_info:
            st.markdown("### Microorganism Information")
            st.markdown(f"""
                - **Type:** {microbe_info.get('type', 'N/A')}
                - **Habitat:** {microbe_info.get('habitat', 'N/A')}
                - **Description:** {microbe_info.get('description', 'N/A')}
            """)
