# Response schema and pydantic (LangChain)

In this sample, you'll learn how to use response schema and pydantic parser of Langchain
to control the response format of the LLM.

See [main.py](./main.py) for the full sample.

## Setup

Make sure your `gcloud` is set up with your Google Cloud project:

```shell
gcloud config set core/project your-google-cloud-project-id
```

You're logged in:

```shell
gcloud auth application-default login
```

Create and activate a virtual environment:

```shell
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```shell
pip install -r requirements.txt
```

## Without controlled generation

First, let's ask a question to LLM without any controlled generation:

```python
model = VertexAI(model_name=MODEL_NAME)
prompt = "List 10 popular cookie recipes"
response = model.invoke(prompt)
```

Run it:

```shell
python main.py without_controlled_generation
```

You get a response in free text:

```log
Prompt: List 10 popular cookie recipes
Response: 1. **Chocolate Chip Cookies:** The classic, arguably the most popular cookie of all time.  Numerous variations exist, but the basic recipe is universally loved.

2. **Oatmeal Raisin Cookies:** A chewy, comforting classic often featuring oats, raisins, brown sugar, and spices.

3. **Peanut Butter Cookies:** Simple, satisfying, and often made with peanut butter, sugar, and an egg.  Variations include adding chocolate chips or pressing a fork into the top.
...
```

Not ideal if you want to parse the output in your application.

## With response schema

You can use the response schema feature of LangChain to define a simple schema for the output:

```python
model = VertexAI(model_name=MODEL_NAME)
prompt = "List a popular cookie recipe"

response_schemas = [
    ResponseSchema(name="recipe_name", description="Name of the recipe", type="str"),
    ResponseSchema(name="calories", description="Calories of the recipe", type="int"),
]
```

Get format instructions out of the schema:

```python
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()
print(f"Format instructions: {format_instructions}")
```

And pass it to the model with a prompt template:

```python
prompt_template = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}",
    input_variables=["query"],
    partial_variables={"format_instructions": format_instructions},
)

chain = prompt_template | model | output_parser
response = chain.invoke({"query": prompt})
```

Run it:

```shell
python main.py with_response_schema 
```

You should see the format instructions printed:

```shell
Format instructions: The output should be a markdown code snippet formatted in the following schema, including the leading and trailing "```json" and "```":

```json
{
        "recipe_name": str  // Name of the recipe
        "calories": int  // Calories of the recipe
}
```

And you should get JSON format back in the response:

```shell
Prompt: List a popular cookie recipe
Response: {'recipe_name': 'Chocolate Chip Cookies', 'calories': 78}
```

This is better but it gets difficult when you need to define a list of recipes. We can do better.

## With pydantic parser

[Pydantic](https://docs.pydantic.dev/latest/) is the most widely used data validation library for Python. You can use 
Pydantic to define a model and use LangChain's Pydantic output parser to make sure LLM outputs conform to that model.

First, define a `Recipe` and a list of `Recipes` classes as our model: 

```python
class Recipe(BaseModel):
    recipe_name: str = Field(description="Name of the recipe")
    calories: int = Field(description="Calories of the recipe")

class Recipes(BaseModel):
    recipes: List[Recipe]
```

Define an output parser with that model and format instructions:

```python
model = VertexAI(model_name=MODEL_NAME)
prompt = "List 10 popular cookie recipes"

output_parser = PydanticOutputParser(pydantic_object=Recipes)
format_instructions = output_parser.get_format_instructions()
```

Pass the format instructions to the model with a prompt template: 

```python
prompt_template = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": format_instructions},
)

chain = prompt_template | model | output_parser
response = chain.invoke({"query": prompt})
```

Run it:

```shell
python main.py with_pydantic 
```

You should see the format instructions printed:

```shell
Format instructions: The output should be formatted as a JSON instance that conforms to the JSON schema below.

As an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}
the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.

Here is the output schema:

{"$defs": {"Recipe": {"properties": {"recipe_name": {"description": "Name of the recipe", "title": "Recipe Name", "type": "string"}, "calories": {"description": "Calories of the recipe", "title": "Calories", "type": "integer"}}, "required": ["recipe_name", "calories"], "title": "Recipe", "type": "object"}}, "properties": {"recipes": {"items": {"$ref": "#/$defs/Recipe"}, "title": "Recipes", "type": "array"}}, "required": ["recipes"]}
```

And you should get Recipe objects in a recipes list automatically parsed!

```shell
Prompt: List 10 popular cookie recipes
Response: recipes=[Recipe(recipe_name='Chocolate Chip Cookies', calories=78), Recipe(recipe_name='Oatmeal Raisin Cookies', calories=110), ...]
```

## References

* [Pydantic](https://docs.pydantic.dev/latest/)
* [LangChain Pydantic parser](https://python.langchain.com/v0.1/docs/modules/model_io/output_parsers/types/pydantic/)