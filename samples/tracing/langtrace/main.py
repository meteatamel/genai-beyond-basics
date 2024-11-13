import os
import sys
from langtrace_python_sdk import langtrace, with_langtrace_root_span  # Must precede any llm module imports
import google.generativeai as genai
import vertexai
from vertexai.generative_models import GenerativeModel

langtrace.init(api_key=os.environ["LANGTRACE_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def generate_googleai_1():
    response = model.generate_content("What is Generative AI?")
    print(response.text)

    response = model.generate_content("Why is sky blue?")
    print(response.text)

@with_langtrace_root_span("generate_googleai")
def generate_googleai_2():
    response = model.generate_content("What is Generative AI?")
    print(response.text)

    response = model.generate_content("Why is sky blue?")
    print(response.text)

@with_langtrace_root_span("generate_vertexai")
def generate_vertexai():
    vertexai.init(project=os.environ["GOOGLE_CLOUD_PROJECT_ID"], location="us-central1")
    model = GenerativeModel("gemini-1.5-flash-002")

    response = model.generate_content("What is Generative AI?")
    print(response.text)

    response = model.generate_content("Why is sky blue?")
    print(response.text)



if __name__ == '__main__':
    globals()[sys.argv[1]]()


