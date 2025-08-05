from google.api_core.client_options import ClientOptions
from google.cloud import modelarmor_v1
from utils import get_env_var, read_text

PROJECT_ID = get_env_var("PROJECT_ID")
LOCATION = get_env_var("LOCATION")
TEMPLATE_ID = get_env_var("TEMPLATE_ID")


def main():
    # Read user prompt
    user_prompt = read_text()

    # Create the Model Armor client.
    client = modelarmor_v1.ModelArmorClient(
        transport="rest",
        client_options=ClientOptions(
            api_endpoint=f"modelarmor.{LOCATION}.rep.googleapis.com"
        ),
    )

    # Initialize request argument(s).
    user_prompt_data = modelarmor_v1.DataItem(text=user_prompt)

    # Prepare request for sanitizing the defined prompt.
    request = modelarmor_v1.SanitizeUserPromptRequest(
        name=f"projects/{PROJECT_ID}/locations/{LOCATION}/templates/{TEMPLATE_ID}",
        user_prompt_data=user_prompt_data,
    )

    # Sanitize the user prompt.
    response = client.sanitize_user_prompt(request=request)

    # Sanitization Result.
    print(response)


if __name__ == "__main__":
    main()