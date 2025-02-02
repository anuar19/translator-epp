import json
import os
import requests
import time

# Microsoft Translator API details
subscription_key = 'a2e643403ddc43818203761d3eabfa0f'  # Replace with your Azure Translator key
endpoint = 'https://api.cognitive.microsofttranslator.com/'  # Replace with your endpoint
location = 'southeastasia'  # Use your region if needed

def translate_to_filipino(text, retries=3):
    """
    Translate the given text from English to Filipino using Microsoft Translator API.
    """
    path = '/translate?api-version=3.0'
    params = '&from=en&to=fil'
    constructed_url = endpoint + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json'
    }

    body = [{'text': text}]

    attempt = 0
    while attempt < retries:
        try:
            print(f"Translating English text to Filipino: {text}")
            response = requests.post(constructed_url, headers=headers, json=body)
            response.raise_for_status()
            result = response.json()

            # Get the Filipino translation from the response
            filipino_translation = result[0]['translations'][0]['text']
            return filipino_translation

        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}. Attempt {attempt + 1} of {retries}")
        except Exception as e:
            print(f"General error occurred: {e}. Attempt {attempt + 1} of {retries}")

        attempt += 1
        time.sleep(1)

    # Return None if all attempts fail
    print(f"Skipping translation for text: {text} after {retries} attempts.")
    return None

def update_json_file_for_filipino(input_file, output_folder):
    # Load the JSON file
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return

    translations_done = 0

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Recursively scan through the dictionary to find "en-us"
    def scan_and_translate(obj):
        nonlocal translations_done
        if isinstance(obj, dict):
            if 'en-us' in obj:
                # English translation exists, translate to Filipino
                english_text = obj['en-us']
                filipino_text = translate_to_filipino(english_text)

                if filipino_text:
                    # Insert the Filipino translation
                    obj['fil-ph'] = filipino_text
                    translations_done += 1
                    print(f"Inserted Filipino translation: {filipino_text}")
                else:
                    print(f"Failed to translate English text: {english_text}")
            # Recursively scan any nested dictionaries
            for key, value in obj.items():
                scan_and_translate(value)
        elif isinstance(obj, list):
            for item in obj:
                scan_and_translate(item)

    # Start the scan-and-translate process
    scan_and_translate(data)

    if translations_done == 0:
        print("No translations were inserted. Check if 'en-us' fields are present in the JSON file.")

    # Save the updated JSON file with '-fil' appended to the filename
    base_filename = os.path.splitext(os.path.basename(input_file))[0]
    updated_file_name = os.path.join(output_folder, base_filename + '-fil.json')

    try:
        with open(updated_file_name, 'w', encoding='utf-8') as updated_file:
            json.dump(data, updated_file, ensure_ascii=False, indent=4)
        print(f"\nUpdated file saved as: {updated_file_name}")
    except Exception as e:
        print(f"Error saving updated JSON file: {e}")

    print(f"Total Filipino translations inserted: {translations_done}")

# Example usage:
json_file = 'translated_files\candidates-portal-configuration-id.json'
output_folder = 'translated_files'
update_json_file_for_filipino(json_file, output_folder)
