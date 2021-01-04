def synthesize_text(text, name, speed, pitch, outputName):
    """Synthesizes speech from the input string of text."""
    from google.cloud import texttospeech

    from google.oauth2 import service_account

    credentials = service_account.Credentials.from_service_account_file(
        'google_credentials.json')

    scoped_credentials = credentials.with_scopes(
        ['https://www.googleapis.com/auth/cloud-platform'])

    client = texttospeech.TextToSpeechClient(credentials = scoped_credentials)

    input_text = texttospeech.SynthesisInput(text = text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code = "en-US",
        name = name,
        ssml_gender = texttospeech.SsmlVoiceGender.MALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding = texttospeech.AudioEncoding.MP3,
        speaking_rate = float(speed),
        pitch = float(pitch)

    )

    response = client.synthesize_speech(
        request = {"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    outputName = outputName + ".mp3"

    # The response's audio_content is binary.
    with open(outputName, "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file "' + outputName + '"')


print("Enter text to convert to mp3")
text = input()
print("Enter exact name of voice. E.g. 'en-US-Wavenet-I'")
name = input()
print("Enter a speed from 0.25 to 4")
speed = input()
print("Enter a pitch from -20 to 20")
pitch = input()
print("Enter name of output file")
outputName = input()

synthesize_text(text, name, speed, pitch, outputName)

while True:
    print("Continue with same settings and new text? Y/N")
    response = input()
    if response.lower() == 'n':
        break
    else:
        print("Enter text to convert to mp3")
        text = input()
        print("Enter name of output file")
        outputName = input()
        synthesize_text(text, name, speed, pitch, outputName)
