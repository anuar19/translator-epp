import json
import re
import requests

# Replace with your Microsoft Translator API key and endpoint
subscription_key = 'a2e643403ddc43818203761d3eabfa0f'
endpoint = 'https://api.cognitive.microsofttranslator.com/'
location = 'southeastasia'

def translate_text(text, target_language='id'):
    path = '/translate?api-version=3.0'
    params = f'&to={target_language}'
    constructed_url = endpoint + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json'
    }
    
    body = [{'Text': text}]
    
    response = requests.post(constructed_url, headers=headers, json=body)
    if response.status_code == 200:
        return response.json()[0]['translations'][0]['text']
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return text  # If translation fails, return the original text

def translate_json(json_data, target_language='id'):
    for key, value in json_data.items():
        if isinstance(value, dict):
            translate_json(value, target_language)
        elif isinstance(value, str):
            # Find portions enclosed in {{}} and leave them unchanged
            parts_to_ignore = re.findall(r'{{.*?}}', value)
            for part in parts_to_ignore:
                value = value.replace(part, f"<ignore>{part}<ignore>")

            # Translate the remaining text
            translated_value = translate_text(value, target_language)

            # Restore the ignored portions
            for part in parts_to_ignore:
                translated_value = translated_value.replace(f"<ignore>{part}<ignore>", part)
            
            json_data[key] = translated_value

    return json_data

def main():
    # Load the JSON file
    with open('en-us-v1.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    # Translate the content
    translated_data = translate_json(json_data, target_language='id')  # Indonesian (id) as example

    # Save the translated JSON to a new file
    with open('id-v1.json', 'w', encoding='utf-8') as file:
        json.dump(translated_data, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
