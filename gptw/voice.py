import azure.cognitiveservices.speech as speechsdk
import openai
import time


ssml = """<speak xmlns="http://www.w3.org/2001/10/synthesis" 
xmlns:mstts="http://www.w3.org/2001/mstts" 
xmlns:emo="http://www.w3.org/2009/10/emotionml" 
version="1.0" xml:lang="en-US">
<voice name="en-US-JennyNeural"><s/>
    <mstts:express-as style="friendly">
        <prosody rate="+8.00%" pitch="+3.00%">
            {}
        </prosody>
    </mstts:express-as><s/>
</voice></speak>"""


prompts = """
As an English language learning assistant, 
your first task is to offer users a selection of engaging topics to choose from. 
Next, you engage in conversation with user. 
For each user input, your primary task is to assess whether their grammar is correct and 
whether it aligns with the conventions used by native speakers. and provide feedback to the user.
make sure keep  every response short and concise.
After provide the feedback, pose the next question related to the user's input.
"""

recognizer_results = []


def chat_in_audio(token, endpoint, depname, tts_key, tts_region):

    global recognizer_results

    # Set up OpenAI API credentials
    openai.api_key = token
    openai.api_base = endpoint
    openai.api_type = "azure"
    openai.api_version = "2023-05-15"

    # Set up Azure TTS API credentials
    speech_config = speechsdk.SpeechConfig(
        subscription=tts_key, region=tts_region)
    speech_config.output_format = speechsdk.OutputFormat.Detailed

    # Set up speech recognizer
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    # https://speech.microsoft.com/portal/voicegallery
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config)

    # Set up conversation loop
    messages = [
        {
            "role": "system",
            "content": prompts,
        },
    ]

    speech_recognizer.recognized.connect(recognized_callback)
    while True:
        # Get user input from microphone
        print("Speak:")

        speech_recognizer.start_continuous_recognition()

        input("...")

        speech_recognizer.stop_continuous_recognition_async().get()
        time.sleep(1)
        # Use speech recognizer to convert speech to text
        user_input = " ".join(recognizer_results)
        print("You said: " + user_input)
        messages.append({"role": "user", "content": user_input})
        completion = openai.ChatCompletion.create(
            engine=depname,
            messages=messages,
            temperature=0.5,
        )

        # Get response text
        response_text = str(completion.choices[0].message.content).strip()
        print("AI said: " + response_text)
        messages.append({"role": "assistant", "content": response_text})

        play_result = speech_synthesizer.speak_ssml_async(
            ssml.format(response_text)).get()

        if play_result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Error synthesizing audio: {}".format(
                play_result.error_details))

        time.sleep(0.5)


def recognized_callback(evt):
    global recognizer_results
    if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
        recognizer_results.append(evt.result.text)
