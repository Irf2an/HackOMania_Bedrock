from flask import Flask, request, jsonify
from PIL import Image
import io
import tempfile
import os

app = Flask(__name__)

def start_langraph_sequence(image_path):
    """
    Placeholder for Langraph call.
    This function should be completed by your teammate.
    Right now, it simply returns a dummy response.
    """
    # return {"message": "Langraph sequence initiated", "image_path": image_path}
    return {"message": "hooray", "image_path": image_path}  # Temporary response

@app.route("/GPT/send-image", methods=["POST"])
def process_image():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:
        # Create a temporary directory
        temp_dir = tempfile.gettempdir()
        image_path = os.path.join(temp_dir, file.filename)  # Safe cross-platform path

        # Save image
        image = Image.open(file)
        image.save(image_path)

        return jsonify({"message": "hooray", "image_path": image_path}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True)  # Ensure this is at the bottom