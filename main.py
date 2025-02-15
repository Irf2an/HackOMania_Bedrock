import streamlit as st
import requests
from PIL import Image
import io
import os

def get_image_url(ingredient_name):
    mealdb_url = f"https://www.themealdb.com/images/ingredients/{ingredient_name}.png"
    response = requests.head(mealdb_url)
    
    if response.status_code == 200:
        return mealdb_url
    else:
        # Fallback to Foodish API for a random food image
        foodish_response = requests.get("https://foodish-api.herokuapp.com/api/")
        if foodish_response.status_code == 200:
            return foodish_response.json().get("image", "https://via.placeholder.com/80?text=No+Image")
        else:
            # Final fallback to a placeholder image
            return "https://via.placeholder.com/80?text=No+Image"
        
# ---- APP CONFIGURATION ----
st.set_page_config(page_title="Kitchen Copilot", page_icon="images/KitchenCopilot_Logo.png", layout="wide")

# ---- FORCE LIGHT THEME (REMOVE BLACK ELEMENTS) ----
st.markdown("""
    <style>
        /* Ensure all text is black */
        * {
            color: #000000 !important;
        }
        /* Full-width Orange Title Bar */
        .title-bar {
            background-color: #FF6F3C;
            padding: 20px;
            color: white;
            text-align: center;
            font-size: 22px;
            font-weight: bold;
            width: 100%;
        }
        /* Ensure input fields, select boxes, file uploader, and buttons are white with black text */
        input[type="text"], select, .stTextInput>div>div>input, .stSelectbox>div>div>select, 
        .stFileUploader>div>div>button, .stButton>button {
            background-color: #FFFFFF !important;
            color: #000000 !important;  /* Ensure text is black */
            border: 1px solid #CCC !important;
            border-radius: 8px;
            padding: 12px;
            width: 100%;
        }
        /* Ensure the file uploader box is white */
        .stFileUploader>div {
            background-color: #FFFFFF !important;
            border: 1px solid #CCC !important;
            color: #000000 !important;
            border-radius: 8px;
        }
        /* Ensure "Dietary Preferences" and "All Recipes" select boxes are white */
        .stSelectbox>div>div {
            background-color: #FFFFFF !important;
        }
        /* Ensure "All Recipes" text is black */
        .stSelectbox>div>div>select option {
            color: #000000 !important;
        }
        /* White background for entire app */
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #FAF9F6 !important;
            color: #333 !important;
        }
        /* Full-width Orange Title Bar */
        .title-bar {
            background-color: #FF6F3C;
            padding: 20px;
            color: white;
            text-align: center;
            font-size: 22px;
            font-weight: bold;
            width: 100%;
        }
        /* Ensure text fields and dropdowns are white */
        input[type="text"], select, .stTextInput>div>div>input, .stSelectbox>div>div>select, .stFileUploader>div>div>button {
            background-color: #FFFFFF !important;
            color: #333 !important;
            border: 1px solid #CCC !important;
            border-radius: 8px;
            padding: 12px;
            width: 100%;
        }
        /* Style buttons */
        .stButton>button {
            background-color: #FF6F3C !important;
            color: white !important;
            font-size: 16px;
            font-weight: bold;
            border-radius: 10px;
            padding: 12px;
            width: 100%;
        }
        /* Styled container to simulate input field */
        .input-container {
            background: white;
            border-radius: 10px;
            padding: 10px;
            border: 1px solid #CCC;
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            font-weight: bold;
            color: #666;
        }
        /* Ingredient and Recipe Cards */
        .ingredient-card, .recipe-card {
            background: white;
            border-radius: 12px;
            padding: 12px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            text-align: center;
            font-size: 14px;
            margin-bottom: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# ---- HEADER ----
st.markdown("""
    <style>
        /* Full-width Orange Header */
        .header-bar {
            background-color: #FF6F3C;
            padding: 15px 20px;
            color: white !important;
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 20px;
            font-weight: bold;
            width: 100%;
            border-bottom-left-radius: 15px;
            border-bottom-right-radius: 15px;
        }
        /* Left-aligned title */
        .header-title {
            margin: 0;
            font-size: 18px;
            font-weight: normal;
            color: white !important;  /* Ensure title text remains white */
        }
        /* Right-aligned icons */
        .header-icons {
            display: flex;
            gap: 15px;
            align-items: center;
        }
        .header-icons img {
            width: 22px; /* Adjust icon size */
            height: 22px;
            filter: invert(1);
        }
    </style>
    <div class="header-bar">
        <span class="header-title">Explore Recipes</span>
        <div class="header-icons">
            <img src="https://cdn-icons-png.flaticon.com/512/134/134819.png" alt="Chat Icon">
            <img src="https://cdn-icons-png.flaticon.com/512/3602/3602145.png" alt="Bell Icon">  <!-- Updated Bell Icon -->
            <img src="https://cdn-icons-png.flaticon.com/512/5662/5662990.png" alt="Menu Icon">
        </div>
    </div>
""", unsafe_allow_html=True)


# ---- Image Upload & Processing ----
st.markdown("<div class='input-container'>📤 Upload Your Leftover Food</div>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Uploader", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

if uploaded_file:
    col1, col2 = st.columns([1, 2])

    with col1:
        image = Image.open(uploaded_file)
        st.image(image, caption="📷 Uploaded Image", use_column_width=True)

    # Convert image to bytes
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="JPEG")
    img_bytes.seek(0)

    if st.button("🔍 Identify Ingredients"):
        with st.spinner("Processing..."):
            data =  {'image_path': '/var/folders/27/fq0b11557z5281q2l7v0nk7w0000gn/T/image.jpg', 'ingredients': ['Maple syrup', 'mustard', 'ketchup', 'tortillas', 'milk', 'carrots', 'lettuce', 'spinach', 'bell peppers', 'onions', 'celery', 'apples', 'pears', 'bananas', 'oranges', 'almonds', 'dates', 'eggs', 'cheese', 'yogurt.'], 'message': 'Langraph sequence initiated', 'recipes': 'Dish Name: Savory Breakfast Tortillas with Fresh Fruit Salad\n\nIngredients:\n- Tortillas\n- Eggs\n- Cheese\n- Milk\n- Lettuce\n- Spinach\n- Bell peppers\n- Onions\n- Carrots\n- Celery\n- Apples\n- Pears\n- Bananas\n- Oranges\n- Almonds\n- Dates\n- Yogurt\n- Maple syrup\n- Mustard\n- Ketchup\n\nInstructions:\n**For the Savory Breakfast Tortillas:**\n1. **Prepare the Vegetables:**\n   - Finely chop the onions, bell peppers, carrots, and celery.\n   - Shred some lettuce and roughly chop the spinach.\n\n2. **Make the Egg Mixture:**\n   - In a bowl, beat the eggs and add a splash of milk, salt, and pepper to taste. Mix well.\n\n3. **Cook the Vegetables:**\n   - Heat a non-stick skillet over medium heat. Add a little oil or butter.\n   - Sauté the onions, bell peppers, carrots, and celery until they are soft.\n\n4. **Add the Eggs:**\n   - Pour the egg mixture into the skillet with the vegetables, stirring gently to combine.\n   - Cook until the eggs are set but still moist, stirring occasionally.\n\n5. **Prepare the Tortillas:**\n   - Warm the tortillas in another pan or in the microwave.\n\n6. **Assemble the Tortillas:**\n   - Place some shredded lettuce and chopped spinach on each tortilla.\n   - Spoon the cooked egg and vegetable mixture over the greens.\n   - Sprinkle shredded cheese on top.\n   - Optionally, you can add a drizzle of ketchup or mustard for extra flavor.\n\n7. **Serve:**\n   - Fold the tortillas over the filling and serve warm.\n\n**For the Fresh Fruit Salad:**\n1. **Prepare the Fruit:**\n   - Chop the apples, pears, bananas, and oranges into bite-sized pieces.\n   - Pit and chop the dates.\n\n2. **Mix the Fruit:**\n   - In a large bowl, combine all the chopped fruits and dates.\n   - Add a handful of almonds for crunch.\n\n3. **Dress the Salad:**\n   - In a small bowl, mix yogurt with a little maple syrup to create a sweet dressing.\n   - Pour the dressing over the fruit salad and toss gently to coat.\n\n4. **Chill and Serve:**\n   - Refrigerate the fruit salad for at least 30 minutes before serving to allow the flavors to meld.\n\n**Final Touch:**\n- Serve the savory breakfast tortillas alongside the chilled fruit salad for a balanced and nutritious meal. Enjoy your colorful and delicious breakfast!'}
            st.session_state["ingredients"] = data.get("ingredients", [])
            st.session_state["recipes"] = data.get("recipes", [])
            # try:
            #     response = requests.post(
            #         "http://127.0.0.1:5000/GPT/send-image",
            #         files={"file": ("image.jpg", img_bytes, "image/jpeg")}
            #     )

            #     if response.status_code == 200:
            #         data = response.json()
            #         print("Response = ", data)
            #         st.session_state["ingredients"] = data.get("ingredients", [])
            #         st.session_state["recipes"] = data.get("recipes", [])

            #         if not st.session_state["ingredients"]:
            #             st.warning("No ingredients detected. Try a different image.")
            #         else:
            #             st.success("✅ Ingredients Identified!")

            #     else:
            #         st.error(f"Error: {response.json().get('error', 'Unknown error')}")

            # except Exception as e:
            #     st.error(f"Failed to process image: {str(e)}")

# ---- DISPLAY INGREDIENT LIST IN RESPONSIVE GRID ----
if "ingredients" in st.session_state and st.session_state["ingredients"]:
    st.markdown("<h2 class='input-container' style='text-align:center;'>📝 Identified Ingredients</h2>", unsafe_allow_html=True)

    if "editable_ingredients" not in st.session_state:
        st.session_state["editable_ingredients"] = list(st.session_state["ingredients"])

    # **Ensure Ingredient Inputs Exist in Session State**
    for i, ingredient in enumerate(st.session_state["editable_ingredients"]):
        key_name = f"ingredient_{i}"
        if key_name not in st.session_state:
            st.session_state[key_name] = ingredient  # Initialize input field value

    # Set up dynamic grid
    cols_per_row = 4
    num_ingredients = len(st.session_state["editable_ingredients"])
    rows = (num_ingredients // cols_per_row) + (1 if num_ingredients % cols_per_row != 0 else 0)

    for row in range(rows):
        cols = st.columns(cols_per_row)

        for col_index in range(cols_per_row):
            ingredient_index = row * cols_per_row + col_index
            if ingredient_index < num_ingredients:
                ingredient = st.session_state["editable_ingredients"][ingredient_index]
                image_url = get_image_url(ingredient)

                with cols[col_index]:
                    st.image(image_url, width=80)

                    # Editable text input (No full rerun)
                    def update_ingredient(index):
                        st.session_state["editable_ingredients"][index] = st.session_state[f"ingredient_{index}"]

                    st.text_input(
                        "Ingredient", st.session_state[f"ingredient_{ingredient_index}"], 
                        key=f"ingredient_{ingredient_index}",
                        on_change=update_ingredient, 
                        args=(ingredient_index,),
                        label_visibility="collapsed"
                    )

                    # Buttons for editing and deleting ingredients
                    col1, col2 = st.columns([1, 1])

                    with col1:
                        st.button("✏️", key=f"edit_{ingredient_index}", use_container_width=True)

                    with col2:
                        def remove_ingredient(index=ingredient_index):
                            del st.session_state["editable_ingredients"][index]
                            st.experimental_rerun()  # Only updates the affected item

                        st.button("❌", key=f"delete_{ingredient_index}", on_click=remove_ingredient, args=(ingredient_index,), use_container_width=True)

    # ---- Add New Ingredient Functionality ----
    new_ingredient = st.text_input("➕ Add a New Ingredient", key="new_ingredient")

    if st.button("Add Ingredient", key="add_ingredient"):
        if new_ingredient and new_ingredient not in st.session_state["editable_ingredients"]:
            st.session_state["editable_ingredients"].append(new_ingredient)
            st.rerun()

# ---- Generate Recipes (Finalizes Ingredients) ----
if "editable_ingredients" in st.session_state and len(st.session_state["editable_ingredients"]) > 0:
    st.markdown("<h2 class='input-container' style='text-align:center;'>🎯 Customize Your Recipe</h2>", unsafe_allow_html=True)

    # Preferences Selection
    dietary_pref = st.selectbox(
        "Dietary Preferences", 
        ["🎯 Dietary Preferences", "None", "Vegetarian", "Vegan", "Gluten-Free", "Keto"], 
        index=0, 
        label_visibility="collapsed"
    )

    seasoning_pref = st.selectbox(
        "Seasoning Preference",
        ["🌶️ Spice Level", "Mild", "Medium", "Spicy", "No Preference"],
        index=0,
        label_visibility="collapsed"
    )

    cooking_time_pref = st.selectbox(
        "Cooking Time",
        ["⏳ Cooking Time", "Quick (Under 30 min)", "Moderate (30-60 min)", "Slow Cooked (1hr+)", "No Preference"],
        index=0,
        label_visibility="collapsed"
    )

    recipe_style_pref = st.selectbox(
        "Recipe Style",
        ["🍽️ Recipe Style", "Classic", "Vegan", "Spicy", "Mediterranean", "Asian Fusion", "No Preference"],
        index=0,
        label_visibility="collapsed"
    )

    user_preferences = {
        "Dietary Preference": dietary_pref if dietary_pref != "🎯 Dietary Preferences" else None,
        "Seasoning Preference": seasoning_pref if seasoning_pref != "🌶️ Spice Level" else None,
        "Cooking Time": cooking_time_pref if cooking_time_pref != "⏳ Cooking Time" else None,
        "Recipe Style": recipe_style_pref if recipe_style_pref != "🍽️ Recipe Style" else None
    }
    
    user_preferences = {k: v for k, v in user_preferences.items() if v}

    if st.button("🍽️ Generate Recipes", key="generate_recipes"):
        st.session_state["final_ingredients"] = st.session_state["editable_ingredients"]
        st.write("Selected Preferences:", user_preferences)
        st.write("Final Ingredients:", st.session_state["final_ingredients"])

        with st.spinner("Creating delicious recipes..."):
            recipes = [
                {"name": "Tomato Cheese Salad", "ingredients": ["Tomato", "Cheese"], "instructions": "Mix everything and serve."},
                {"name": "Grilled Cheese Sandwich", "ingredients": ["Cheese", "Bread"], "instructions": "Grill with butter and serve."}
            ]
            st.markdown("<div class='input-container'>🍛 Suggested Recipes</div>", unsafe_allow_html=True)
            for recipe in recipes:
                st.markdown(f"### {recipe['name']}")
                st.write(f"**Ingredients:** {', '.join(recipe['ingredients'])}")
                st.write(f"**Instructions:** {recipe['instructions']}")


# ---- SEARCH & FILTER SECTION ----
search_query = st.text_input("Search", placeholder="🔍 Search Recipe", label_visibility="collapsed")

col1, col2 = st.columns([3, 1])
with col1:
    st.selectbox("Select", ["All Recipes", "Vegetarian", "Quick Meals", "Desserts"], key="cookbook_select", label_visibility="collapsed")
with col2:
    st.button("+ Add New", key="add_new")

# ---- MOCK RECIPE DATA ----
image_folder = "images"

recipes = [
    {"name": "Applesauce Cake", "time": "45 minutes", "image": os.path.join(image_folder, "AppleSauceCake.jpg")},
    {"name": "Lemon, Garlic and Thyme Roast Chicken", "time": "45 minutes", "image": os.path.join(image_folder, "RoastChicken.jpeg")},
    {"name": "Quick and Easy Caprese Salad", "time": "45 minutes", "image": os.path.join(image_folder, "CapreseSalad.jpeg")},
    {"name": "Quinoa Tabouli with Lemon Garlic Shrimp", "time": "45 minutes", "image": os.path.join(image_folder, "GarlicShrimp.jpeg")},
    {"name": "Falafels With Tahini Sauce", "time": "45 minutes", "image": os.path.join(image_folder, "Falafels.jpg")},
    {"name": "Eggless Brownies", "time": "45 minutes", "image": os.path.join(image_folder, "Brownie.jpeg")},
]

# ---- RECIPE CATEGORIES ----
st.markdown("<div class='input-container'>🍔 American Recipes</div>", unsafe_allow_html=True)
cols = st.columns(3)
for i, recipe in enumerate(recipes[:3]):
    with cols[i]:
        st.image(recipe["image"], width=30, use_column_width=True)
        st.markdown(f"**{recipe['name']}**")
        st.markdown(f"⏳ {recipe['time']}")

st.markdown("<div class='input-container'>🍕 European Recipes</div>", unsafe_allow_html=True)
cols = st.columns(3)
for i, recipe in enumerate(recipes[3:]):
    with cols[i]:
        st.image(recipe["image"], width=30, use_column_width=True)
        st.markdown(f"**{recipe['name']}**")
        st.markdown(f"⏳ {recipe['time']}")