import sys
from vertexai.generative_models import GenerativeModel, GenerationConfig


def without_controlled_generation1():
    model = GenerativeModel('gemini-1.5-flash-001')

    prompt = "List a few popular cookie recipes"
    response = model.generate_content(prompt)
    print_prompt_response(prompt, response)


def without_controlled_generation2():
    model = GenerativeModel('gemini-1.5-flash-001')

    prompt = """
        List a few popular cookie recipes using this JSON schema:
        Recipe = {"recipe_name": str}
        Return: list[Recipe]
      """
    response = model.generate_content(prompt)
    print_prompt_response(prompt, response)


def with_response_mime_type():
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
    print_prompt_response(prompt, response)


def with_response_schema1():
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
    print_prompt_response(prompt, response)


def with_response_schema2():
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
    print_prompt_response(prompt, response)


def print_prompt_response(prompt, response):
    print(f"Prompt: {prompt}")
    print(f"Response: {response.candidates[0].content.parts[0].text}")


if __name__ == "__main__":
    globals()[sys.argv[1]]()
