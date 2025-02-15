from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
import base64

# ✅ Load environment variables
load_dotenv()

# ✅ Get the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")

# ✅ Check if API key is missing
if not api_key:
    raise ValueError("❌ ERROR: OPENAI_API_KEY is missing. Please set it in the .env file or environment variables.")

# ✅ Initialize GPT-4 Turbo (with Vision support)
llm = ChatOpenAI(model_name="gpt-4-turbo", temperature=0.3, openai_api_key=api_key)

def encode_image(image_path):
    """
    Converts an image file into a Base64 string for OpenAI's Vision API.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def recognise_ingredients(image_path):
    """
    Uses GPT-4 Turbo Vision to analyze an image and extract ingredients.
    """
    # ✅ Convert image to Base64 format
    encoded_image = encode_image(image_path)

    # ✅ Correct OpenAI ChatML format for image input
    messages = [
        {"role": "system", "content": "You are a food expert who can identify ingredients from images."},
        {"role": "user", "content": [
            {"type": "text", "text": "Analyze this image and list the ingredients present. Provide only a comma-separated list."},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
        ]}
    ]

    # ✅ Call GPT-4 Turbo API
    response = llm.invoke(messages)

    # ✅ Extract response text from AIMessage
    response_text = response.content if hasattr(response, "content") else str(response)

    # ✅ Process response into a clean ingredient list
    ingredients = [ingredient.strip() for ingredient in response_text.split(",")]

    return ingredients

def get_recipes(ingredients):
    """
    Uses GPT-4 Turbo to suggest a dish based on the extracted ingredients.
    Returns a dish name and a short step-by-step recipe.
    """
    # ✅ Create structured prompt for better recipe generation
    messages = [
        {"role": "system", "content": "You are a professional chef who suggests recipes based on available ingredients."},
        {"role": "user", "content": f"""
        I have the following ingredients available: {', '.join(ingredients)}.
        Suggest a suitable dish I can cook using these ingredients and provide a step-by-step recipe.
        Make sure the recipe is practical and uses all or most of the ingredients listed.
        Format the response as:
        Dish Name: [Dish Name]
        Ingredients: [List of Ingredients]
        Instructions: [Step-by-step cooking instructions]
        """}
    ]

    # ✅ Call GPT-4 Turbo API to generate a recipe
    response = llm.invoke(messages)

    # ✅ Extract response text
    recipe_text = response.content if hasattr(response, "content") else str(response)

    return recipe_text
