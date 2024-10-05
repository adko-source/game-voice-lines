# Game Voice Lines
# Tools 
------------
* Python 
* Text-to-speech API (elevenlabs.io) https://elevenlabs.io/docs/api-reference/text-to-speech

# Description
------------
Generates voice line audio files for games by processing `voice_lines.json` and `contacts.json`. It utilizes a text-to-speech API to create voice assets for in-game dialogue. 

# Instructions
1. Clone and open repository
2. Open a new terminal and enter the following:
`python -m venv venv; venv\Scripts\activate; python -m pip install -r requirements.txt`
3. Create a config.json file in the root directory and add the following to the file:
{
    "api_key": "<your_elevenlabs_api_key>"
}
4. Update the `voice_lines.json` and `contacts.json` files following the structure shown in the examples
5. cd 'voiceline generator'
6. Enter `python generate_voicelines.py` in the terminal to start app and generate audio files
7. Access the completed audio files in the 'Game Files/Assets/VoiceLines' folder. 
