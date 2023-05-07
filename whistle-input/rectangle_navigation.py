# DESCRIPTION:
# - A simple 2D application using pyglet that displays a stack of rectangles of which one is visually selected. 
# - The frequency at an interval of 2 seconds is observed. It is observed whether the frequency rises briefly and then falls again 
# - and whether the frequency rises, then falls and then rises again. 
# - If there is a short whistle, the selection goes down. Two short whistles move the selection up.
# - If the bottom cube is selected and the selection goes down, then the top cube is selected and vice versa.

import pyaudio
import numpy as np
from pyglet import app, image, clock
from pyglet.window import Window

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

# window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
# rectangle properties
RECTANGLE_SIZE = 50
RECTANGLE_X_POS = WINDOW_WIDTH / 2
RECTANGLE_Y_POS = WINDOW_HEIGHT * 0.9
COLOR_NOT_CHOOSEN = (255,255,255,0)
COLOR_CHOOSEN = (0,255,0,0)
RECTANGLE_AMOUNT = 3
choosen_rectangle = 1

# create game window
window = Window(WINDOW_WIDTH, WINDOW_HEIGHT)
# used for the whistle detection
    # 2 sec = 20 saved frequencies (1 per 0.1 sec)
frequency_arr = [0] * 20
index = 0

@window.event
def on_draw():
    draw_rectangles()

def draw_rectangles():
    for i in range(RECTANGLE_AMOUNT):
        color = COLOR_NOT_CHOOSEN
        if choosen_rectangle == i:
            color = COLOR_CHOOSEN

        rectangle_image = image.create(RECTANGLE_SIZE, RECTANGLE_SIZE, image.SolidColorImagePattern(color))
        rectangle_image.blit(RECTANGLE_X_POS, (RECTANGLE_Y_POS * 0.8 - RECTANGLE_SIZE * i) - 20 * i )

def update_choosen(dt):

    global choosen_rectangle, index, frequency_arr
            
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
            if choosen_rectangle + 1 <= RECTANGLE_AMOUNT - 1:
                choosen_rectangle += 1
            else:
                choosen_rectangle = 0
            print("down")
        if sum(frequency_arr) > 3500:
            if choosen_rectangle - 1 >= 0:
                choosen_rectangle -= 1
            else:
                choosen_rectangle = RECTANGLE_AMOUNT - 1
            print("up")
        frequency_arr = [0] * 20
    
clock.schedule_interval(update_choosen, 0.1)

# run game
app.run()