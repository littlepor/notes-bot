import os
import time
from datetime import datetime, timedelta
from instagrapi import Client

# Instagram credentials
USERNAME = "lapo_6090"
PASSWORD = "thitiyakorn2561"

# Constants
BASE_MINUTE_INTERVAL = 1  # Change interval to 1 minute
NOTE_CONTROL = 0.5
MAX_EMOJI_INDEX = 23

# Utility Functions

def generate_cookie(USERNAME, PASSWORD):
    cl = Client()
    cl.login(USERNAME, PASSWORD)
    cl.dump_settings(f"{USERNAME}.json")

def round_to_base(number, base, control):
    rounded = round(number / base) * base
    difference = number - rounded
    if abs(difference) > control * base:
        rounded += base if difference > 0 else -base
    return rounded

def get_time_data():
    seasia_time = datetime.utcnow() + timedelta(hours=7)  # Adding 7 hours for SEASIA time zone
    clock_emojis = ['🕐', '🕜', '🕑', '🕝', '🕒', '🕞', '🕓', '🕟', '🕔', '🕠', '🕕', '🕡',
                    '🕖', '🕢', '🕗', '🕣', '🕘', '🕤', '🕙', '🕥', '🕚', '🕦', '🕛', '🕧']

    time_min = seasia_time.minute
    time_hr = seasia_time.hour

    if time_min < 23:
        quarter = 0
    elif time_min < 53:
        quarter = 1
    else:
        quarter = 2

    emoji_index = ((time_hr * 2) - 2) + quarter
    if emoji_index > MAX_EMOJI_INDEX:
        emoji_index = MAX_EMOJI_INDEX

    return time_hr, time_min, clock_emojis[emoji_index]

def countdown(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = 'Next check on {:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        seconds -= 1

def send_note(note_text):
    cl = Client()
    cl.load_settings(f"{USERNAME}.json")
    cl.login(USERNAME, PASSWORD)
    hr, round_min, emoji = get_time_data()
    print(f"{hr}:{round_min} {emoji} - {note_text}")
    cl.create_note(note_text, 0)
    return f"Posted on {hr}:{round_min}"

# Main Script

if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{USERNAME}.json")):
    print("Using existing cookies")
else:
    generate_cookie(USERNAME, PASSWORD)
    print("Cookies generated")

while True:
    hr, min, emoji = get_time_data()
    rounded_min = round_to_base(min, base=BASE_MINUTE_INTERVAL, control=NOTE_CONTROL)
    
    if rounded_min == 60:
        rounded_min = "00"
        hr += 1

    note_text = f'ตอนนี้{emoji} {hr}:{rounded_min} แล้วนะ'
    
    print(send_note(note_text))
    countdown(60)  # Change countdown to 60 seconds for each minute
