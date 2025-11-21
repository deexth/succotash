import os
from google.genai import types


def write_file(working_directory, file_path, content):
    abs_path = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_path.startswith(abs_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        if not os.path.exists(target_path):
            os.makedirs(os.path.dirname(target_path), exist_ok=True)

        if os.path.exists(target_path) and os.path.isdir(target_path):
            return f'Error: "{file_path}" is a directory, not a file'

        with open(target_path, "w") as f:
            nber_content = f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({nber_content} characters written)'
        )
    except Exception as e:
        return f"Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file within the working directory. Creates the file if it doesn't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)
