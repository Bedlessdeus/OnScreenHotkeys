import tkinter
import window
from util import list_keys
from pynput import keyboard

class KeyPressApp:

    def __init__(self, root):
        self.root = root
        self.pressed_keys = set()
        self.last_window : window.Window = window.Window()
        self.last_window.create_window()
        self.listener = keyboard.Listener(on_press=self.on_key_press, on_release=self.on_key_release)
        self.listener.start()

    def on_key_press(self, key):
        try:
            self.pressed_keys.add(key.char)
        except AttributeError:
            self.pressed_keys.add(str(key))
        if len(self.pressed_keys) > 1:
            print(list_keys(self.pressed_keys))
            self.last_window.overwrite_master(list_keys(self.pressed_keys))

    def on_key_release(self, key):
        try:
            self.pressed_keys.discard(key.char)
            print(f"Dropped Key {key.char}")
            self.last_window.overwrite_master(list_keys(self.pressed_keys))
        except AttributeError as ex:
            self.pressed_keys.discard(str(key))
            print(f"Dropped Key {str(key)}")
            self.last_window.overwrite_master(list_keys(self.pressed_keys))

if __name__ == "__main__":
    root = tkinter.Tk()
    #root.withdraw()
    app = KeyPressApp(root)
    root.mainloop()
