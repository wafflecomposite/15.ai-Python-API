import requests
import time
import json


class FifteenAICharacters:
    # Portal
    GLaDOS = "GLaDOS"
    Wheatley = "Wheatley"

    # MLP
    TwilightSparkle = "Twilight Sparkle"
    Fluttershy = "Fluttershy"
    Rarity = "Rarity"
    PrincessCelestia = "Princess Celestia"

    # The Stanley Parable
    TheNarrator = "The Narrator"

    # Doctor Who
    TenthDoctor = "Tenth Doctor"

    # Undertale
    Sans = "Sans"

    # Team Fortress 2
    Soldier = "Soldier"
    #Pyro = "Pyro"

class FifteenAI:

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

    options_headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "access-control-request-headers": "access-control-allow-origin,content-type",
        "access-control-request-method": "POST",
        "origin": "https://fifteen.ai",
        "referer": "https://fifteen.ai/app",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "python-requests 15.ai-Python-API(https://github.com/wafflecomposite/15.ai-Python-API)"
    }

    tts_url = "https://api.fifteen.ai/app/getAudioFile"

    def __init__(self):
        pass

    def get(self, text, character):

        text_len = len(text)
        if text_len > self.max_text_len:
            print(f'Text too long ({text_len} > {self.max_text_len}), trimming to {self.max_text_len} symbols')
            text = text[:self.max_text_len - 1]

        if not text.endswith(".") and not text.endswith("!") and not text.endswith("?"):
            if len(text) < 140:
                text += '.'
            else:
                text = text[:-1] + '.'

        print(f'Target text: [{text}]')
        print(f'Character: [{character}]')

        data = json.dumps({"text": text, "character": character})

        print('Waiting for response...')
        # pre_resp = requests.options(self.tts_get_url, headers=self.options_get_headers)
        response = requests.post(self.tts_url, data=data, headers=self.tts_headers)

        filename = f'{round(time.time())}.wav'

        if response.status_code == 200:
            f = open(f'{filename}', 'wb')
            f.write(response.content)
            f.close()
        else:
            print(f'ERROR! Status code: {response.status_code}')
        print(f'Filename: {filename}')


if __name__ == "__main__":
    fifteen = FifteenAI()
    fifteen.get(
        "This is a test. I think it's a test. Isn't this a test?",
        FifteenAICharacters.GLaDOS
    )
