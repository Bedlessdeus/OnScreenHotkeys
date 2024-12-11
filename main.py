import tkinter, win32api, win32con, pywintypes, screeninfo
from pynput import keyboard

def int_to_string(value: int):
    if value < 0:
        return f"-{value}"
    else:
        return f"+{value}"

def get_primary_monitor():
    for monitor in screeninfo.get_monitors():
        if monitor.is_primary:
            return monitor

def list_keys(keys):
    if len(keys) == 0:
        return ""
    elif len(keys) == 1:
        try:
            return keys[0]
        except Exception as e:
            return ""
    else:
        return " + ".join(keys)

def create_window(text: str, font: str, font_size: int, fg: str, bg: str, x: int, y: int):
    label = tkinter.Label(text=text, font=(font, str(font_size)), fg=fg, bg=bg)
    master = label.master

    master.overrideredirect(True)
    master.geometry(f"{int_to_string(x)}{int_to_string(y)}")
    master.lift()
    master.wm_attributes("-topmost", True)
    master.wm_attributes("-disabled", True)
    master.wm_attributes("-transparentcolor", "black")

    exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
    win32api.SetWindowLong(pywintypes.HANDLE(int(master.frame(), 16)), win32con.GWL_EXSTYLE, exStyle)

    label.pack()
    return label

class KeyPressApp:

    def __init__(self, root):
        self.root = root
        self.pressed_keys = set()
        self.last_window = None
        self.listener = keyboard.Listener(on_press=self.on_key_press, on_release=self.on_key_release)
        self.listener.start()

    def on_key_press(self, key):
        try:
            self.pressed_keys.add(key.char)
        except AttributeError:
            self.pressed_keys.add(str(key))
        print(list_keys(self.pressed_keys))
        if len(self.pressed_keys) > 1:
            print("Creating window")
            self.last_window = create_window(list_keys(self.pressed_keys), 'Times New Roman', 30, 'white', 'black', 20, get_primary_monitor().height - 100)

    def on_key_release(self, key):
        try:
            self.pressed_keys.discard(key.char)
        except AttributeError:
            self.pressed_keys.discard(str(key))
        if self.last_window is not None and len(self.pressed_keys) == 0:
            print("Destroying window")
            #self.last_window.destroy()
            self.last_window = None

if __name__ == "__main__":
    root = tkinter.Tk()
    root.withdraw()
    app = KeyPressApp(root)
    root.mainloop()