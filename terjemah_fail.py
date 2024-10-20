import json
import re
import time
import requests

# Set up Microsoft Translator API details
subscription_key = 'a2e643403ddc43818203761d3eabfa0f'
endpoint = 'https://api.cognitive.microsofttranslator.com/'
location = 'southeastasia'

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

# Function to handle translating text while ignoring content inside {{ }}
def translate_ignoring_placeholders(text, target_language):
    # Find and temporarily replace all content inside {{ }}
    placeholders = re.findall(r'{{.*?}}', text)
    modified_text = re.sub(r'{{.*?}}', '_PLACEHOLDER_', text)

    # Translate the modified text
    translated_text = translate_text(modified_text, target_language)

    # Replace the placeholders back in the translated text
    for placeholder in placeholders:
        translated_text = translated_text.replace('_PLACEHOLDER_', placeholder, 1)
    
    return translated_text

# Function to process the JSON content and translate placeholders
def process_translation(input_file, output_file, target_language):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    start_time = time.time()

    # Loop through the JSON structure
    def translate_json(data):
        if isinstance(data, dict):
            for key, value in data.items():
                # Only translate if key is in capital letters, and handle lines with {{ }} correctly
                if re.match(r'^[A-Z_]+$', key) and isinstance(value, str):
                    try:
                        translated_value = translate_ignoring_placeholders(value, target_language)
                        data[key] = translated_value
                    except Exception as e:
                        print(f"Error translating key {key}: {e}")
                else:
                    translate_json(value)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                translate_json(item)

    translate_json(data)

    # Measure the time taken
    time_taken = time.time() - start_time
    print(f"Translation to {target_language} completed in {time_taken:.2f} seconds.")

    # Save the translated file with the appropriate suffix
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)

# Main function
if __name__ == "__main__":
    input_file = 'language_files\en-us-v1.json'  # Input file path
    
    # Translate to Indonesian
    print("Translating from English to Indonesian...")
    output_file_id = 'translated_files\id-id-v1.json'
    process_translation(input_file, output_file_id, 'id')  # Indonesian translation

    # Translate to Filipino
    print("Translating from English to Filipino...")
    output_file_fil = 'translated_files\il-ph-v1.json'
    process_translation(input_file, output_file_fil, 'fil')  # Filipino translation

    # Translate to Fijian
    print("Translating from English to Fijian...")
    output_file_fj = 'translated_files\j-fj-v1.json'
    process_translation(input_file, output_file_fj, 'fj')  # Fijian translation
