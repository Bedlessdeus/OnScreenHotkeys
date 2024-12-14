from time import sleep

from util import get_primary_monitor, int_to_string
import tkinter, win32api, win32con, pywintypes, win32gui

class Window:
    def __init__(self, text: str = "No Text here :(", font: str = "Times New Roman", font_size: int = 30, fg: str = "white", bg: str = "black", x: int = 20, y: int = get_primary_monitor().height - 100):
        self.text = text
        self.font = font
        self.font_size = font_size
        self.fg = fg
        self.bg = bg
        self.x = x
        self.y = y
        self.label = None
        self.master = None

    def create_window(self):
        self.label = tkinter.Label(text=self.text, font=(self.font, str(self.font_size)), fg=self.fg, bg=self.bg)
        master = self.label.master
        master.overrideredirect(True)
        master.geometry(f"{int_to_string(self.x)}{int_to_string(self.y)}")
        master.lift()
        master.wm_attributes("-topmost", True)
        master.wm_attributes("-disabled", True)
        master.wm_attributes("-transparentcolor", "black")

        exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
        win32api.SetWindowLong(pywintypes.HANDLE(int(master.frame(), 16)), win32con.GWL_EXSTYLE, exStyle)
        self.master = master
        self.label.pack()
        self.show_window()
        return self.label

    def overwrite_master(self, text: str = "No Text here :(", font: str = "Times New Roman", font_size: int = 30, fg: str = "white", bg: str = "black", x: int = 20, y: int = get_primary_monitor().height - 100):
        if self.label is None:
            return
        self.label.config(text=text, font=(font, str(font_size)), fg=fg, bg=bg)
        self.show_window()
        return self.label

    async def destroy_window(self):
        win32gui.PostMessage(pywintypes.HANDLE(int(self.master.frame(), 16)), win32con.WM_CLOSE, 0, 0)
        self.label = None
        self.master = None

    async def destroy_window_later(self, milli: int):
        sleep(milli / 1000)
        await self.destroy_window()

    async def hide_window(self):
        self.master.withdraw()

    async def hide_window_later(self, milli: int):
        sleep(milli / 1000)
        await self.hide_window()

    async def show_window(self):
        self.master.deiconify()

    async def show_window_later(self, milli: int):
        sleep(milli / 1000)
        await self.show_window()

    async def cut_first(self):
        self.label.config(text=self.label.cget("text")[3:])