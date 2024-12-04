import sys
from langchain_google_vertexai import VertexAI
from langchain.output_parsers import ResponseSchema, PydanticOutputParser, StructuredOutputParser
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import List


MODEL_NAME = "gemini-1.5-flash-002"

def without_controlled_generation():
    model = VertexAI(model_name=MODEL_NAME)
    prompt = "List 10 popular cookie recipes"
    response = model.invoke(prompt)
    print_prompt_response(prompt, response)


def with_response_schema():
    model = VertexAI(model_name=MODEL_NAME)
    prompt = "List a popular cookie recipe"

    response_schemas = [
        ResponseSchema(name="recipe_name", description="Name of the recipe", type="str"),
        ResponseSchema(name="calories", description="Calories of the recipe", type="int"),
    ]

    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()
    print(f"Format instructions: {format_instructions}")

    prompt_template = PromptTemplate(
        template="Answer the user query.\n{format_instructions}\n{query}",
        input_variables=["query"],
        partial_variables={"format_instructions": format_instructions},
    )

    chain = prompt_template | model | output_parser
    response = chain.invoke({"query": prompt})
    print_prompt_response(prompt, response)


class Recipe(BaseModel):
    recipe_name: str = Field(description="Name of the recipe")
    calories: int = Field(description="Calories of the recipe")

class Recipes(BaseModel):
    recipes: List[Recipe]


def with_pydantic():
    model = VertexAI(model_name=MODEL_NAME)
    prompt = "List 10 popular cookie recipes"

    output_parser = PydanticOutputParser(pydantic_object=Recipes)
    format_instructions = output_parser.get_format_instructions()
    print(f"Format instructions: {format_instructions}")

    prompt_template = PromptTemplate(
        template="Answer the user query.\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": format_instructions},
    )

    chain = prompt_template | model | output_parser
    response = chain.invoke({"query": prompt})
    print_prompt_response(prompt, response)


def print_prompt_response(prompt, response):
    print(f"Prompt: {prompt}")
    print(f"Response: {response}")


if __name__ == "__main__":
    globals()[sys.argv[1]]()