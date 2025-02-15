from flask import Flask, request, jsonify, render_template, session as flask_session
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
from neo4j import GraphDatabase
import bcrypt
from passlib.hash import pbkdf2_sha256  # Import PBKDF2-SHA256 for hashing

#  Load OpenAI API Key from .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
CORS(app)  # Allow cross-origin requests if using a frontend

# Neo4j Connection Setup
NEO4J_URI = os.getenv("AURA_CONNECTION_URI")  # Change if using a remote Neo4j instance
NEO4J_USER = os.getenv("AURA_USERNAME")
NEO4J_PASSWORD = os.getenv("AURA_PASSWORD")
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

#  Store recognized ingredients temporarily (acts as session storage)
ingredient_storage =  {'almond': 'https://oaidalleapiprodscus.blob.core.windows.net/private/org-Uj9FJRmMKLcHA4gqcnprCSG2/user-oheEB9tdBKLOOZv1WdUAtztR/img-iteRsunfw2mchNcngUukvnV8.png?st=2025-02-15T18%3A07%3A36Z&se=2025-02-15T20%3A07%3A36Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-02-14T22%3A54%3A35Z&ske=2025-02-15T22%3A54%3A35Z&sks=b&skv=2024-08-04&sig=vNHCRpqMQ%2BOb992vniPm2FtvkUVoaY%2BzITka30S314U%3D', 'pickled cucumber': 'https://oaidalleapiprodscus.blob.core.windows.net/private/org-Uj9FJRmMKLcHA4gqcnprCSG2/user-oheEB9tdBKLOOZv1WdUAtztR/img-aTkRFRMwrqVjiVXTC0QMX2zN.png?st=2025-02-15T18%3A07%3A36Z&se=2025-02-15T20%3A07%3A36Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-02-15T11%3A19%3A34Z&ske=2025-02-16T11%3A19%3A34Z&sks=b&skv=2024-08-04&sig=cqmp6kretJNCMKB4Q6eV00seAllwBHpImT2xnv3tNkM%3D', 'sparkling water': 'https://oaidalleapiprodscus.blob.core.windows.net/private/org-Uj9FJRmMKLcHA4gqcnprCSG2/user-oheEB9tdBKLOOZv1WdUAtztR/img-bouGkYPsiOZFfXeQ2qb2UxXi.png?st=2025-02-15T18%3A07%3A36Z&se=2025-02-15T20%3A07%3A36Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-02-15T12%3A11%3A45Z&ske=2025-02-16T12%3A11%3A45Z&sks=b&skv=2024-08-04&sig=bxP1B2lp85VI1yZtsmnaJW6mANAMpwmTiUmBOI8OWgY%3D', 'salad dressing': 'https://oaidalleapiprodscus.blob.core.windows.net/private/org-Uj9FJRmMKLcHA4gqcnprCSG2/user-oheEB9tdBKLOOZv1WdUAtztR/img-gIk3r9zKbNiMZP7dInSdr6O0.png?st=2025-02-15T18%3A07%3A35Z&se=2025-02-15T20%3A07%3A35Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-02-15T03%3A06%3A44Z&ske=2025-02-16T03%3A06%3A44Z&sks=b&skv=2024-08-04&sig=dIWavTLD%2BaaEIAElPV%2BIeXcGx7zOFd2OdAN%2BK64QCjo%3D', 'arugula': 'https://oaidalleapiprodscus.blob.core.windows.net/private/org-Uj9FJRmMKLcHA4gqcnprCSG2/user-oheEB9tdBKLOOZv1WdUAtztR/img-2Pa3OtXT50rf1WjxbLTjY19u.png?st=2025-02-15T18%3A07%3A36Z&se=2025-02-15T20%3A07%3A36Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-02-15T08%3A24%3A22Z&ske=2025-02-16T08%3A24%3A22Z&sks=b&skv=2024-08-04&sig=btVmRdaZ%2BZ83m9BAsTghW9jcu82BSRUwTtJDfmknS2Y%3D', 'sunflower seed': 'https://oaidalleapiprodscus.blob.core.windows.net/private/org-Uj9FJRmMKLcHA4gqcnprCSG2/user-oheEB9tdBKLOOZv1WdUAtztR/img-ZSdLZL3uK7YWrIVCdyCwPJsJ.png?st=2025-02-15T18%3A07%3A36Z&se=2025-02-15T20%3A07%3A36Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-02-15T13%3A35%3A25Z&ske=2025-02-16T13%3A35%3A25Z&sks=b&skv=2024-08-04&sig=FOqBsq0wDONqfmngPtnMbD0VsX2d8/8dhEHIrJOTHTk%3D', 'red cabbage': 'https://oaidalleapiprodscus.blob.core.windows.net/private/org-Uj9FJRmMKLcHA4gqcnprCSG2/user-oheEB9tdBKLOOZv1WdUAtztR/img-0uCzmJ3bkxqIIU6Aud8wkLGR.png?st=2025-02-15T18%3A07%3A35Z&se=2025-02-15T20%3A07%3A35Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-02-15T00%3A02%3A13Z&ske=2025-02-16T00%3A02%3A13Z&sks=b&skv=2024-08-04&sig=WLxmF7hJFz2kJTokNWYhuyXuU9AlWdt19RAZytjtVGY%3D', 'red bell pepper': 'https://oaidalleapiprodscus.blob.core.windows.net/private/org-Uj9FJRmMKLcHA4gqcnprCSG2/user-oheEB9tdBKLOOZv1WdUAtztR/img-tvUgr5Wtd4TUVyEx6RS45bff.png?st=2025-02-15T18%3A07%3A35Z&se=2025-02-15T20%3A07%3A35Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-02-15T17%3A17%3A15Z&ske=2025-02-16T17%3A17%3A15Z&sks=b&skv=2024-08-04&sig=4PDXpWOdPgrzcejKhmIdMD3%2BsBRNOYcK67d4omMSFr8%3D', 'pear': 'https://oaidalleapiprodscus.blob.core.windows.net/private/org-Uj9FJRmMKLcHA4gqcnprCSG2/user-oheEB9tdBKLOOZv1WdUAtztR/img-IKlumwsfICebBeqWEQqPsOGW.png?st=2025-02-15T18%3A07%3A36Z&se=2025-02-15T20%3A07%3A36Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-02-15T02%3A55%3A42Z&ske=2025-02-16T02%3A55%3A42Z&sks=b&skv=2024-08-04&sig=DQqhUM2YAT8aaiUpvkea0cq/xsWWhjWk2V13AdC2bm8%3D', 'pasta': 'https://oaidalleapiprodscus.blob.core.windows.net/private/org-Uj9FJRmMKLcHA4gqcnprCSG2/user-oheEB9tdBKLOOZv1WdUAtztR/img-qdLxqQP4HGRp9g0AgPQ8OAH7.png?st=2025-02-15T18%3A07%3A37Z&se=2025-02-15T20%3A07%3A37Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-02-15T05%3A40%3A24Z&ske=2025-02-16T05%3A40%3A24Z&sks=b&skv=2024-08-04&sig=ahLQ/TKM6AnAI4D4kTTFRmqYWON3hq2IxeqeDE7LuUg%3D', 'pickled carrot': 'https://oaidalleapiprodscus.blob.core.windows.net/private/org-Uj9FJRmMKLcHA4gqcnprCSG2/user-oheEB9tdBKLOOZv1WdUAtztR/img-CqOw6aR4yp4kyoghfcynm1Oh.png?st=2025-02-15T18%3A07%3A35Z&se=2025-02-15T20%3A07%3A35Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-02-15T14%3A51%3A37Z&ske=2025-02-16T14%3A51%3A37Z&sks=b&skv=2024-08-04&sig=4ep%2B4LuTOtaS8/Uvv9TpmsBVt/NzCvlNyqDYrpCpCvc%3D', 'bottled water': 'https://oaidalleapiprodscus.blob.core.windows.net/private/org-Uj9FJRmMKLcHA4gqcnprCSG2/user-oheEB9tdBKLOOZv1WdUAtztR/img-7nZbG3GVrVsBFeZZ0sG3tl2J.png?st=2025-02-15T18%3A07%3A35Z&se=2025-02-15T20%3A07%3A35Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-02-15T07%3A05%3A32Z&ske=2025-02-16T07%3A05%3A32Z&sks=b&skv=2024-08-04&sig=sD3/Maega7rg/ikUf1Gc009v6vxhxkbwgHZVgqlG8qg%3D'}

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
        print("Generating recipe...")
        #  Run LangGraph pipeline with the input ingredient list
        input_data = {"ingredients": ingredients, "preferences": preferences}
        output_data = compiled_recipe_graph.invoke(input_data)  #  LangGraph execution
        recipes_result = output_data["recipe_text"]

        debug = jsonify({
            "message": "Recipe generated successfully",
            "ingredients": ingredients,
            "recipes": recipes_result
        })

        print("debug = ", debug)

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
        print(f"Generating image for {ingredient}...")
        response = await asyncio.to_thread(openai.images.generate,
            model="dall-e-2",  #  Faster model
            prompt=f"A high-resolution image of fresh {ingredient} as food, isolated on a white background.",
            n=1,
            size="1024x1024"
        )
        print("Generated URL = ", response.data[0].url)
        return response.data[0].url
    except openai.OpenAIError as e:
        return f"Error: {str(e)}"

@app.route("/GPT/missing-url", methods=["POST"])
async def get_ingredient_images():
    """
    Accepts a list of ingredient names and returns DALL·E 2-generated images asynchronously.
    Uses caching to avoid redundant API calls.
    """
    data = request.get_json()
    ingredients = data.get("ingredients")

    if not ingredients or not isinstance(ingredients, list):
        return jsonify({"error": "Invalid or missing ingredients list"}), 400

    for ingredient in ingredients:
        if ingredient in ingredient_storage:
            print(f"{ingredient} exists in cache!")

    # Ingredients that need new images
    new_ingredients = [ingredient for ingredient in ingredients if ingredient not in ingredient_storage]
    
    # Generate new images only for missing ingredients
    if new_ingredients:
        tasks = [generate_dalle_image_async(ingredient) for ingredient in new_ingredients]
        new_images = await asyncio.gather(*tasks)

        # Store newly generated images in cache
        for ingredient, image in zip(new_ingredients, new_images):
            ingredient_storage[ingredient] = image

    # Retrieve all images from cache
    ingredient_images = {ingredient: ingredient_storage[ingredient] for ingredient in ingredients}
    print("ingredient_storage = ", ingredient_storage)

    return jsonify(ingredient_images), 200


def create_user(tx, username, hashed_password):
    query = """
    MERGE (u:User {username: $username})
    ON CREATE SET u.password = $hashed_password
    RETURN u.username
    """
    result = tx.run(query, username=username, hashed_password=hashed_password)
    return result.single()

def find_user(tx, username):
    query = "MATCH (u:User {username: $username}) RETURN u.password"
    result = tx.run(query, username=username)
    return result.single()


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Generate a unique salt
    salt = os.urandom(16).hex()
    salted_password = f"{salt}{password}"

    # Hash the salted password
    hashed_password = pbkdf2_sha256.hash(salted_password)

    with driver.session() as session:
        existing_user = session.run("MATCH (u:User {username: $username}) RETURN u", username=username).single()
        if existing_user:
            return jsonify({"error": "Username already taken"}), 400

        session.run(
            """
            CREATE (u:User {username: $username, password: $hashed_password, salt: $salt})
            """,
            username=username,
            hashed_password=hashed_password,
            salt=salt
        )

    return jsonify({"message": "User registered successfully"}), 201



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    with driver.session() as session:
        result = session.run(
            """
            MATCH (u:User {username: $username})
            RETURN u.password AS password, u.salt AS salt
            """,
            username=username
        )
        record = result.single()

        if not record:
            return jsonify({"error": "Invalid username or password"}), 401

        stored_password = record["password"]
        salt = record["salt"]

        # Verify salted password
        salted_password = f"{salt}{password}"
        if pbkdf2_sha256.verify(salted_password, stored_password):
            flask_session["username"] = username
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401



@app.route("/logout", methods=["POST"])
def logout():
    flask_session.pop("username", None)
    return jsonify({"message": "Logged out successfully"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8071))  # Heroku requires using PORT env var
    app.run(host="0.0.0.0", port=port, debug=True, threaded=True)  # Use 0.0.0.0 for Heroku