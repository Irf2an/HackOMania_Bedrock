import streamlit as st
import requests
import json  #For JSON processing

st.title("Leftover Food Recipe App")

uploaded_image = st.camera_input("Take a photo of your leftover food")

if uploaded_image is not None:
    st.image(uploaded_image, caption="Your Leftover Food", use_column_width=True)

    if st.button("Recognize Ingredients"):
        # Simulate ingredient recognition (REPLACE THIS WITH YOUR ACTUAL LOGIC)
        # In a real app, you would send the image to your backend for processing.
        # For this example, we'll just return some dummy ingredients.
        # with open("food.jpg", "wb") as f:
        #     f.write(uploaded_image.getbuffer())
        # files = {'file': open("food.jpg", 'rb')}
        # response = requests.post('http://127.0.0.1:5000/recognize_ingredients', files=files)
        # ingredients = response.json()['ingredients']
        ingredients = ["Apple", "Banana", "Orange"]  # Replace with actual recognition

        edited_ingredients = st.multiselect("Edit Ingredients", ingredients, default=ingredients)

        if st.button("Get Recipes"):
            if edited_ingredients:
                payload = {"ingredients": edited_ingredients}
                response = requests.post('http://127.0.0.1:5000/get_recipes', json=payload)
                if response.status_code == 200:
                    recipes = response.json().get('recipes', []) #Handle cases where recipes might not exist
                    if recipes:
                        st.subheader("Here are some recipes:")
                        for recipe in recipes:
                            st.write(f"- {recipe}") # Simplified recipe display
                    else:
                        st.write("No recipes found for those ingredients.")
                else:
                    st.write(f"Error: {response.status_code}") #Display error message
            else:
                st.write("Please select at least one ingredient.")