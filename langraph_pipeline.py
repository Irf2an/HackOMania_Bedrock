from langchain.chat_models import ChatOpenAI
from langraph.graph import StateGraph

# Define State for LLM1 output
class ExtractionState:
    query: str
    ingredients: list

# Define State for LLM2 validation output
class ValidationState:
    ingredients: list
    valid_ingredients: list

# Initialize LLM models (You need an OpenAI API key)
llm1 = ChatOpenAI(model_name="gpt-4", temperature=0.3)
llm2 = ChatOpenAI(model_name="gpt-4", temperature=0.3)

# Define Langraph workflow
workflow = StateGraph(ExtractionState)

@workflow.add_node()
def extract_ingredients(state: ExtractionState):
    response = llm1.predict(f"Extract food ingredients from this query: {state.query}")
    state.ingredients = response.split(", ")
    return state

@workflow.add_node()
def validate_ingredients(state: ExtractionState):
    valid_response = llm2.predict(f"Validate these as real ingredients: {', '.join(state.ingredients)}")
    state.valid_ingredients = [i.strip() for i in valid_response.split(",")]
    return state

# Define flow
workflow.set_entry_point(extract_ingredients)
workflow.add_edge(extract_ingredients, validate_ingredients)
workflow.compile()

# Function to run the pipeline
def process_query(query):
    initial_state = ExtractionState(query=query, ingredients=[])
    output_state = workflow.invoke(initial_state)
    return output_state.valid_ingredients
