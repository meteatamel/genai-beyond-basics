# Controlled generation

In this sample, you'll learn how to use controlled generation of Vertex AI
to control the response format of the LLM.

Take a look at the sample [main.py](./main.py).

## Without controlled generation

First, let's ask a question to LLM without controlled generation:

```python
model = GenerativeModel('gemini-1.5-flash-001')
prompt = "List a few popular cookie recipes"
response = model.generate_content(prompt)
```

Run it:

```shell
python main.py --project_id genai-atamel without_controlled_generation1
```

You get a response in free text:

```log
Prompt: List a few popular cookie recipes
Response: ## Popular Cookie Recipes:

**Classic and Simple:**

* **Chocolate Chip Cookies:** This timeless classic is a crowd-pleaser for a reason! The perfect balance of sweet and chewy.
* **Sugar Cookies:** 
...
```

You can try to format the response a little bit with more detailed prompt:

```python
model = GenerativeModel('gemini-1.5-flash-001')
prompt = """
    List a few popular cookie recipes using this JSON schema:
    Recipe = {"recipe_name": str}
    Return: list[Recipe]
  """
response = model.generate_content(prompt)
```

And you get the following response:

```log
Prompt: 
        List a few popular cookie recipes using this JSON schema:
        Recipe = {"recipe_name": str}
        Return: list[Recipe]
      
Response: ```json
[
  {"recipe_name": "Chocolate Chip Cookies"},
  {"recipe_name": "Oatmeal Raisin Cookies"},
  {"recipe_name": "Snickerdoodles"},
  {"recipe_name": "Sugar Cookies"},
  {"recipe_name": "Peanut Butter Cookies"},
  {"recipe_name": "Gingerbread Cookies"},
  {"recipe_name": "Shortbread Cookies"}
]
```

The response is in JSON markdown format but not quite JSON.

## Generate with response mime type

One easy way of forcing JSON in response is to use the response mime type:

```python
model = GenerativeModel('gemini-1.5-flash-001',
                        generation_config=GenerationConfig(
                            response_mime_type="application/json"
                        ))
prompt = """
    List a few popular cookie recipes using this JSON schema:
    Recipe = {"recipe_name": str}
    Return: list[Recipe]
  """
response = model.generate_content(prompt)
```

Run it:

```shell
python main.py --project_id genai-atamel with_response_mime_type
```

Now you should get proper JSON back:

```log
Prompt: 
        List a few popular cookie recipes using this JSON schema:
        Recipe = {"recipe_name": str}
        Return: list[Recipe]

Response: [{"recipe_name": "Chocolate Chip Cookies"}, {"recipe_name": "Oatmeal Raisin Cookies"}, {"recipe_name": "Snickerdoodles"}, {"recipe_name": "Sugar Cookies"}, {"recipe_name": "Peanut Butter Cookies"}]
```

## Generate with response schema

You can further enforce a schema for the response. Note that the prompt does not have to talk 
about a schema at all:

```python
response_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "recipe_name": {"type": "string"},
            "calories": {"type": "integer"}
        },
        "required": ["recipe_name"]
    },
}
model = GenerativeModel('gemini-1.5-pro-001',
                        generation_config=GenerationConfig(
                            response_mime_type="application/json",
                            response_schema=response_schema))
prompt = "List a few popular cookie recipes"
response = model.generate_content(prompt)
```

Run it:

```shell
python main.py --project_id genai-atamel with_response_schema1
```

The response respects the schema:

```log
Prompt: List a few popular cookie recipes
Response: [{"recipe_name": "Chocolate Chip Cookies", "calories": 150}, {"recipe_name": "Peanut Butter Cookies", "calories": 160}, {"recipe_name": "Oatmeal Raisin Cookies", "calories": 140}, {"recipe_name": "Sugar Cookies", "calories": 130}] 
```

## Extract with response schema

You can also use response schema to extract information in more structured format.

For example, you can extract social media comments in a structured JSON like this:

```python
response_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "dessert_name": { "type": "string"},
            "rating" : { "type": "integer"},
            "message": { "type": "string"}
        },
        "required": ["dessert_name", "rating", "message"]
    },
}

model = GenerativeModel('gemini-1.5-pro-001',
                        generation_config=GenerationConfig(
                            response_mime_type="application/json",
                            response_schema=response_schema))

prompt = """
  Extract reviews from our social media:

  - "Absolutely loved it! Best ice cream I've ever had." Rating: 4
  - "Quite good cheese cake, but a bit too sweet for my taste." Rating: 2
  - "Did not like the tiramisu." Rating: 0
"""
response = model.generate_content(prompt)
```

Run it:

```shell
python main.py --project_id genai-atamel with_response_schema2
```

You'll get back the extracted information in JSON:

```log
Prompt: 
      Extract reviews from our social media:

      - "Absolutely loved it! Best ice cream I've ever had." Rating: 4
      - "Quite good cheese cake, but a bit too sweet for my taste." Rating: 2
      - "Did not like the tiramisu." Rating: 0
    
Response: [{"dessert_name": "ice cream", "message": "Absolutely loved it! Best ice cream I've ever had", "rating": 4}, {"dessert_name": "cheese cake", "message": "Quite good cheese cake, but a bit too sweet for my taste", "rating": 2}, {"dessert_name": "tiramisu", "message": "Did not like the tiramisu", "rating": 0}] 
```
