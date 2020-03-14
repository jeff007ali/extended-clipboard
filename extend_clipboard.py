from pynput import keyboard
from pynput.keyboard import Controller, Key
import pyperclip
import time
import datetime

kb = Controller()
paste_flag = False
index = float('inf')
injected = False  

def get_today_date():
    date = datetime.datetime.now()
    return date.strftime("%d%m%Y")

def get_clipboard_archive_data():
    try:
        with open("clipboard_archiver_{}.txt".format(get_today_date()), "r") as arch_file:
            arch_data = arch_file.read()
    except FileNotFoundError:
        with open("clipboard_archiver_{}.txt".format(get_today_date()), "x") as arch_file:
            arch_data = ''
    
    if arch_data:
        return arch_data.split(':end\n\nstart:')
    else:
        return list()

clipboard_archive_data_list = get_clipboard_archive_data()

def read_clipboard_data():
    return pyperclip.paste()

def write_clipboard_data(data):
    pyperclip.copy(data)

def clear_clipboard_data():
    pyperclip.copy('')

def select_text(text):
    # kb = Controller()
    print("in select text")
    words = text.split()
    # words = words[:-1]
    # text = ' '.join(words)
    print(words)

    # ctrl+shift+left will select word
    print("Before : Is ctrl pressed : {}".format(kb.ctrl_pressed))
    print("Before : Is shift pressed : {}".format(kb.shift_pressed))
    # kb.press(Key.ctrl)
    kb.release(Key.ctrl)
    kb.press(Key.shift)
    print("middle : Is ctrl pressed : {}".format(kb.ctrl_pressed))
    print("middle : Is shift pressed : {}".format(kb.shift_pressed))
    for c in text:
        print(c)
        kb.press(Key.left)
        kb.release(Key.left)
        time.sleep(0.05)
    kb.release(Key.shift)
    # kb.release(Key.ctrl)
    # time.sleep(0.05)
    print("After : Is ctrl pressed : {}".format(kb.ctrl_pressed))
    print("After : Is shift pressed : {}".format(kb.shift_pressed))

def paste_text_in_archiver_file():
    global paste_flag
    paste_flag = False

    # TODO : before copy check that previous copied text is same or not

    # populate list to get data faster for paste
    clipboard_archive_data_list.append(read_clipboard_data())
    print("in copy : {}".format(clipboard_archive_data_list))

    # logs clipboard data for history purpose
    with open("clipboard_archiver_{}.txt".format(get_today_date()), "a") as arch_file:
        arch_file.write(":end\n\nstart:")
        arch_file.write(read_clipboard_data())

def paste_text():
    global paste_flag
    global injected
    paste_flag = True
    print("actual paste : {}".format(read_clipboard_data()))
    if not injected:
        pass
        # select_text(read_clipboard_data())

def manual_paste():
    # kb = Controller()
    global injected
    injected = True
    print("START Manual paste")
    kb.press(Key.ctrl)
    kb.press('v')
    kb.release('v')
    kb.release(Key.ctrl)
    # time.sleep(0.05)
    # select_text(read_clipboard_data())
    print("END manual paste")

def paste_previous_text():
    if paste_flag:
        global index
        global clipboard_archive_data_list
        # print("in previous paste : {}".format(clipboard_archive_data_list))
        ln = len(clipboard_archive_data_list)
        if ln > 1:
            if index == float('inf'):
                index = ln - 2
            else:
                index = index - 1 if index - 1 >= 0 else index
            write_clipboard_data(clipboard_archive_data_list[index])
            manual_paste()

def paste_next_text():
    if paste_flag:
        global index
        global clipboard_archive_data_list
        # print("in next paste : {}".format(clipboard_archive_data_list))
        ln = len(clipboard_archive_data_list)
        if ln > 1:
            if index == float('inf'):
                index = ln - 1
            else:
                index = ln - 1 if index == ln - 1 else index + 1
            write_clipboard_data(clipboard_archive_data_list[index])
            manual_paste()
        
    

# sometimes gives weird behaviour
with keyboard.GlobalHotKeys({
        '<ctrl>+c': paste_text_in_archiver_file,
        '<ctrl>+x': paste_text_in_archiver_file,
        '<ctrl>+v': paste_text,
        '<alt>+q':paste_previous_text,
        '<alt>+a':paste_next_text,
        }) as h:
    h.join()