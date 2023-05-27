# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from services.pbiembedservice import PbiEmbedService
from utils import Utils
from flask import Flask, render_template, send_from_directory
import json
import os
import openai
import azure.cognitiveservices.speech as speechsdk

# Initialize the Flask app
app = Flask(__name__)

# Load configuration
app.config.from_object('config.BaseConfig')
openai.api_type = "azure"
openai.api_base = "https://openaitest316.openai.azure.com/"
openai.api_version = "2022-12-01"
openai.api_key = "a23bed7889fe4570a08a98c929a748f9"
speech_config = speechsdk.SpeechConfig(subscription='9573ea4d70a141488f350d2397955693', region='westus2')
speech_config.speech_recognition_language="zh-TW"

audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

@app.route('/')
def index():
    '''Returns a static HTML page'''

    return render_template('index.html')
@app.route('/translate',methods=['POST'])
def getNLP():
    while True:
        try:
            name = ""
            # name = input ("What is your question ? ").strip()
            print("Speak into your microphone.")
            speech_recognition_result = speech_recognizer.recognize_once_async().get()
            if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
                print("Recognized: {}".format(speech_recognition_result.text))
                name = speech_recognition_result.text
            elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
                print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
            elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = speech_recognition_result.cancellation_details
                print("Speech Recognition canceled: {}".format(cancellation_details.reason))
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    print("Error details: {}".format(cancellation_details.error_details))
                    print("Did you set the speech resource key and region values?")
            # name = speech_recognition_result
            if name == "yes":
                print("message for A")
                # break       
            else:
                usr_input = 'please translate it to english:'+name
                response = ""
                try:
                # start_phrase = query+"\n"+str(rows)+"\nQ: "+usr_input+"\n A: "
                    response = openai.Completion.create(
                        engine='davinci',
                        prompt=usr_input,
                        max_tokens=2048,
                        temperature=0.8,
                        stop=['Q']
                    )
                    text = response['choices'][0]['text'].replace('\n', '').replace(' .', '.').strip()
                    print("Answer:\n"+text)
                    return text
                except:
                    print("An exception has occurred. \n")
                    print("Error Message:", response['error']['message'])
                    return(response['error']['message'])
        except ValueError:
            print ("Sorry, my only purpose is to talk to N and A")
            return None
    return None
    # inputq = input()

    # print("please speak")
    #     # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    # speech_config = speechsdk.SpeechConfig(subscription='dd06729c8a2c4ee685dbf9b876ce6068', region='eastasia')
    # speech_config.speech_recognition_language="zh-TW"

    # audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    # speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # # print("Speak into your microphone.")
    # speech_recognition_result = speech_recognizer.recognize_once_async().get()

    # if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
    #     # print("Recognized: {}".format(speech_recognition_result.text))
    #     print(speech_recognition_result.text)
    #     return speech_recognition_result.text
    # elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
    #     print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    # elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
    #     cancellation_details = speech_recognition_result.cancellation_details
    #     print("Speech Recognition canceled: {}".format(cancellation_details.reason))
    #     if cancellation_details.reason == speechsdk.CancellationReason.Error:
    #         print("Error details: {}".format(cancellation_details.error_details))
    #         print("Did you set the speech resource key and region values?")

    

@app.route('/getembedinfo', methods=['GET'])
def get_embed_info():
    '''Returns report embed configuration'''

    config_result = Utils.check_config(app)
    if config_result is not None:
        return json.dumps({'errorMsg': config_result}), 500

    try:
        embed_info = PbiEmbedService().get_embed_params_for_single_report(app.config['WORKSPACE_ID'], app.config['REPORT_ID'])
        return embed_info
    except Exception as ex:
        return json.dumps({'errorMsg': str(ex)}), 500

@app.route('/favicon.ico', methods=['GET'])
def getfavicon():
    '''Returns path of the favicon to be rendered'''

    return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run()