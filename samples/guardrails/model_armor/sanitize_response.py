from google.api_core.client_options import ClientOptions
from google.cloud import modelarmor_v1
from utils import get_env_var, read_text

PROJECT_ID = get_env_var("PROJECT_ID")
LOCATION = get_env_var("LOCATION")
TEMPLATE_ID = get_env_var("TEMPLATE_ID")


def main():
    # Read model response
    model_response = read_text()

    # Create the Model Armor client.
    client = modelarmor_v1.ModelArmorClient(
        transport="rest",
        client_options=ClientOptions(
            api_endpoint=f"modelarmor.{LOCATION}.rep.googleapis.com"
        ),
    )

    # Initialize request argument(s).
    model_response_data = modelarmor_v1.DataItem(text=model_response)

    # Prepare request for sanitizing model response.
    request = modelarmor_v1.SanitizeModelResponseRequest(
        name=f"projects/{PROJECT_ID}/locations/{LOCATION}/templates/{TEMPLATE_ID}",
        model_response_data=model_response_data,
    )

    # Sanitize the model response.
    response = client.sanitize_model_response(request=request)

    # Sanitization Result.
    print(response)


if __name__ == "__main__":
    main()