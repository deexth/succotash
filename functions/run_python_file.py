import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    abs_path = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_path.startswith(abs_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(target_path):
        return f'Error: File "{file_path}" not found.'

    if not target_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        commands = ["python", target_path]
        if args:
            commands.extend(args)
        output_bytes = subprocess.run(
            commands, capture_output=True, check=True, timeout=30.0, cwd=abs_path
        )
        if output_bytes:
            return f"STDOUT: {output_bytes.stdout}, STDERR: {output_bytes.stderr}"
        return "No output produced."
    except subprocess.CalledProcessError as e:
        return f"Process exited with code {e}"
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)
