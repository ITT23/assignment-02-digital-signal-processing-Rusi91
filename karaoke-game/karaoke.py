# GAME: VOCAL RANGE TESTER
#
# DESCRIPTION:
#   - This application is designed to help you test your own vocal range.
#   - The vocal range is tested for low tones and high tones.
#   - Users should try to sing the note given to them. If this succeeds, the next note to be sung comes.
#                -> For example, when testing the low vocal rank, the user starts with a tone that becomes progressively lower.
#                -> If a tone is successfully replicated by the user, it is saved as the lowest or highest achieved tone.
#
#   - The tone to be achieved is on the left and the tone generated by the user is on the right.
#   - The sound generated by the user is formed by converting the sound's major frequency into a musical note.
#   - Each tone can be skipped with the space key (will not be considered as done) and with the N key one can skip to the next test.
#   - The start of a test and the restart of the Vocal Range Tester (at the end) is done with the spacebar.
#
# TEST:
#   - I tested it on several Youtube videos where musicians/singers sang certain pitches (music note was displayed in the video). 
#

import pyaudio
import numpy as np
import librosa
import pyglet
from os import path
from matplotlib import pyplot as plt
from pyglet import app, image, clock
from pyglet.window import Window
# own classes
    # enum for the different vocal test stages
from vocal_range_enum import Vocal_Range
    # handels sound attributes
from sound_manager import Sound_Manager
from scipy.signal import butter, sosfilt

# from audio-sample.py ------------------------------------------------------------------------------------------------------

# Set up audio stream
# reduce chunk size and sampling rate for lower latency
CHUNK_SIZE = 1024 * 4  # Number of audio frames per buffer
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

#----------------------------------------------------------------------------------------------------------------------------

# detects the sound’s major frequency
    # used sources to understand how to do that:
        # SOURCE 1: https://stackoverflow.com/questions/3694918/how-to-extract-frequency-associated-with-fft-values-in-python
        # SOURCE 2: https://dsp.stackexchange.com/questions/78355/how-to-extract-the-dominant-frequency-from-the-audio-wav-file-using-numpy
def extract_major_frequency(data, sampling_rate):
    print(len(data), sampling_rate)
    highpass = butter(1, 1000, btype='hp', analog=False, output='sos', fs=sampling_rate)
    data = sosfilt(highpass, data)
    fft = np.fft.fft(data)
    fft_freqs = np.fft.fftfreq(len(data))
    major_freq_coefficient = np.argmax(np.abs(fft))
    major_freq = fft_freqs[major_freq_coefficient]
    
    return abs(major_freq * sampling_rate)


# vocal ranges to test the low and high areas
    # Since I'm not musical and not very familiar with musical notes, I determined the values ​​using two vocal range test videos.
        # VIDEO 1: https://www.youtube.com/watch?v=0DLEviuO6HM&t=138s
        # VIDEO 2: https://www.youtube.com/watch?v=WQvjXZfcddQ&t=13s
    
# vocal range for low notes
low_notes = ["C5", "C4", "B4", "B3", "A4", "A3", "G4", "G3", "F4", "F3", "E4", "E3", "D4", "D3", "C4", "C3", "B3", "B2", "A3", "A2", \
             "G3", "G2", "F3", "F2", "E3", "E2", "D3", "D2", "C3", "C2", "B2", "B1", "A2", "A1", "G2", "G1", "F2", "F1", "E2", "E1", "C2", "C1"]
# vocal range for high notes
high_notes = ["C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4", "C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A5", "A#5", \
              "B5", "C6", "C#6", "D6", "D#6", "E6", "F6", "F#6", "G6", "G#6", "A6", "A#6", "B6", "C7"]
# position in the tested vocal range (low_notes or high_notes)
notes_index = 0
# initial note input value (note input value = peak frequency converted to a music note)
note_input_empty = ""
# initial value for the highest from the user achieved musical note
highest_achieved_note = "not tested"
# initial value for the lowest from the user achieved musical note
lowest_achieved_note = "not tested"
# enum for the different vocal test stages (initial stage is the test description)
vocal_range_test = Vocal_Range(Vocal_Range.DESCRIPTION)
# handels all the sound properties and attributes to avoid many globals
sound_manager = Sound_Manager(low_notes, high_notes, notes_index, note_input_empty, lowest_achieved_note, highest_achieved_note)

# game window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = Window(WINDOW_WIDTH, WINDOW_HEIGHT)
# path for the success sound (sound if user achieves to sing a musical note)
    # sound source: https://www.youtube.com/watch?v=_q8QmJadSEE -Piano Note C Sound Effect - @Sound Effects
SUCCESS_SOUND_PATH = path.join(path.dirname(__file__), "music/success_sound.mp3")
# path for the background image
    # image source: https://unsplash.com/de/fotos/drir5tDCWF4 @Andrey Konstantinov
BACKGROUND_IMAGE_PATH = path.join(path.dirname(__file__), "pictures/background.png")

@window.event
def on_draw():

    window.clear()
    draw_background() # background image
    # show start description screen
    if vocal_range_test == Vocal_Range.DESCRIPTION:
        draw_start_screen()
    # show vocal test screen for low notes or high notes
    elif vocal_range_test == Vocal_Range.LOW_TEST or vocal_range_test == Vocal_Range.HIGH_TEST:
        draw_tested_note()
        draw_input_note()
        draw_scip_message()
    # if vocal test for low notes is finished show start screen for the high notes vocal test
    elif vocal_range_test == Vocal_Range.LOW_TESTED:
        draw_next_test_screen()
    # if vocal test for high notes is finished too show result screen
    elif vocal_range_test == Vocal_Range.HIGH_TESTED:
        draw_result_screen()

# draw background image
def draw_background():
    background_image = image.load(BACKGROUND_IMAGE_PATH)
    background_image.blit(0,0)

# draw the musical note which the user has to sing (left side of screen)
def draw_tested_note():

    tested_note = ""
    # determine if vocal test for low or high notes
    if vocal_range_test == Vocal_Range.LOW_TEST:
        tested_note = sound_manager.get_next_low_note()
        draw_test_title("VOCAL TEST FOR LOW RANGE")
    else:
        tested_note = sound_manager.get_next_high_note()
        draw_test_title("VOCAL TEST FOR HIGH RANGE")
        
    # title 
    tested_note_desc_label = pyglet.text.Label("GOAL",
                          font_name='Times New Roman',
                          font_size=30,
                          x = WINDOW_WIDTH / 4,
                          y = WINDOW_HEIGHT / 2 + WINDOW_HEIGHT / 5,
                          anchor_x='center', anchor_y='center')
    
    # note
    tested_note_label = pyglet.text.Label(tested_note,
                          font_name='Times New Roman',
                          font_size=60,
                          x = WINDOW_WIDTH / 4,
                          y = WINDOW_HEIGHT / 2,
                          anchor_x='center', anchor_y='center')
    
    tested_note_desc_label.draw()
    tested_note_label.draw()

# draw the input note (right side of screen)
def draw_input_note():

    # title
    input_note_desc_label = pyglet.text.Label("INPUT",
                          font_name='Times New Roman',
                          font_size=30,
                          x = WINDOW_WIDTH / 2 + WINDOW_WIDTH / 4,
                          y = WINDOW_HEIGHT / 2 + WINDOW_HEIGHT / 5,
                          anchor_x='center', anchor_y='center')
    
    # note
    input_note_label = pyglet.text.Label(sound_manager.get_note_input(),
                          font_name='Times New Roman',
                          font_size=60,
                          x = WINDOW_WIDTH / 2 + WINDOW_WIDTH / 4,
                          y = WINDOW_HEIGHT / 2,
                          anchor_x='center', anchor_y='center')
    
    input_note_desc_label.draw()
    input_note_label.draw()

# draw vocal test title (for low notes / for high notes)
def draw_test_title(title):

    test_title_label = pyglet.text.Label(title,
                          font_name='Times New Roman',
                          font_size=20,
                          x = WINDOW_WIDTH / 2,
                          y = WINDOW_HEIGHT * 0.9,
                          anchor_x='center', anchor_y='center')

    test_title_label.draw()

# draw scip message (to scip the current note)
def draw_scip_message():

    scip_message_label = pyglet.text.Label("Press -spacebar- to skip the note or -N- to skip the test.",
                          font_name='Times New Roman',
                          font_size=15,
                          x = WINDOW_WIDTH / 2,
                          y = WINDOW_HEIGHT * 0.1,
                          anchor_x='center', anchor_y='center')

    scip_message_label.draw()

# handle sound input from sound device
def handle_note_input(dt):
    global vocal_range_test
    # Read audio data from stream 
    data = stream.read(CHUNK_SIZE)
    # Convert audio data to numpy array 
    data = np.frombuffer(data, dtype=np.int16)
    # detects the sound’s major frequency

    if np.max(data) > 10000:
        most_frequ = extract_major_frequency(data, RATE)
    else:
        return

    if int(most_frequ) != 0 :

        low_note_goal = sound_manager.get_next_low_note()
        high_note_goal = sound_manager.get_next_high_note()
        low_notes_arr = sound_manager.get_low_notes_arr()
        high_notes_arr = sound_manager.get_high_notes_arr()
        notes_arr_index = sound_manager.get_notes_index()
        # convert sound's major frequency to a musical note
            # doc: https://librosa.org/doc/main/generated/librosa.hz_to_note.html
        sound_manager.set_note_input(librosa.hz_to_note(most_frequ))
        note_input = sound_manager.get_note_input()

        # vocal test for low notes
            # if input sound (note) matches the desired note
        if vocal_range_test == vocal_range_test.LOW_TEST and note_input == low_note_goal and notes_arr_index + 1 < len(low_notes_arr):
                # play sound
            play_success_sound()
                # set index to the next note to test
            sound_manager.set_notes_index(notes_arr_index + 1)
                # set lowest achieved note to sound input (note)
            sound_manager.set_lowest_achieved_note(note_input)
                # if it was the last note of the low notes arr 
            if notes_index + 1 >= len(low_notes_arr):
                    # start vocal test for high notes
                vocal_range_test = vocal_range_test.LOW_TESTED
                    # set index to 0 (start of the high notes array)
                sound_manager.set_notes_index(0)
        # vocal test for low notes
            # if input sound (note) matches the desired note
        elif vocal_range_test == vocal_range_test.HIGH_TEST and note_input == high_note_goal and notes_arr_index + 1 < len(high_notes_arr):
                # play sound
            play_success_sound()
                # set index to the next note to test
            sound_manager.set_notes_index(notes_arr_index + 1)
                # set highest achieved note to sound input (note)
            sound_manager.set_highest_achieved_note(note_input)
            if notes_arr_index + 1 >= len(high_notes_arr):
                # init the results
                vocal_range_test = vocal_range_test.HIGH_TESTED
                sound_manager.set_notes_index(0)

        # latency test
        print("Peak frequency is " + str(most_frequ) + " (" + note_input + ")")

# draw start screen
def draw_start_screen():
    # title
    description_overall = pyglet.text.Label("VOCAL RANGE TESTER",
                          font_name='Times New Roman',
                          font_size=40,
                          x = WINDOW_WIDTH/2, y = WINDOW_HEIGHT / 1.5,
                          anchor_x = 'center', anchor_y = 'center')
    
    # start info
    description_continue = pyglet.text.Label("Press the - spacebar key - to start the test for LOW RANGE.",
                          font_name='Times New Roman',
                          font_size=20,
                          x = WINDOW_WIDTH / 2, y = WINDOW_HEIGHT / 3,
                          anchor_x = 'center', anchor_y = 'center')
    
    description_overall.draw()
    description_continue.draw()

# draw start screen for vocal test of high notes
def draw_next_test_screen():
    # title
    description_overall = pyglet.text.Label("VOCAL TEST FOR HIGH RANGE",
                          font_name='Times New Roman',
                          font_size=40,
                          x = WINDOW_WIDTH/2, y = WINDOW_HEIGHT / 1.5,
                          anchor_x = 'center', anchor_y = 'center')
    
    # start info
    description_continue = pyglet.text.Label("Press the - spacebar key - to start the test.",
                          font_name='Times New Roman',
                          font_size=20,
                          x = WINDOW_WIDTH / 2, y = WINDOW_HEIGHT / 3,
                          anchor_x = 'center', anchor_y = 'center')
    
    description_overall.draw()
    description_continue.draw()

# draw results screen
def draw_result_screen():
    
    # title
    result_overall = pyglet.text.Label("YOUR VOCAL RANGE",
                          font_name='Times New Roman',
                          font_size=30,
                          x = WINDOW_WIDTH/2, y = WINDOW_HEIGHT * 0.9,
                          anchor_x = 'center', anchor_y = 'center')
    
    # results for lowest achieved note
    result_lowest_note = pyglet.text.Label("Your lowest achieved note is " + sound_manager.get_lowest_achieved_note(),
                          font_name='Times New Roman',
                          font_size=20,
                          x = WINDOW_WIDTH/2, y = WINDOW_HEIGHT * 0.7,
                          anchor_x = 'center', anchor_y = 'center')
    
    # results for highest achieved note
    result_highest_note = pyglet.text.Label("Your highest achieved note is " + sound_manager.get_highest_achieved_note(),
                          font_name='Times New Roman',
                          font_size=20,
                          x = WINDOW_WIDTH/2, y = WINDOW_HEIGHT * 0.5,
                          anchor_x = 'center', anchor_y = 'center')
    
    # restart test
    restart_label = pyglet.text.Label("Press -spacebar- to restart the test.",
                          font_name='Times New Roman',
                          font_size=15,
                          x = WINDOW_WIDTH / 2,
                          y = WINDOW_HEIGHT * 0.1,
                          anchor_x='center', anchor_y='center')
    
    result_overall.draw()
    result_lowest_note.draw()
    result_highest_note.draw()
    restart_label.draw()
    
@window.event
def on_key_press(symbol, modifiers):
    global vocal_range_test

    low_notes_arr = sound_manager.get_low_notes_arr()
    high_notes_arr = sound_manager.get_high_notes_arr()
    notes_arr_index = sound_manager.get_notes_index()
    
    # spacebar used to start each test, to skip notes and at the end to restart test
    if symbol == pyglet.window.key.SPACE:
        if vocal_range_test == Vocal_Range.DESCRIPTION:
            vocal_range_test = Vocal_Range.LOW_TEST
        elif vocal_range_test == Vocal_Range.LOW_TESTED:
            vocal_range_test = Vocal_Range.HIGH_TEST
        elif vocal_range_test == Vocal_Range.HIGH_TESTED:
            vocal_range_test = Vocal_Range.DESCRIPTION
            sound_manager.set_lowest_achieved_note("not tested")
            sound_manager.set_highest_achieved_note("not tested")
        elif vocal_range_test == Vocal_Range.LOW_TEST and notes_arr_index < len(low_notes_arr):
            sound_manager.set_notes_index(notes_arr_index + 1)
            if notes_arr_index + 1 >= len(low_notes_arr):
                sound_manager.set_notes_index(0)
                vocal_range_test = Vocal_Range.LOW_TESTED
        elif vocal_range_test == Vocal_Range.HIGH_TEST and notes_arr_index < len(high_notes_arr):
            sound_manager.set_notes_index(notes_arr_index + 1)
            if notes_arr_index + 1 >= len(high_notes_arr):
                sound_manager.set_notes_index(0)
                vocal_range_test = Vocal_Range.HIGH_TESTED
    # N is used to skip a whole test section
    elif symbol == pyglet.window.key.N:
        if vocal_range_test == Vocal_Range.LOW_TEST:
            vocal_range_test = Vocal_Range.LOW_TESTED
        elif vocal_range_test == Vocal_Range.HIGH_TEST:
            vocal_range_test = Vocal_Range.HIGH_TESTED

# play sound if user achieved to sing a note
def play_success_sound():
    success_sound = pyglet.media.load(SUCCESS_SOUND_PATH, streaming=False)
    success_sound.play()

# latency of input sound
clock.schedule_interval(handle_note_input, 0.1)

# run game
app.run()

