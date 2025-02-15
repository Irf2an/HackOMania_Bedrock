from flask import Flask, request, jsonify
from PIL import Image
import io
import tempfile
import os
from langraph_pipeline import recognise_ingredients, get_recipes  # ✅ Import Langraph functions (placeholders)

app = Flask(__name__)

# ✅ Temporary dummy functions to test API (Replace with Langraph later)
# def recognise_ingredients(image_path):
#     """ Dummy function to return fake ingredients. """
#     return ["chicken", "garlic", "pepper"]  # Fake output

# def get_recipes(ingredients):
#     """ Dummy function to return fake recipes. """
#     return ["Garlic Chicken Stir Fry", "Spicy Chicken Soup"]  # Fake output

@app.route("/GPT/send-image", methods=["POST"])
def process_image():
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

        # ✅ Start both Langraphs simultaneously (placeholders)
        ingredients_result = recognise_ingredients(image_path)  # Placeholder function
        recipes_result = get_recipes(ingredients_result)  # Placeholder function

        return jsonify({
            "message": "Langraph sequence initiated",
            "image_path": image_path,
            "ingredients": ingredients_result,
            "recipes": recipes_result
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)  # Ensure this is at the bottom
