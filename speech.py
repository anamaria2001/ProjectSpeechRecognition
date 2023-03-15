import speech_recognition as sr
import pyttsx3
import pyaudio
import time
import wave

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()

stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)

print("start recording...")

frames = []
seconds = 10
for i in range(0, int(RATE / FRAMES_PER_BUFFER * seconds)):
    data = stream.read(FRAMES_PER_BUFFER)
    frames.append(data)

print("recording has stopped")

print("waiting for 10 seconds")
time.sleep(5)

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open("ana_recorder.wav", 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

print("start talking")
r = sr.Recognizer()


def speakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


def speak(r):
    while(1):
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=0.2)
            audio2 = r.listen(source2)
            mytext = r.recognize_google(audio2)
            mytext = mytext.lower()
            print("Did you say ", mytext)
            speakText(mytext)
        return mytext


def save_transcribe():
    data1 = speak(r)
    text_filename = 'test.txt'
    with open(text_filename, 'w') as f:
        f.write(data1)
    print('Transcript saved')


save_transcribe()
