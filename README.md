# 15API - 15.ai Python API

Unofficial Python3 API for https://fifteen.ai/

## Attention!
15.ai TOS explicitly states that:
- Website (and the content generated with it) is intended for strictly non-commercial use.
- If you want to publish the generated content online, you should include a citation (simply including 15.ai is sufficient).
  
These are simple rules, please follow them. Don't be that guy.


Refer to [About](https://fifteen.ai/about) and [FAQ](https://fifteen.ai/faq) for more info.


Keep in mind that the 15.ai is constantly changing and improving, and this script may and eventually will break and will require updating. If it does not work, create issue, or, even better, pull request to fix that.

  
## Installation
Requires `python >= 3.6`


Note: on Windows, in this and the following commands instead of `python3`, you may want to use `python`

Install dependencies

    python3 -m pip install requests
Grab the `fifteen_api.py` and throw it where you want to use it.

## Usage
### As command line tool:
You can use `fifteen_api.py` as executable in terminal. Launch it with

    python3 fifteen_api.py
 You will get a list of characters and their available emotions, and you can use them right there to get your text-to-speech dreams come true as .wav files.
### As imported module in python code:
Suppose you put `fifteen_api.py` next to the file in which you want to use it:
#### Import class:

    from fifteen_api import FifteenAPI

#### Initialize API:

    tts_api = FifteenAPI()
Alternatively, to get verbose output:

    tts_api = FifteenAPI(show_debug=True)

#### Get characters list:

    tts_api.get_characters_list()
Example output

    ['Twilight Sparkle', 'Fluttershy', 'Rarity', 'Applejack', 'Rainbow Dash', 'Pinkie Pie', 'GLaDOS', 'Wheatley', 'Chell']
#### Get character emotions:

    tts_api.get_character_emotions_list("Twilight Sparkle")

Example output:

    ['Happy', 'Neutral']
#### Save TTS to file:

    tts_api.save_to_file("Fluttershy", "Neutral", "This is a test text", "my_tts_file.wav")
Alternatively, to automatically generate a unique file name

    tts_api.save_to_file("Fluttershy", "Neutral", "This is a test text")
Example output on successful request: 


    {'status': 'OK', 'filename': '15ai-Fluttershy-Thisisatestte-1588057995.wav'}
Example output on failed request: 

     {'status': 'Reason_why_it_failed', 'filename': None}
#### Get TTS as bytes:

    response = tts_api.get_tts_raw("Fluttershy", "Neutral", "This is a test text")
Example output on successful request: 


    {'status': 'OK', 'data': b'th3r3g03sy0urbyt3s'}
Example output on failed request: 

     {'status': 'Reason_why_it_failed', 'data': None}