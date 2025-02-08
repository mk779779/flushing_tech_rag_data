import json
import os
import re

import requests


def query_llama_model(prompt, model="deepseek-r1:8b"):
    headers = {"Content-Type": "application/json"}

    payload = {"model": model, "prompt": prompt}

    url = "http://localhost:11434/api/generate"

    try:
        response = requests.post(url, json=payload, headers=headers, stream=True)

        if response.status_code == 200:
            full_response = ""
            for chunk in response.iter_lines():
                if chunk:
                    data = json.loads(chunk.decode("utf-8"))
                    full_response += data.get("response", "")

                    if data.get("done", False):
                        break

            return full_response
        else:
            return f"Error: {response.status_code} - {response.text}"

    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"


def extract_sections(text):
    """
    Extracts the <think> section and the normal section from the input text.

    Args:
        text (str): The input text containing <think> tags and normal text.

    Returns:
        tuple: A tuple containing the <think> section and the normal section as strings.
    """
    # Extract the `<think>` section
    think_section = re.search(r"<think>(.*?)</think>", text, re.DOTALL)
    think_section = think_section.group(1).strip() if think_section else ""

    # Extract the "normal" section (everything after </think>)
    response_section = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

    return think_section, response_section


if __name__ == "__main__":
    prompt = "What is elixir, explain it in 1 sentence"
    response = query_llama_model(prompt)
    think_section, response_section = extract_sections(response)
    print("think_section:", think_section)
    print("response_section:", response_section)
