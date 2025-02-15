import streamlit as st
import requests
from PIL import Image
import io
import os

# ---- APP CONFIGURATION ----
st.set_page_config(page_title="Kitchen Copilot", page_icon="images/KitchenCopilot_Logo.png", layout="wide")

# ---- FORCE LIGHT THEME (REMOVE BLACK ELEMENTS) ----
st.markdown("""
    <style>
        /* White background for entire app */
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #FAF9F6 !important;
            color: #333 !important;
        }
        /* Ensure text fields and dropdowns are white */
        input[type="text"], select, .stTextInput>div>div>input, .stSelectbox>div>div>select {
            background-color: #FFFFFF !important;
            color: #333 !important;
            border: 1px solid #CCC !important;
            border-radius: 8px;
            padding: 10px;
            width: 100%;
        }
        /* Style buttons */
        .stButton>button {
            background-color: #FF6F3C !important;
            color: white !important;
            font-size: 16px;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px 15px;
            width: 100%;
        }
        /* Title bar */
        .title-bar {
            background-color: #FF6F3C;
            padding: 15px;
            color: white;
            text-align: left;
            font-size: 20px;
            font-weight: bold;
            border-bottom-left-radius: 15px;
            border-bottom-right-radius: 15px;
        }
        /* Ingredient and Recipe Cards */
        .ingredient-card, .recipe-card {
            background: white;
            border-radius: 12px;
            padding: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            text-align: center;
            font-size: 14px;
            margin-bottom: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# ---- HEADER ----
st.markdown("<div class='title-bar'>Explore Recipes</div>", unsafe_allow_html=True)

# ---- IMAGE UPLOAD & PROCESSING SECTION ----
st.subheader("📤 Upload Your Leftover Food")
col1, col2 = st.columns([1, 2])

with col1:
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    col1.image(image, caption="📷 Uploaded Image", use_column_width=True)

    # Convert image to bytes
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="JPEG")
    img_bytes = img_bytes.getvalue()

    if col1.button("🔍 Identify Ingredients"):
        with st.spinner("Processing..."):
            # Mock API Call - Replace with real API call
            detected_ingredients = ["Tomato", "Onion", "Cheese"]
            st.session_state["ingredients"] = detected_ingredients
            col1.success("✅ Ingredients Identified!")

# ---- INGREDIENT LIST ----
st.subheader("📝 Identified Ingredients:")

if "ingredients" in st.session_state:
    ingredient_list = st.session_state["ingredients"]
    cols = st.columns(len(ingredient_list))  # Dynamic layout

    for i, ingredient in enumerate(ingredient_list):
        with cols[i]:
            st.markdown(f"""
                <div class='ingredient-card'>
                    <img src="https://www.themealdb.com/images/ingredients/{ingredient}.png" width='80'><br>
                    <strong>{ingredient}</strong>
                </div>
            """, unsafe_allow_html=True)

# ---- PREFERENCE SELECTION ----
st.subheader("🎯 Dietary Preferences:")
dietary_pref = st.selectbox("Choose Preference", ["None", "Vegetarian", "Vegan", "Gluten-Free", "Keto"])

# ---- GENERATE RECIPE BUTTON ----
if "ingredients" in st.session_state and st.button("🍽️ Generate Recipes"):
    with st.spinner("Creating delicious recipes..."):
        # Mock API Response - Replace with real API Call
        recipes = [
            {"name": "Tomato Cheese Salad", "ingredients": ["Tomato", "Cheese"], "instructions": "Mix everything and serve."},
            {"name": "Grilled Cheese Sandwich", "ingredients": ["Cheese", "Bread"], "instructions": "Grill with butter and serve."}
        ]
        st.subheader("🍛 Suggested Recipes")
        for recipe in recipes:
            st.markdown(f"### {recipe['name']}")
            st.write(f"**Ingredients:** {', '.join(recipe['ingredients'])}")
            st.write(f"**Instructions:** {recipe['instructions']}")

# ---- SEARCH & FILTER SECTION ----
col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    st.selectbox("📚 General Cookbook", ["All Recipes", "Vegetarian", "Quick Meals", "Desserts"], key="cookbook_select")

with col2:
    st.button("+ Add New", key="add_new")

st.text_input("🔍 Search recipe", placeholder="Search recipe here...")

# ---- MOCK RECIPE DATA ----
recipes = [
    {"name": "Applesauce Cake", "time": "45 minutes", "image": "https://via.placeholder.com/150"},
    {"name": "Lemon, Garlic and Thyme Roast Chicken", "time": "45 minutes", "image": "https://via.placeholder.com/150"},
    {"name": "Quick and Easy Caprese Salad", "time": "45 minutes", "image": "https://via.placeholder.com/150"},
    {"name": "Quinoa Tabouli with Lemon Garlic Shrimp", "time": "45 minutes", "image": "https://via.placeholder.com/150"},
    {"name": "Falafels With Tahini Sauce", "time": "45 minutes", "image": "https://via.placeholder.com/150"},
    {"name": "Eggless Brownies", "time": "45 minutes", "image": "https://via.placeholder.com/150"},
]

# ---- RECIPE CATEGORIES ----
st.subheader("🍔 American")
cols = st.columns(3)
for i, recipe in enumerate(recipes[:3]):
    with cols[i]:
        st.markdown(f"""
            <div class='recipe-card'>
                <img src='{recipe["image"]}' width='100%' style='border-radius:10px'><br>
                <strong>{recipe["name"]}</strong><br>
                ⏳ {recipe["time"]}
            </div>
        """, unsafe_allow_html=True)

st.subheader("🍕 European")
cols = st.columns(3)
for i, recipe in enumerate(recipes[3:]):
    with cols[i]:
        st.markdown(f"""
            <div class='recipe-card'>
                <img src='{recipe["image"]}' width='100%' style='border-radius:10px'><br>
                <strong>{recipe["name"]}</strong><br>
                ⏳ {recipe["time"]}
            </div>
        """, unsafe_allow_html=True)
