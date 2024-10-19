import json
import re
import time
import requests

# Set up Microsoft Translator API details
subscription_key = 'a2e643403ddc43818203761d3eabfa0f'
endpoint = "https://api.cognitive.microsofttranslator.com/translate"
location = 'southeastasia'  # For example, 'global'

# Function to call the Microsoft Translator API
def translate_text(text, target_language):
    path = '/translate'
    params = {
        'api-version': '3.0',
        'to': target_language
    }
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-Type': 'application/json'
    }
    body = [{'text': text}]
    
    response = requests.post(endpoint + path, params=params, headers=headers, json=body)
    response.raise_for_status()
    return response.json()[0]['translations'][0]['text']

# Function to process the JSON content and translate placeholders
def process_translation(input_file, output_file, target_language):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    start_time = time.time()

    for key, value in data.items():
        # Find placeholders with all capital letters and ignore content inside {{ }}
        if re.search(r'^[A-Z_]+$', key) and '{{' not in value:
            try:
                translated_text = translate_text(value, target_language)
                data[key] = translated_text
            except Exception as e:
                print(f"Error translating key {key}: {e}")

    # Measure the time taken
    time_taken = time.time() - start_time
    print(f"Translation to {target_language} completed in {time_taken:.2f} seconds.")

    # Save the translated file with the appropriate suffix
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)

# Main function
if __name__ == "__main__":
    input_file = 'language_files\en-us-v1.json'  # Change this to your input file path
    output_file_id = 'translated_files\id-id-v1.json'
    
    process_translation(input_file, output_file_id, 'id')  # Indonesian translation
