from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
import base64
from langgraph.graph import StateGraph, END
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

import operator
from typing import Annotated, Sequence, List
from typing_extensions import TypedDict 
from pydantic import BaseModel # A base class for creating Pydantic models.
from langchain_core.documents import Document
from langgraph.graph import END, StateGraph, START

from IPython.display import Image, display 

# Create States for the graph

class InputImageState(TypedDict):
    image_path: str

class OverallState(TypedDict):
    query: Annotated[Sequence[BaseModel], operator.add]
    next_action: str
    steps: Annotated[List[str], operator.add]
    ingredients: list  # Add ingredients to the state
    filtered_ingredients: list # Add filtered_ingredients to the state
    preferences: list # Add preferences to the state

class OutputState(TypedDict):
    answer: str
    steps: List[str]

class InputIngredientState(TypedDict):
    query: list
    
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
    
# Define ingredients nodes
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

    return {"ingredients": ingredients}

def recognise_ingredients_node(state: InputImageState): # Add image_path argument
    ingredients_result = recognise_ingredients(state.get('image_path'))
    return {"ingredients": ingredients_result["ingredients"]} # Extract and return ingredients

def filter_ingredients(ingredients: list):
    if not ingredients:
        return {"filtered_ingredients": []}

    template = """You are a helpful assistant that determines if a list of items are food ingredients.

    Here's the list of items: {ingredients}

    Return a comma-separated list of the items that ARE food ingredients.  If none are food ingredients, return "None".
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that determines if items are food ingredients."),
        ("user", template)
    ])
    chain = LLMChain(llm=llm, prompt=prompt)
    ingredients_str = chain.run(ingredients=", ".join(ingredients))

    if "None" in ingredients_str:
        filtered_ingredients = []
    else:
        filtered_ingredients = [ing.strip() for ing in ingredients_str.split(",")]
    return {"filtered_ingredients": filtered_ingredients}

def filter_ingredients_node(state: OverallState):
    filtered_ingredients_result = filter_ingredients(state.get('ingredients')) # Please complete this
    return {"filtered_ingredients": filtered_ingredients_result["filtered_ingredients"]} # Extract and return filtered ingredients


# Create ingredients graph
ingredient_graph = StateGraph(OverallState, input=InputImageState, output=OutputState)

# Define ingredient nodes (Agents)
ingredient_graph.add_node("recognise_ingredients", recognise_ingredients_node)
ingredient_graph.add_node("filter_ingredients", filter_ingredients_node)
ingredient_graph.add_edge("recognise_ingredients", "filter_ingredients")
ingredient_graph.add_edge("filter_ingredients", END)
ingredient_graph.set_entry_point("recognise_ingredients")

# Compile the ingredient graph 
compiled_ingredient_graph = ingredient_graph.compile()  # Store the compiled graph

# Create a runner for the ingredient graph (THIS IS THE KEY CHANGE)
ingredient_runner = compiled_ingredient_graph.create_runner()  # Create a runner
# View
display(Image(compiled_ingredient_graph.get_graph().draw_mermaid_png()))

# Define recipe nodes
def get_recipes(ingredients, preferences):
    """
    Uses GPT-4 Turbo to suggest a dish based on the extracted ingredients.
    Returns a dish name and a short step-by-step recipe.
    """
    # ✅ Create structured prompt for better recipe generation
    messages = [
        {"role": "system", "content": "You are a professional chef who suggests recipes based on available ingredients."},
        {"role": "user", "content": f"""
        I have the following ingredients available: {', '.join(ingredients)} and
        I have the following cuisine prefences: {', '.join(preferences)}.
        Suggest a suitable dish I can cook using these ingredients and provide a step-by-step recipe.
        Make sure the recipe is practical and uses all or most of the ingredients listed and aligns with the cuisine preferences.
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

    return {"recipe_text": recipe_text}

def get_recipes_node(state: OverallState): # Add arguments
    recipes_result = get_recipes(state.get('filtered_ingredients'), state.get('preferences'))
    return {"recipe_text": recipes_result["recipe_text"]} # Extract and return recipe text


recipe_graph = StateGraph(OverallState)
recipe_graph.add_node("generate_recipes", get_recipes_node)
recipe_graph.add_edge("generate_recipes", END)
recipe_graph.set_entry_point("generate_recipes")

# 4. Compile the graph
compiled_recipe_graph = recipe_graph.compile()

# View
display(Image(compiled_recipe_graph.get_graph().draw_mermaid_png()))

# Create a runner for the recipe graph (THIS IS THE KEY CHANGE)
recipe_runner = compiled_recipe_graph.create_runner()  # Create a runner

# Export compiled graphs and runners (important!)
__all__ = ['compiled_ingredient_graph', 'compiled_recipe_graph', 'ingredient_runner', 'recipe_runner']
