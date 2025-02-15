from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
import base64
from langgraph.graph import StateGraph, END
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableLambda

import operator
from typing import Annotated, Sequence, List
from typing_extensions import TypedDict 
from pydantic import BaseModel

#  Load environment variables
load_dotenv()

#  Get the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ ERROR: OPENAI_API_KEY is missing. Please set it in the .env file.")

#  Initialize GPT-4 Turbo
llm = ChatOpenAI(model_name="gpt-4-turbo", temperature=0.3, openai_api_key=api_key)

#  Define states
class OverallIngredientState(TypedDict):
    image_path: str
    ingredients: list
    filtered_ingredients: list
    preferences: list
    recipe_text: str
    
class OverallRecipeState(TypedDict):
    ingredients: list
    preferences: list
    recipe_text: str


#  Encode image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

#  Recognize ingredients
def recognise_ingredients(state: OverallIngredientState):
    encoded_image = encode_image(state['image_path'])
    messages = [
        {"role": "system", "content": "You are a food expert who identifies ingredients."},
        {"role": "user", "content": [
            {"type": "text", "text": "Analyze this image and list ingredients. Please be specific for each ingredients. Ensure there is no repeated items."},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
        ]}
    ]
    response = llm.invoke(messages)
    ingredients = response.content.split(",") if response.content else []
    return {"ingredients": [ingredient.strip() for ingredient in ingredients]}

#  Filter ingredients
def filter_ingredients(state: OverallIngredientState):
    if not state['ingredients']:
        return {"filtered_ingredients": []}
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a food expert who can identify ingredients from a list. You answer only in singular form such as orange instead of oranges."),
        ("user", "Here's the list: {ingredients}. Return only valid ingredients. Provide only a comma-separated list of ingredients in their singular form (in other words orange instead of oranges).")
    ])
    chain = prompt | llm
    ingredients_str = chain.invoke({"ingredients": ", ".join(state['ingredients'])}).content
    return {"filtered_ingredients": ingredients_str.split(",") if "None" not in ingredients_str else []}

#  Generate recipe
def get_recipes(state: OverallRecipeState):
    messages = [
        {"role": "system", "content": "You are a professional chef who suggests recipes based on available ingredients."},
        {"role": "user", "content": f"""
        I have the following ingredients available: {', '.join(state['ingredients'])}.
        I have dietary preference of {state['preferences']['Dietary Preference']}.
        I prefer {state['preferences']['Recipe Style']} cooking style with {state['preferences']['Seasoning Preference']} level of seasoning/spices.
        I would like the cooking time to be around {state['preferences']['Cooking Time']}.
        Suggest a suitable dish I can cook using these ingredients and preferences.
        Provide it as a step-by-step recipe.
        Make sure the recipe is practical and uses all or most of the ingredients listed.
        Format the response as:
        Dish Name: [Dish Name]
        Ingredients: [List of Ingredients]
        Instructions: [Step-by-step cooking instructions]
        """}
    ]
    response = llm.invoke(messages)
    print(messages)
    return {"recipe_text": response.content}

#  Create graphs
ingredient_graph = StateGraph(OverallIngredientState)
ingredient_graph.add_node("recognise_ingredients", RunnableLambda(recognise_ingredients))
ingredient_graph.add_node("filter_ingredients", RunnableLambda(filter_ingredients))
ingredient_graph.add_edge("recognise_ingredients", "filter_ingredients")
ingredient_graph.add_edge("filter_ingredients", END)
ingredient_graph.set_entry_point("recognise_ingredients")
compiled_ingredient_graph = ingredient_graph.compile()

recipe_graph = StateGraph(OverallRecipeState)
recipe_graph.add_node("generate_recipes", RunnableLambda(get_recipes))
recipe_graph.add_edge("generate_recipes", END)
recipe_graph.set_entry_point("generate_recipes")
compiled_recipe_graph = recipe_graph.compile()

#  Export compiled graphs
__all__ = ['compiled_ingredient_graph', 'compiled_recipe_graph']