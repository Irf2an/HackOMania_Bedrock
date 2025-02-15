from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from PIL import Image
import io
import tempfile
import os
from langraph_pipeline import compiled_ingredient_graph, compiled_recipe_graph  #  Import LangGraph pipeline
from dotenv import load_dotenv
import requests
import openai
import asyncio

#  Load OpenAI API Key from .env
load_dotenv()

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests if using a frontend

#  Store recognized ingredients temporarily (acts as session storage)
ingredient_storage = {}

@app.route('/')
def index_page():
    return render_template('index.html')

@app.route("/GPT/send-image", methods=["POST"])
def process_image():
    """
    Step 1: Takes an image, extracts ingredients, and stores them temporarily.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:     
        #  Create a temporary directory
        temp_dir = tempfile.gettempdir()
        image_path = os.path.join(temp_dir, file.filename)  # Safe cross-platform path

        #  Save image
        image = Image.open(file)
        image.save(image_path)

        #  Run LangGraph pipeline with the input image
        input_data = {"image_path": image_path}
        output_data = compiled_ingredient_graph.invoke(input_data)  #  LangGraph execution
        filtered_ingredients = output_data["filtered_ingredients"]
        
        #  Store ingredients (temporary storage per session)
        session_id = os.path.basename(image_path)  # Using filename as session key
        ingredient_storage[session_id] = filtered_ingredients

        return jsonify({
            "message": "Ingredients extracted successfully",
            "session_id": session_id,
            "ingredients": filtered_ingredients
        }), 200  #  Send back LangGraph result

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/GPT/send-details", methods=["POST"])
def generate_recipe():
    """
    Step 2: Accepts a list of ingredients directly and returns a recipe.
    """
    data = request.get_json()
    ingredients = data.get("ingredients")
    preferences = data.get("preferences")

    if not ingredients or not isinstance(ingredients, list):
        return jsonify({"error": "Invalid or missing ingredients list"}), 400

    try:
        #  Run LangGraph pipeline with the input ingredient list
        input_data = {"ingredients": ingredients, "preferences": preferences}
        output_data = compiled_recipe_graph.invoke(input_data)  #  LangGraph execution
        recipes_result = output_data["recipe_text"]

        return jsonify({
            "message": "Recipe generated successfully",
            "ingredients": ingredients,
            "recipes": recipes_result
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#  Load OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

async def generate_dalle_image_async(ingredient):
    """
    Uses OpenAI DALL·E 2 to generate an image of the given ingredient asynchronously.
    Returns a URL for the generated image.
    """
    try:
        response = await asyncio.to_thread(openai.images.generate,
            model="dall-e-2",  #  Faster model
            prompt=f"A high-resolution image of fresh {ingredient} as food, isolated on a white background.",
            n=1,
            size="1024x1024"
        )
        return response.data[0].url
    except openai.OpenAIError as e:
        return f"Error: {str(e)}"

@app.route("/GPT/missing-url", methods=["POST"])
async def get_ingredient_images():
    """
    Accepts a list of ingredient names and returns DALL·E 2-generated images asynchronously.
    """
    data = request.get_json()
    ingredients = data.get("ingredients")

    if not ingredients or not isinstance(ingredients, list):
        return jsonify({"error": "Invalid or missing ingredients list"}), 400

    #  Run all image requests in parallel
    tasks = [generate_dalle_image_async(ingredient) for ingredient in ingredients]
    ingredient_images = await asyncio.gather(*tasks)

    return jsonify(dict(zip(ingredients, ingredient_images))), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8071))  # Heroku requires using PORT env var
    app.run(host="0.0.0.0", port=port, debug=True)  # Use 0.0.0.0 for Heroku