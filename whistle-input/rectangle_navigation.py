import pyaudio
import numpy as np

from matplotlib import pyplot as plt
import pyglet
from pyglet import app, image, clock
from pyglet.window import Window
from os import path
import math

from rectangle import Rectangle

# Set up audio stream
# reduce chunk size and sampling rate for lower latency
CHUNK_SIZE = 1024  # Number of audio frames per buffer
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Mono audio
RATE = 44100  # Audio sampling rate (Hz)
p = pyaudio.PyAudio()

# window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

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

def extract_major_frequency(data, sampling_rate):
    fft = np.fft.fft(data)
    fft_freqs = np.fft.fftfreq(len(data))
    major_freq_coefficient = np.argmax(np.abs(fft))
    major_freq = fft_freqs[major_freq_coefficient]
    
    return abs(major_freq * sampling_rate)

RECTANGLE_SIZE = 50
RECTANGLE_X_POS = WINDOW_WIDTH / 2

RECTANGLE_ONE_Y_POS = WINDOW_HEIGHT * 0.9
RECTANGLE_TWO_Y_POS = RECTANGLE_ONE_Y_POS - RECTANGLE_SIZE
RECTANGLE_THREE_Y_POS = RECTANGLE_TWO_Y_POS - RECTANGLE_SIZE

rectangle_one = Rectangle(RECTANGLE_SIZE, RECTANGLE_SIZE, 1, False)
rectangle_one = Rectangle(RECTANGLE_SIZE, RECTANGLE_SIZE, 2, True)
rectangle_one = Rectangle(RECTANGLE_SIZE, RECTANGLE_SIZE, 3, False)

# create game window
window = Window(WINDOW_WIDTH, WINDOW_HEIGHT)

@window.event
def on_draw():
    draw_rectangles()

def draw_rectangles():
    rectangle_one.draw_rectangle()








# run game
app.run()