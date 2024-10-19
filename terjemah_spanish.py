import json
import os
import requests
import time

# Microsoft Translator API details
subscription_key = 'a2e643403ddc43818203761d3eabfa0f'  # Replace with your Azure Translator key
endpoint = 'https://api.cognitive.microsofttranslator.com/'  # Replace with your endpoint
location = 'southeastasia'  # Use your region if needed

def translate_to_spanish(text, retries=3):
    """
    Translate the given text from English to Spanish using Microsoft Translator API.
    """
    path = '/translate?api-version=3.0'
    params = '&from=en&to=es'
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
            print(f"Translating English text to Spanish: {text}")
            response = requests.post(constructed_url, headers=headers, json=body)
            response.raise_for_status()
            result = response.json()

            # Get the Spanish translation from the response
            spanish_translation = result[0]['translations'][0]['text']
            return spanish_translation

        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}. Attempt {attempt + 1} of {retries}")
        except Exception as e:
            print(f"General error occurred: {e}. Attempt {attempt + 1} of {retries}")

        attempt += 1
        time.sleep(1)

    # Return None if all attempts fail
    print(f"Skipping translation for text: {text} after {retries} attempts.")
    return None

def update_json_file_for_spanish(input_file):
    # Load the JSON file
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return

    translations_done = 0

    # Recursively scan through the dictionary to find "en-us"
    def scan_and_translate(obj):
        nonlocal translations_done
        if isinstance(obj, dict):
            if 'en-us' in obj:
                # English translation exists, translate to Spanish
                english_text = obj['en-us']
                spanish_text = translate_to_spanish(english_text)

                if spanish_text:
                    # Insert the Spanish translation
                    obj['es'] = spanish_text
                    translations_done += 1
                    print(f"Inserted Spanish translation: {spanish_text}")
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

    # Save the updated JSON file with '-spanish-updated' appended to the filename
    updated_file_name = os.path.splitext(input_file)[0] + '-spanish-updated.json'
    try:
        with open(updated_file_name, 'w', encoding='utf-8') as updated_file:
            json.dump(data, updated_file, ensure_ascii=False, indent=4)
        print(f"\nUpdated file saved as: {updated_file_name}")
    except Exception as e:
        print(f"Error saving updated JSON file: {e}")

    print(f"Total Spanish translations inserted: {translations_done}")

# Specify the path to your JSON file
json_file = 'translations.json'
update_json_file_for_spanish(json_file)
