import os
from fifteen_api import FifteenAPI

# initialization
api = FifteenAPI(show_debug=True)

# print characters and their available emotions to console
api.print_characters()

# be aware that there is a serverside max text length. If text is too long, it will be trimmed.
print(api.max_text_len)


### valid usage examples

# get tts raw bytes (well, assuming that Fluttershy is not currently disabled)
response = api.get_tts_raw("Fluttershy", "Neutral", "This is a test")
assert response["status"] == "OK"
assert len(response["data"]) > 100000  # those are .wav audiofile bytes

# save tts to file with generated filename
response = api.save_to_file("Fluttershy", "Neutral", "This is another test")
assert response["status"] == "OK"
assert response["filename"] != None  # this is a generated filename of TTS file
os.remove(response["filename"])

# save tts to file with target filename.
response = api.save_to_file("Fluttershy", "Neutral", "One more test", "tts.wav")
assert response["status"] == "OK"
assert response["filename"] == "tts.wav"
os.remove("tts.wav")

# if filename doesn't end with '.wav', it will be added automatically
response = api.save_to_file("Fluttershy", "Neutral", "Last one valid test", "randomfilename")
assert response["status"] == "OK"
assert response["filename"] == "randomfilename.wav"
os.remove("randomfilename.wav")


### invalid usage examples

# unavailable character
response = api.save_to_file("random character or an incorrect name", "Neutral", "Test?", "tts.wav")
assert response["status"] != "OK"
assert response["filename"] == None
print(response)

# emotion that doesn't exist
response = api.save_to_file("Fluttershy", "Super extra angry!", "Angry test!!!", "tts.wav")
assert response["status"] != "OK"
assert response["filename"] == None
print(response)

# assume that 15.ai api is currently broken
api.tts_url = "https://example.com/brokenapi"
response = api.save_to_file("Fluttershy", "Neutral", "...test?", "tts.wav")
assert response["status"] != "OK"
assert response["filename"] == None
print(response)

# assume that whole 15.ai website is currently down (or format changed or whatever). It's gonna crash.
api.app_page_url = "https://example.com/eh"
api.update_characters_status()
response = api.save_to_file("Fluttershy", "Neutral", "oof", "tts.wav")
