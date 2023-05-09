import time
import openai
import speech_recognition as sr
import pyttsx3

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Set OpenAI API key
openai.api_key = "YOUR TOKEN HERE"

# Function to send text to ChatGPT and get a response
def generate_code(prompt, conversation_context):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=conversation_context,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.1,
    )

    message = response.choices[0].message["content"].strip()
    return message


# Function to read text out loud using text-to-speech
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

def main():
    speak("Hi Alejandro, welcome back, remember that my keyword is Alexa")
    while True:
        conversation_context = [
            {"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "The text that you will recieve now may have grammatic holes since it is from a transcription, do your best to answer"}
        ]

        print("Listening for the keyword 'Alexa'...")
        
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)

            while True:
                audio_data = recognizer.record(source, duration=5)

                try:
                    text = recognizer.recognize_google(audio_data, language='en-US')
                    print(text)

                    if 'alexa' in text.lower():
                        print("Keyword detected! Start talking...")
                        speak("Hi, I'm listening")
                        break
                except sr.UnknownValueError:
                    pass

            transcript = ''
            silence_start_time = None
            listening_for_keyword = False

            while True:
                audio_data = recognizer.record(source, duration=10)

                try:
                    text = recognizer.recognize_google(audio_data, language='en-US')
                    transcript += ' ' + text
                    print(text)

                    conversation_context.append({"role": "user", "content": text})

                    silence_start_time = None

                    chat_gpt_response = generate_code(text, conversation_context)
                    print("ChatGPT Response:", chat_gpt_response)

                    speak(chat_gpt_response)

                    if "thank you alexa" in transcript.lower():
                        conversation_context = []
                        break
                except sr.UnknownValueError:
                    if silence_start_time is None:
                        silence_start_time = time.time()

                    if time.time() - silence_start_time > 20.1:
                        speak("bye for now")
                        break


if __name__ == "__main__":
    main()
