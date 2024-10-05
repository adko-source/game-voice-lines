import requests  # Used for making HTTP requests
import json  # Used for working with JSON data
import os  # Used for interacting with the operating system

# Get Eleven Labs API key from config.json
with open('../config.json') as config_file:
    config = json.load(config_file)

api_key = config['api_key']

# Define constants
CONTACTS_FILE_PATH = "../Game Files/Data/contacts.json"
VOICE_LINES_FILE_PATH = "../Game Files/Data/voice_lines.json"
OUTPUT_FOLDER = "../Game Files/Assets/VoiceLines"
API_KEY = api_key

# Get data from contacts.json
with open(CONTACTS_FILE_PATH) as contacts_file:
    data = json.load(contacts_file)

contacts = data['contacts']

print(contacts)

# Get data from voice_lines.json
with open(VOICE_LINES_FILE_PATH) as voice_lines_file:
    data = json.load(voice_lines_file)

voice_lines = data['voiceLines']

# Create a temporary folder to store each voice line object as a separate JSON file
folder = 'voice_lines_output_tmp'
os.makedirs(folder, exist_ok=True)

# Write each voice line object to a separate JSON file
for index, item in enumerate(data["voiceLines"]):
    print(index)
    print(item)
    file_name = f"voice_line_{index}.json"
    file_path = os.path.join(folder, file_name)

    with open(file_path, 'w') as file:
        json.dump(item, file, indent=4)

# for index, item in voice_lines:
#     for key, value in item.items():
#         print(f"{key}: {value}")
    



data = {
    "name": "John",
    "age": 30,
    "city": "New York"
}

file_name = 'line1.json'
file_path = os.path.join(OUTPUT_FOLDER, file_name)

# Writing data to a JSON file
with open(file_path, 'w') as file:
    json.dump(data, file, indent=4)

# # Define constants
# CHUNK_SIZE = 1024  # Size of chunks to read/write at a time
# XI_API_KEY = api_key  # Your API key for authentication
# OUTPUT_FOLDER = "speech_files"
# EXCEL_FILE_PATH = "unprocessed_files/lines.xlsx"

# print("App started!")
# print("Audio files will be saved in the 'speech_files' folder.")

# def call_text_to_speech_api(voice_id, text, file_name, folder_name):

#     headers = {
#         "Accept": "application/json",
#         "xi-api-key": XI_API_KEY
#     }
     
#     url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"

#     payload = {
#         "text": text,
#         "model_id": "eleven_monolingual_v1",
#         "voice_settings": {
#         "stability": 0.5,
#         "similarity_boost": 0.8,
#         "style": 0.0,
#         "use_speaker_boost": True
#         }
#     }
   
#     response = requests.request("POST", url, json=payload, headers=headers)
    
#     # Check if the request was successful
#     if response.ok:

#         # Create the directory to save the audio files in
#         # group by voice actor name in the speech_files folder
#         os.makedirs(os.path.join(OUTPUT_FOLDER, folder_name), exist_ok=True)

#         file_name_and_path = os.path.join(OUTPUT_FOLDER, folder_name, file_name)
       
#         # Open the output file in write-binary mode
#         with open(file_name_and_path, "wb") as f:
#             # Read the response in chunks and write to the mp3 audio file
#             for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
#                 f.write(chunk)
#         # Inform the user of success
#         print("Audio stream saved successfully.")
#     else:
#         # Print the error message if the request was not successful
#         print(response.text)
        
#     return response.text

# # Get the list of available voices from API
# def get_voices():

#     headers = {
#         "Accept": "application/json",
#         "xi-api-key": XI_API_KEY,
#         "Content-Type": "application/json"
#     }

#     url = "https://api.elevenlabs.io/v1/voices"

#     response = requests.request("GET", url, params={"api_key": api_key}, headers=headers)

#     response_json = response.json()

#     voices = response_json["voices"]
    
#     # Convert voices json into a DataFrame
#     df = pd.DataFrame(voices)

#     # Save the available voices returned from the api to an Excel file
#     df.to_excel('voices.xlsx', index=False)
    
#     return voices

# get_voices()

# # Read the unprocessed Excel file to get data for the API call
# def get_data_from_excel_file():

#     # Read the unprocessed Excel file into a DataFrame
#     df = pd.read_excel(EXCEL_FILE_PATH)

#     for index, row in df.iterrows():
#         line_id = row['line_id']
#         voice_id = row['voice_id']
#         text = row['text']
#         name = row['name'].lower()
#         file_name = f"{line_id}_{voice_id}.mp3"
#         folder_name = f"{name}"
#         print(f"Line ID: {line_id}, Voice ID: {voice_id}, Text: {text}")
        
#         # Call the Text-to-Speech API and save the audio stream to an output file
#         # for each row in the Excel file

#         # TODO: Pass file name (index)
#         # 
#         call_text_to_speech_api(
#             voice_id=voice_id,
#             text=text,
#             file_name=file_name,
#             folder_name=folder_name
            
#         )    

# get_data_from_excel_file()

# # Move the processed files to the processed_files folder
# def move_files():
    
#     source_path = 'unprocessed_files/lines.xlsx'

#     destination_path = 'processed_files/lines.xlsx'

#     os.rename(source_path, destination_path)

# move_files()