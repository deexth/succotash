import os
import sys
from dotenv import load_dotenv
from google import genai

# from functions.get_files_info import schema_get_files_info
from config import SYSTEM_PROMPT, MODEL_NAME
from functions.call_function import available_functions, call_function


def gemini_call(key, prompt):
    client = genai.Client(api_key=key)

    messages = [
        genai.types.Content(role="user", parts=[genai.types.Part(text=prompt)]),
    ]

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=messages,
        config=genai.types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=SYSTEM_PROMPT,
        ),
    )

    return response


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    user_prompt = " ".join(args)
    api_key = os.environ.get("GEMINI_API_KEY")

    responses = []

    try:
        response = gemini_call(api_key, user_prompt)
    except Exception as e:
        print(f"An error occurred while calling Gemini API: {e}")
        sys.exit(1)

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if not response.function_calls:
        return response.text

    for function_call_part in response.function_calls:
        # print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        call_resp = call_function(function_call_part, verbose)
        if not call_resp.parts or not call_resp.parts[0].function_response:
            raise Exception("Response part missing")
        responses.append(call_resp.parts[0].function_response.response)
        if verbose:
            print(f"-> {call_resp.parts[0].function_response.response}")

    if not responses:
        raise Exception("no function responses generated, exiting.")


if __name__ == "__main__":
    main()
