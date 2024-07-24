from pynput.keyboard import Key, Controller
import keyboard
import pyperclip
import os
import time
import re
from threading import Thread

def clear_keys():
    while True:
        # Hotkeys stop working after windows locks & unlocks
        # https://github.com/boppreh/keyboard/issues/223
        deleted = []
        with keyboard._pressed_events_lock:
            for k in list(keyboard._pressed_events.keys()):
                item = keyboard._pressed_events[k]
                if time.time() - item.time > 2:
                    deleted.append(item.name)
                    del keyboard._pressed_events[k]
        if deleted:
            print(f'Deleted keys: {deleted}')
        time.sleep(1)

Thread(target=clear_keys).start()

SEQUENCES = ["porn", "xvideo", "xvidéo","twerk","blowjob","xnxx", "xhamster", "redtube", "brazzers", "hentai", "yaoi", "rule34", "r34", "anal", "gangbang", "sex amateur", "amateur sex", "hardcore sex", "sex hardcore", "big ass"]
sequence_indices = [0] * len(SEQUENCES)
mots = ""
mots2 = ""
copied_text = ""
copied_text2 = ""

keyboard_obj = Controller()
def select_right():
    keyboard_obj.press(Key.shift)
    keyboard_obj.press(Key.end)
    time.sleep(0.0001) 
    keyboard_obj.release(Key.end)
    keyboard_obj.release(Key.shift)

def select_left():
    keyboard_obj.press(Key.shift)
    keyboard_obj.press(Key.home)
    time.sleep(0.0001)
    keyboard_obj.release(Key.home)
    keyboard_obj.release(Key.shift)

def copy_text():
    global copied_text
    select_right()
    keyboard.press_and_release('ctrl+c')
    keyboard.press_and_release('ctrl+c')
    time.sleep(0.001)
    copied_text = pyperclip.paste()
    select_left()
    keyboard.press_and_release('ctrl+c')
    keyboard.press_and_release('ctrl+c')
    time.sleep(0.001)
    copied_text = pyperclip.paste() + copied_text
    keyboard.press_and_release('right')
    keyboard.press_and_release('enter')

def copy_text2():
    global copied_text
    select_right()
    keyboard.press_and_release('ctrl+c')
    keyboard.press_and_release('ctrl+c')
    time.sleep(0.001)
    copied_text = pyperclip.paste()
    select_left()
    keyboard.press_and_release('ctrl+c')
    keyboard.press_and_release('ctrl+c')
    time.sleep(0.001)
    copied_text = pyperclip.paste() + copied_text
    keyboard.press_and_release('left')
    keyboard.press_and_release('enter')

def shutdown_system():
    os.system("shutdown /s /f /t 0")


def nettoyer_chaine(chaine):
    motifs_echappes = [
        r'\n',      
        r'\r',      
        r'\t',      
        r'\v',      
        r'\f',      
        r'\\',      
        r'\'',      
        r'\"',      
    ]
    motif_combine = '|'.join(motifs_echappes)
    
    chaine_nettoyee = re.sub(motif_combine, '', chaine)
    
    return chaine_nettoyee

def check_long_word(event):
    global mots
    global copied_text
    mots2 = ""
    copied_text2 = ""
    if len(event.name) != 1 and event.name != 'space':
        name = ''
    elif event.name == 'space' :
        name = ' '
    else : name = event.name
    if event.name == 'backspace' and len(mots) > 0 :
        mots = mots[:len(mots)-1]
    else :
        mots += name
    
    mots2 = nettoyer_chaine(mots).replace(' ', '').lower()
    copied_text2 = nettoyer_chaine(copied_text2).replace(' ', '').lower()
    for seq in SEQUENCES :
        if seq in mots or seq in copied_text or seq in mots2 or seq in copied_text2:
            shutdown_system()
            mots = ""

    if len(mots) > 200 :
        mots = mots[100:]

def on_key_event(event):
    global sequence_indices
    check_long_word(event)
    try:
        for i, seq in enumerate(SEQUENCES):
            if event.name == 'space' :
                name = ' '
            else : name = event.name 

            if name == seq[sequence_indices[i]] :
                sequence_indices[i] += 1
                if sequence_indices[i] == len(seq): 
                    shutdown_system()
                    sequence_indices[i] = 0
            elif name == 'backspace' and sequence_indices[i] > 0:
                sequence_indices[i] -= 1
            else:
                sequence_indices[i] = 0 
    except:
        sequence_indices = [0] * len(SEQUENCES)  


keyboard.add_hotkey('enter', copy_text, suppress=True)
keyboard.add_hotkey('shift+enter', copy_text2, suppress=True)
keyboard.add_hotkey('ctrl+enter', copy_text, suppress=True)

keyboard.on_press(on_key_event)

while True:
    time.sleep(1)