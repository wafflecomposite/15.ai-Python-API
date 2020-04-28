import re
import time
import json
import logging

import requests
from requests.exceptions import ConnectionError


class FifteenAPI:

    logger = logging.getLogger('15API')
    logger.addHandler(logging.StreamHandler())

    max_text_len = 140

    tts_headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "access-control-allow-origin": "*",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://fifteen.ai",
        "referer": "https://fifteen.ai/app",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "python-requests 15.ai-Python-API(https://github.com/wafflecomposite/15.ai-Python-API)"
    }

    app_page_url = "https://fifteen.ai"
    app_js_url = None  # set dinamically
    tts_url = "https://api.fifteen.ai/app/getAudioFile"

    characters_show_data = {}  # set dinamically
    characters_data = {}  # same but without show keys


    def __init__(self, show_debug = False):
        if show_debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.WARNING)
        self.logger.info("FifteenAPI initialization")
        self.update_characters_status()

    def update_characters_status(self):
        self.characters_show_data = {}  # set dinamically
        self.characters_data = {}  # same but without show keys
        self.logger.info('Performing character status update...')
        self.logger.info('Getting 15.ai app page...')
        response = requests.get(self.app_page_url, headers=self.tts_headers)

        if response.status_code == 200:
            matches = re.findall(r"(/js/app\.[A-z0-9]{8}\.js)", response.text)
            if len(matches) == 0:
                raise ValueError('[15API]Error: can\t find app script url on main app page.')
            else:
                self.app_js_url = self.app_page_url + matches[0]

        else:
            raise ConnectionError(f'[15API]Error while getting main app page. Status code: {response.status_code}')

        if self.app_js_url:
            self.logger.info('Getting 15.ai app js...')
            response = requests.get(self.app_js_url, headers=self.tts_headers)

            if response.status_code == 200:
                matches = re.findall(r"Q=(.*),V=", response.text)
                if len(matches) == 0:
                    raise ValueError('[15API]Error: can\t find characters data in app js.\nMost likely, the format has changed and requires updating the code.')
                else:
                    characters_data = re.sub(r"(\$)(\w+:)(!)", r'\g<2>',  matches[0])
                    characters_data = re.sub(r"([,{])(\w+)(:)", r'\g<1>"\g<2>"\g<3>', characters_data)
                    try:
                        characters_data = json.loads(characters_data)
                    except json.decoder.JSONDecodeError:
                        raise ValueError("[15API]Error while parsing app js.\nMost likely, the format has changed and requires updating the code.'")

                    for show_name, show_char_list in characters_data.items():
                        for character in show_char_list:
                            if not show_name in self.characters_show_data:
                                self.characters_show_data[show_name] = []
                            self.characters_show_data[show_name].append({
                                "name": character['name'],
                                "emotions": character['emotions'],
                                "disabled": not character.get('isDisabled', 1)
                                })
                            self.characters_data[character['name']] = {
                                "emotions": character['emotions'],
                                "disabled": not character.get('isDisabled', 1)
                                }

            else:
                raise ConnectionError(f'[15API]Error while getting app JS. Status code: {response.status_code}')

    def print_characters(self):
        for show_name, show_char_list in self.characters_show_data.items():
            print(show_name)
            for character in show_char_list:
                disabled_str = ""
                if (character['disabled']):
                    disabled_str = "[DISABLED] "
                print(f"  {disabled_str}'{character['name']}', emotions: {character['emotions']}")

    def is_character_exist(self, character):
        return character in self.characters_data

    def get_character_emotions(self, character):
        return self.characters_data[character]["emotions"]

    def is_character_disabled(self, character):
        return self.characters_data[character]["disabled"]

    def get_tts_raw(self, character, emotion, text):

        resp = {"status": "NOT SET", "data": None}

        if not self.is_character_exist(character):
            resp["status"] = "character not found"
            return resp

        if not emotion in self.get_character_emotions(character):
            resp["status"] = "emotion not found"
            return resp

        if self.is_character_disabled(character):
            resp["status"] = "emotion is currently disabled"
            return resp

        text_len = len(text)
        if text_len > self.max_text_len:
            self.logger.warning(f'Text too long ({text_len} > {self.max_text_len}), trimming to {self.max_text_len} symbols')
            text = text[:self.max_text_len - 1]

        if not text.endswith(".") and not text.endswith("!") and not text.endswith("?"):
            if len(text) < 140:
                text += '.'
            else:
                text = text[:-1] + '.'

        self.logger.info(f'Target text: [{text}]')
        self.logger.info(f'Character: [{character}]')
        self.logger.info(f'Emotion: [{emotion}]')

        data = json.dumps({"text": text, "character": character, "emotion": emotion})

        self.logger.info('Waiting for 15.ai response...')

        try:
            response = requests.post(self.tts_url, data=data, headers=self.tts_headers)
        except requests.exceptions.ConnectionError as e:
            resp["status"] = f"ConnectionError ({e})"
            self.logger.error(f"ConnectionError ({e})")
            return resp

        if response.status_code == 200:
            resp["status"] = "OK"
            resp["data"] = response.content
            self.logger.info(f"15.ai API response success")
            return resp
        else:
            self.logger.error(f'15.ai API request error, Status code: {response.status_code}')
            resp["status"] = f'15.ai API request error, Status code: {response.status_code}'
        return resp
        
    def save_to_file(self, character, emotion, text, filename=None):
        tts = self.get_tts_raw(character, emotion, text)
        if tts["status"] == "OK" and tts["data"] is not None:
            if filename is None:
                char_filename_part = "".join(x for x in character[:10] if x.isalnum())
                text_filename_part = "".join(x for x in text[:16] if x.isalnum())
                filename = f"15ai-{char_filename_part}-{text_filename_part}-{round(time.time())}.wav"
            if not filename.endswith(".wav"):
                filename += ".wav"
            f = open(filename, 'wb')
            f.write(tts["data"])
            f.close()
            self.logger.info(f"File saved: {filename}")
            return {"status": tts["status"], "filename": filename}
        else:
            return {"status": tts["status"], "filename": None}
        



if __name__ == "__main__":
    fifteen = FifteenAPI(show_debug = True)

    print("Available characters:")
    fifteen.print_characters()
    print()

    input_str = None
    while input_str != "quit":
        print("Input character:")
        character = input()
        if (character in fifteen.characters_data):
            emotions = fifteen.get_character_emotions(character)
            emotion = None
            if len(emotions) > 1:
                print(f"Input emotion [{emotions}]:")
                emotion = input()
                if emotion not in emotions:
                    print("Emotion not found")
                    continue
            elif len(emotions) == 1:
                emotion = emotions[0]
                print(f"Using only available emotion ({emotion})")
            else:
                print("Error: no emotions available for this character (???)")
                continue
            print("Input text:")
            text = input()
            print("Processing...")
            fifteen.save_to_file(character, emotion, text)
        else:
            print(f"Character not found (character)")
