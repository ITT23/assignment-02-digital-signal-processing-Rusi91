# DESCRIPTION:
# 
# - The frequency is observed. It is observed whether the frequency rises briefly and then falls again 
# - and whether the frequency rises, then falls and then rises again. 
# - If there is a short whistle, the left arrow key is triggered. Two short whistles triggers the right arrow key.
# 
# TESTED:
# - Tested it on a power point presentation on my google drive

import pyaudio
import numpy as np
from pynput.keyboard import Key, Controller

# Set up audio stream
# reduce chunk size and sampling rate for lower latency
CHUNK_SIZE = 1024  # Number of audio frames per buffer
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Mono audio
RATE = 44100  # Audio sampling rate (Hz)
p = pyaudio.PyAudio()

# print info about audio devices
# let user select audio device
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

print('select audio device:')
input_device = int(input())

# open audio input stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK_SIZE,
                input_device_index=input_device)

# sources used: in karaoke.py
# get peak frequency
def extract_major_frequency(data, sampling_rate):
    fft = np.fft.fft(data)
    fft_freqs = np.fft.fftfreq(len(data))
    major_freq_coefficient = np.argmax(np.abs(fft))
    major_freq = fft_freqs[major_freq_coefficient]
    
    return abs(major_freq * sampling_rate)

# used for the whistle detection
    # 2 sec = 20 saved frequencies (1 per 0.1 sec)
frequency_arr = [0] * 20
index = 0

# doc: https://pynput.readthedocs.io/en/latest/keyboard.html
keyboard = Controller()

while True:
    # Read audio data from stream
    data = stream.read(CHUNK_SIZE)
    # Convert audio data to numpy array
    data = np.frombuffer(data, dtype=np.int16)
    most_frequ = extract_major_frequency(data, RATE)

    if index < 19:
        if most_frequ > 1000:
            frequency_arr[index] = most_frequ
        else:
            frequency_arr[index] = 0
        index += 1
    else:
        index = 0
        if sum(frequency_arr) > 1000 and sum(frequency_arr) < 3500:
            keyboard.press(Key.left)
        if sum(frequency_arr) > 3500:
            keyboard.press(Key.right)
        frequency_arr = [0] * 20

    print(most_frequ)
