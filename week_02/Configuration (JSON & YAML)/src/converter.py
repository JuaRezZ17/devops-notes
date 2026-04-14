import json
import yaml
import sys

def transform_config(input_file, output_file):
    try:
        # 1. Read JSON file
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        print(f"--- Data loaded from {input_file} ---")

        # 2. Validación del puerto
        if not isinstance(data.get("port"), int):
            raise TypeError(f"Error de validación: El puerto '{data.get('port')}' debe ser un número entero.")

        # 3. Modify the debug_mode parameter
        print("Modifying 'debug_mode' to False...")
        data["debug_mode"] = False

        # 4. Save as YAML
        with open(output_file, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
        
        print(f"--- File {output_file} generated with success ---")

    except FileNotFoundError:
        print(f"Error: File {input_file} not found")
    except json.JSONDecodeError:
        print(f"Error: File {input_file} has an invalid JSON format")
    except TypeError as e:
        print(e)
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    transform_config('config.json', 'config.yaml')
