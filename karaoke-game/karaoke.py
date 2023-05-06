import pyaudio
import numpy as np
import librosa
from matplotlib import pyplot as plt
import pyglet
from pyglet import app, image, clock
from pyglet.window import Window
from vocal_range_enum import Vocal_Range

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



low_notes = ["C5", "C4", "B4", "B3", "A4", "A3", "G4", "G3", "F4", "F3", "E4", "E3", "D4", "D3", "C4", "C3", "B3", "B2", "A3", "A2", \
             "G3", "G2", "F3", "F2", "E3", "E2", "D3", "D2", "C3", "C2", "B2", "B1", "A2", "A1", "G2", "G1", "F2", "F1", "E2", "E1", "C2", "C1"]
high_notes = ["C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4", "C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A5", "A#5", \
              "B5", "C6", "C#6", "D6", "D#6", "E6", "F6", "F#6", "G6", "G#6", "A6", "A#6", "B6", "C7"]
notes_index = 0

note_input = ""

vocal_range_test = Vocal_Range(Vocal_Range.DESCRIPTION)

highest_achieved_note = ""
lowest_achieved_note = ""



# create game window
window = Window(WINDOW_WIDTH, WINDOW_HEIGHT)




@window.event
def on_draw():
    window.clear()

    if vocal_range_test == Vocal_Range.DESCRIPTION:
        draw_start_screen()
    elif vocal_range_test == Vocal_Range.LOW_TEST or vocal_range_test == Vocal_Range.HIGH_TEST:
        draw_tested_note()
        draw_input_note()
        draw_scip_message()
    elif vocal_range_test == Vocal_Range.LOW_TESTED:
        draw_next_test_screen()
    elif vocal_range_test == Vocal_Range.HIGH_TESTED:
        draw_result_screen()


def draw_tested_note():
    tested_note = ""
    if vocal_range_test == Vocal_Range.LOW_TEST:
        tested_note = low_notes[notes_index]
        draw_test_title("VOCAL TEST FOR LOW RANGE")
    else:
        tested_note = high_notes[notes_index]
        draw_test_title("VOCAL TEST FOR HIGH RANGE")
        

    tested_note_desc_label = pyglet.text.Label("GOAL",
                          font_name='Times New Roman',
                          font_size=30,
                          x = WINDOW_WIDTH / 4,
                          y = WINDOW_HEIGHT / 2 + WINDOW_HEIGHT / 5,
                          anchor_x='center', anchor_y='center')

    tested_note_label = pyglet.text.Label(tested_note,
                          font_name='Times New Roman',
                          font_size=60,
                          x = WINDOW_WIDTH / 4,
                          y = WINDOW_HEIGHT / 2,
                          anchor_x='center', anchor_y='center')
    tested_note_desc_label.draw()
    tested_note_label.draw()

def draw_input_note():
    global note_input

    input_note_desc_label = pyglet.text.Label("INPUT",
                          font_name='Times New Roman',
                          font_size=30,
                          x = WINDOW_WIDTH / 2 + WINDOW_WIDTH / 4,
                          y = WINDOW_HEIGHT / 2 + WINDOW_HEIGHT / 5,
                          anchor_x='center', anchor_y='center')
    
    input_note_label = pyglet.text.Label(note_input,
                          font_name='Times New Roman',
                          font_size=60,
                          x = WINDOW_WIDTH / 2 + WINDOW_WIDTH / 4,
                          y = WINDOW_HEIGHT / 2,
                          anchor_x='center', anchor_y='center')
    input_note_desc_label.draw()
    input_note_label.draw()

def draw_test_title(title):

    test_title_label = pyglet.text.Label(title,
                          font_name='Times New Roman',
                          font_size=20,
                          x = WINDOW_WIDTH / 2,
                          y = WINDOW_HEIGHT * 0.9,
                          anchor_x='center', anchor_y='center')

    test_title_label.draw()
    
def draw_scip_message():

    scip_message_label = pyglet.text.Label("Press -spacebar- to skip the note or -N- to skip the test.",
                          font_name='Times New Roman',
                          font_size=15,
                          x = WINDOW_WIDTH / 2,
                          y = WINDOW_HEIGHT * 0.1,
                          anchor_x='center', anchor_y='center')

    scip_message_label.draw()

def handle_note_input(dt):
    global note_input, notes_index, vocal_range_test, lowest_achieved_note, highest_achieved_note
    # Read audio data from stream
    data = stream.read(CHUNK_SIZE)

    # Convert audio data to numpy array
    data = np.frombuffer(data, dtype=np.int16)

    most_frequ = extract_major_frequency(data, RATE)

    if int(most_frequ) != 0 :
        note_input = librosa.hz_to_note(most_frequ)
        if vocal_range_test == vocal_range_test.LOW_TEST and note_input == low_notes[notes_index] and notes_index + 1 < len(low_notes):
            notes_index += 1
            lowest_achieved_note = note_input
            if notes_index + 1 >= len(low_notes):
                vocal_range_test = vocal_range_test.LOW_TESTED
                notes_index = 0
        elif vocal_range_test == vocal_range_test.HIGH_TEST and note_input == high_notes[notes_index] and notes_index + 1 < len(high_notes):
            notes_index += 1
            highest_achieved_note = note_input
            if notes_index + 1 >= len(high_notes):
                vocal_range_test = vocal_range_test.HIGH_TESTED
                notes_index = 0

def draw_start_screen():
    description_overall = pyglet.text.Label("VOCAL RANGE TESTER",
                          font_name='Times New Roman',
                          font_size=40,
                          x = WINDOW_WIDTH/2, y = WINDOW_HEIGHT / 1.5,
                          anchor_x = 'center', anchor_y = 'center')
    description_continue = pyglet.text.Label("Press the - spacebar key - to start the test for LOW RANGE.",
                          font_name='Times New Roman',
                          font_size=20,
                          x = WINDOW_WIDTH / 2, y = WINDOW_HEIGHT / 3,
                          anchor_x = 'center', anchor_y = 'center')
    description_overall.draw()
    description_continue.draw()

def draw_next_test_screen():
    description_overall = pyglet.text.Label("VOCAL TEST FOR HIGH RANGE",
                          font_name='Times New Roman',
                          font_size=40,
                          x = WINDOW_WIDTH/2, y = WINDOW_HEIGHT / 1.5,
                          anchor_x = 'center', anchor_y = 'center')
    description_continue = pyglet.text.Label("Press the - spacebar key - to start the test.",
                          font_name='Times New Roman',
                          font_size=20,
                          x = WINDOW_WIDTH / 2, y = WINDOW_HEIGHT / 3,
                          anchor_x = 'center', anchor_y = 'center')
    description_overall.draw()
    description_continue.draw()

def draw_result_screen():
    global lowest_achieved_note, highest_achieved_note
    result_overall = pyglet.text.Label("RESULTS OF THE VOCAL TESTER",
                          font_name='Times New Roman',
                          font_size=40,
                          x = WINDOW_WIDTH/2, y = WINDOW_HEIGHT / 1.5,
                          anchor_x = 'center', anchor_y = 'center')
    
    lowest_note_desc_label = pyglet.text.Label("LOWEST ACHIEVED NOTE:",
                          font_name='Times New Roman',
                          font_size=30,
                          x = WINDOW_WIDTH / 4,
                          y = WINDOW_HEIGHT / 2 + WINDOW_HEIGHT / 5,
                          anchor_x='center', anchor_y='center')

    lowest_note_label = pyglet.text.Label(lowest_achieved_note,
                          font_name='Times New Roman',
                          font_size=60,
                          x = WINDOW_WIDTH / 4,
                          y = WINDOW_HEIGHT / 2,
                          anchor_x='center', anchor_y='center')
    
    highest_note_desc_label = pyglet.text.Label("HIGHEST ACHIEVED NOTE:",
                          font_name='Times New Roman',
                          font_size=30,
                          x = WINDOW_WIDTH / 2 + WINDOW_WIDTH / 4,
                          y = WINDOW_HEIGHT / 2 + WINDOW_HEIGHT / 5,
                          anchor_x='center', anchor_y='center')
    
    highest_note_label = pyglet.text.Label(highest_achieved_note,
                          font_name='Times New Roman',
                          font_size=60,
                          x = WINDOW_WIDTH / 2 + WINDOW_WIDTH / 4,
                          y = WINDOW_HEIGHT / 2,
                          anchor_x='center', anchor_y='center')
    
    restart_label = pyglet.text.Label("Press -spacebar- to restart the test.",
                          font_name='Times New Roman',
                          font_size=15,
                          x = WINDOW_WIDTH / 2,
                          y = WINDOW_HEIGHT * 0.1,
                          anchor_x='center', anchor_y='center')
    
    lowest_achieved_note = ""
    highest_achieved_note = ""

    result_overall.draw()
    lowest_note_desc_label.draw()
    lowest_note_label.draw()
    highest_note_desc_label.draw()
    highest_note_label.draw()
    restart_label.draw()
    
@window.event
def on_key_press(symbol, modifiers):
    global vocal_range_test, notes_index
    if symbol == pyglet.window.key.SPACE:
        if vocal_range_test == Vocal_Range.DESCRIPTION:
            vocal_range_test = Vocal_Range.LOW_TEST
        elif vocal_range_test == Vocal_Range.LOW_TESTED:
            vocal_range_test = Vocal_Range.HIGH_TEST
        elif vocal_range_test == Vocal_Range.HIGH_TESTED:
            vocal_range_test = Vocal_Range.DESCRIPTION
        elif vocal_range_test == Vocal_Range.LOW_TEST and notes_index < len(low_notes):
            notes_index += 1
            if notes_index + 1 >= len(low_notes):
                notes_index = 0
                vocal_range_test = Vocal_Range.LOW_TESTED
        elif vocal_range_test == Vocal_Range.HIGH_TEST and notes_index < len(high_notes):
            notes_index += 1
            if notes_index + 1 >= len(high_notes):
                notes_index = 0
                vocal_range_test = Vocal_Range.HIGH_TESTED
    elif symbol == pyglet.window.key.N:
        if vocal_range_test == Vocal_Range.LOW_TEST:
            vocal_range_test = Vocal_Range.LOW_TESTED
        elif vocal_range_test == Vocal_Range.HIGH_TEST:
            vocal_range_test = Vocal_Range.HIGH_TESTED

clock.schedule_interval(handle_note_input, 0.1)

# run game
app.run()