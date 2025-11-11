import os
import sys
from dotenv import load_dotenv
from google import genai


def gemini_call(key, prompt):
    client = genai.Client(api_key=key)

    messages = [
        genai.types.Content(role="user", parts=[genai.types.Part(text=prompt)]),
    ]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
    )

    return response


def main():
    if len(sys.argv) < 2:
        print("You need to provide an argument for the prompt")
        sys.exit(1)
    prompt = sys.argv[1]
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    resp = gemini_call(api_key, prompt)

    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        print(f"Response: {resp.text}")
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {resp.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {resp.usage_metadata.candidates_token_count}")
    else:
        print(resp.text)


if __name__ == "__main__":
    main()
