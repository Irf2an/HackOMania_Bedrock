from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io
import tempfile
import os
from langraph_pipeline import recognise_ingredients, get_recipes  # ✅ Import Langraph functions
from flask import Flask, render_template

app = Flask(__name__)
CORS(app)

# ✅ Store recognized ingredients temporarily (acts as session storage)
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
        # ✅ Create a temporary directory
        temp_dir = tempfile.gettempdir()
        image_path = os.path.join(temp_dir, file.filename)  # Safe cross-platform path

        # ✅ Save image
        image = Image.open(file)
        image.save(image_path)

        # ✅ Extract ingredients
        ingredients_result = recognise_ingredients(image_path)

        # ✅ Store ingredients (temporary storage per session)
        session_id = os.path.basename(image_path)  # Using filename as session key
        ingredient_storage[session_id] = ingredients_result

        return jsonify({
            "message": "Ingredients extracted successfully",
            "session_id": session_id,
            "ingredients": ingredients_result
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/GPT/send-details", methods=["POST"])
def generate_recipe():
    """
    Step 2: Accepts a list of ingredients directly and returns a recipe.
    """
    data = request.get_json()
    ingredients = data.get("ingredients")

    if not ingredients or not isinstance(ingredients, list):
        return jsonify({"error": "Invalid or missing ingredients list"}), 400

    try:
        # ✅ Generate recipe from the ingredient list
        recipes_result = get_recipes(ingredients)

        return jsonify({
            "message": "Recipe generated successfully",
            "ingredients": ingredients,
            "recipes": recipes_result
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)  # Ensure this is at the bottom
