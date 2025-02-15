import streamlit as st
import requests
from PIL import Image
import io

# API URL for Ingredient Images (TheMealDB)
MEALDB_INGREDIENT_IMAGE_URL = "https://www.themealdb.com/images/ingredients/"

# Function to fetch ingredient image
def get_ingredient_image(ingredient_name):
    return f"{MEALDB_INGREDIENT_IMAGE_URL}{ingredient_name}.png"

# ---- Streamlit UI ----
st.title("🥗 AI-Powered Recipe Generator")
st.write("Upload an image of your leftover food, and we'll generate a delicious recipe!")

# Upload Image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Mock API Call to get detected ingredients
    detected_ingredients = ["Tomato", "Onion", "Cheese"]

    st.subheader("📝 Identified Ingredients:")
    for ingredient in detected_ingredients:
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(get_ingredient_image(ingredient), width=80)
        with col2:
            st.write(f"**{ingredient}**")
