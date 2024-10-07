import requests  # Used for making HTTP requests
import json  # Used for working with JSON data
import os  # Used for interacting with the operating system

print("App started")

# Get Eleven Labs API key from config.json
with open('../config.json') as config_file:
    config = json.load(config_file)

api_key = config['api_key']

# Define constants
CONTACTS_FILE_PATH = "../Game Files/Data/contacts.json"
VOICE_LINES_FILE_PATH = "../Game Files/Data/voice_lines.json"
OUTPUT_FOLDER = "../Game Files/Assets/VoiceLines"
CHUNK_SIZE = 1024  
XI_API_KEY = api_key

def create_audio_file(api_response, file_name, folder_name):
        # Create the directory to save the audio files in
        os.makedirs(os.path.join(OUTPUT_FOLDER, folder_name), exist_ok=True)

        file_name_and_path = os.path.join(OUTPUT_FOLDER, folder_name, file_name)
       
        # Open the output file in write-binary mode
        with open(file_name_and_path, "wb") as f:
            # Read the response in chunks and write to the mp3 audio file
            for chunk in api_response.iter_content(chunk_size=CHUNK_SIZE):
                f.write(chunk)
        
        print("Audio stream saved successfully.")

def call_text_to_speech_api(voice_id, text, file_name, folder_name):

    headers = {
        "Accept": "application/json",
        "xi-api-key": XI_API_KEY
    }
     
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"

    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.8,
        "style": 0.0,
        "use_speaker_boost": True
        }
    }
   
    response = requests.request("POST", url, json=payload, headers=headers)
    
    # Check if the request was successful
    if response.ok:
        create_audio_file(
            api_response=response, 
            file_name=file_name, 
            folder_name=folder_name
        )
        
    else:
        # Print the error message if the request was not successful
        print(response.text)
        
    return response.text


# Update voice_lines.json with the generated assets details
def update_voice_lines_file(generated_file_name, voice_actor, line, voice_line_index): 
    with open(VOICE_LINES_FILE_PATH, 'r') as file:
        data = json.load(file)

        voice_line_object = data['voiceLines'][voice_line_index]
      
        # Add new properties to the voice_line_object
        # to refernce the generated assets
        if 'generated_assets' not in voice_line_object:
            voice_line_object['generated_assets'] = []

        generated_asset_info = {
            "line": line,
            "audio_file_name": generated_file_name,
            "voice_actor": voice_actor
        }
        # Add new properties to the file
        voice_line_object['generated_assets'].append(generated_asset_info)

        # Write the updated data back to the file
        with open(VOICE_LINES_FILE_PATH, 'w') as updated_file:
            json.dump(data, updated_file, indent=4)

def process_voice_line(voice_line, voice_line_index):
    current_voice_line = str(voice_line_index + 1)
    print("Processing voice line " + current_voice_line)
    
    lines = voice_line.get('lines', [])
    valid_speakers = voice_line.get('valid_speakers', [])
    
    if (len(valid_speakers) == 0):
        print("Voice line has no valid speakers")
        return
         
    if len(lines) == 0:
        print("No lines found")
        return

    for speaker in valid_speakers:
        voice_id = get_voice_id_from_name(speaker)
        
        for line_index, line in enumerate(lines):
            print(f"Processing voice line {line_index + 1} for {speaker}: {line}")
            current_voice_line = str(voice_line_index + 1)
            text = line
            audio_file_name = f"{line_index}_{voice_id}.mp3"
            
            folder_name = f"{"New"}"
            
            call_text_to_speech_api(
                voice_id=voice_id,
                text=text,
                file_name=audio_file_name,
                folder_name=folder_name
            ) 
            update_voice_lines_file(
                generated_file_name=audio_file_name,
                voice_actor=voice_id,
                line=line,
                voice_line_index=voice_line_index
            )

    print("Finished processing voice line " + current_voice_line)

# TODO: Get the voice ID from the name
def get_voice_id_from_name(name):
    
    return "CwhRBWXzGAHq8TQ4Fs17"

# Check if each contact has an associated voice ID
try:
    with open(CONTACTS_FILE_PATH) as contacts_file:
        data = json.load(contacts_file)

    contacts = data['contacts']

    for contact in contacts:
        try:
            # Check if contact has a 'elevenLabsId' property
            print(contact['voice_actor'])  
        
        except KeyError:
            # Handle the case where the property is missing
            print("No associated voice ID found for the character",contact['name'])

except FileNotFoundError:
    print(f"Error: The file {CONTACTS_FILE_PATH} was not found.")
except json.JSONDecodeError:
    print("Error: Failed to decode JSON from the contacts file.")


# Get data from voice_lines.json
with open(VOICE_LINES_FILE_PATH) as voice_lines_file:
    data = json.load(voice_lines_file)

voice_lines = data['voiceLines']

if(len(voice_lines) == 0):
    print("No voice lines found in voices_lines.json")
else:
    # Process each voice line
    for index, voice_line in enumerate(voice_lines):
        process_voice_line(
            voice_line, 
            voice_line_index=index
        )

print("App finished. Assets generated in " + OUTPUT_FOLDER)