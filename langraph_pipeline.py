from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import os

# Initialize OpenAI models
llm1 = ChatOpenAI(model_name="gpt-4", temperature=0.3)
llm2 = ChatOpenAI(model_name="gpt-4", temperature=0.3)

# Step 1: Extract Ingredients from Query
def extract_ingredients(query):
    messages = [
        SystemMessage(content="You are an expert chef who extracts ingredients from user queries."),
        HumanMessage(content=f"Extract only food ingredients from this query: {query}")
    ]
    response = llm1(messages).content
    return response.split(", ")

# Step 2: Filter Non-Ingredients
def filter_non_ingredients(ingredients):
    messages = [
        SystemMessage(content="Filter out non-food items from the given ingredient list."),
        HumanMessage(content=f"Remove non-food items from: {', '.join(ingredients)}")
    ]
    response = llm1(messages).content
    return response.split(", ")

# Step 3: Validate Ingredients
def validate_ingredients(ingredients):
    messages = [
        SystemMessage(content="Validate if the following ingredients are real food ingredients."),
        HumanMessage(content=f"Validate these as real ingredients: {', '.join(ingredients)}")
    ]
    response = llm2(messages).content
    return response.split(", ")

# Step 4: Generate Final Recipe
def generate_recipe(valid_ingredients):
    messages = [
        SystemMessage(content="You are a master chef. Create a recipe using the given ingredients."),
        HumanMessage(content=f"Create a recipe using: {', '.join(valid_ingredients)}")
    ]
    response = llm2(messages).content
    return response

# Main pipeline function
def process_query(query):
    extracted_ingredients = extract_ingredients(query)
    filtered_ingredients = filter_non_ingredients(extracted_ingredients)
    
    # This step is where users manually review ingredients via UI
    user_approved_ingredients = filtered_ingredients  # Placeholder for UI interaction

    valid_ingredients = validate_ingredients(user_approved_ingredients)
    final_recipe = generate_recipe(valid_ingredients)

    return {"valid_ingredients": valid_ingredients, "final_recipe": final_recipe}
