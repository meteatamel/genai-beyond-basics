from llm_guard import scan_output, scan_prompt
from llm_guard.vault import Vault
from llm_guard.input_scanners import Anonymize
from llm_guard.output_scanners import Deanonymize
from vertexai.generative_models import GenerativeModel


# References:
# https://llm-guard.com/input_scanners/anonymize/
# https://llm-guard.com/output_scanners/deanonymize/

def main():
    prompt = ("Make an SQL insert statement to add a new user to our database. Name is John Doe. Email is "
              "test@test.com but also possible to contact him with hello@test.com email. Phone number is 555-123-4567 "
              "and the IP address is 192.168.1.100. And credit card number is 4567-8901-2345-6789. " +
              "He works in Test LLC. " +
              "Only return the SQL statement and nothing else")
    print(f"Original prompt: {prompt}")

    vault = Vault()
    input_scanners = [Anonymize(vault)]
    sanitized_prompt, results_valid, results_score = scan_prompt(input_scanners, prompt)
    # if any(results_valid.values()) is False:
    #     print(f"Prompt {prompt} is not valid, scores: {results_score}")
    #     exit(1)
    print(f"Sanitized prompt: {sanitized_prompt}")

    model = GenerativeModel('gemini-1.5-flash-001')
    response = model.generate_content(sanitized_prompt)
    print(f"Response text: {response.text}")

    output_scanners = [Deanonymize(vault)]
    sanitized_output, results_valid, results_score = scan_output(
        output_scanners, sanitized_prompt, response.text
    )
    # if any(results_valid.values()) is False:
    #     print(f"Output {response.text} is not valid, scores: {results_score}")
    #     exit(1)
    print(f"Sanitized output: {sanitized_output}")


if __name__ == '__main__':
    main()
