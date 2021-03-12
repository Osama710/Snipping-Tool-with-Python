import tkinter as tk
from tkinter import *
import pyautogui
import webbrowser
from tkinter import ttk, messagebox

class Application():
    def __init__(self) -> None:

        self.bg = "#00203F"
        self.fg = "#ADEFD1"

        self.main_window = self.createWindow("Snipping Tool")
        self.main_window.config(bg=self.bg)

        self.title = tk.Label(self.main_window, text="SNIPPING TOOL", font=("HELVETICA",28,"bold"),bg=self.bg,fg=self.fg)
        self.title.grid(row=0,column=0,sticky=N,pady=(40,20),padx=40)

        self.desc = tk.Label(self.main_window, text="Click the button below and snip the image.",font=("ARIAL",12),bg=self.bg,fg=self.fg)
        self.desc.grid(row=1,column=0,padx=20, pady=20)

        self.snip_button = tk.Button(self.main_window,text="Snip image", font=("TIMES NEW ROMAN",14),bg=self.fg,fg=self.bg, height = 2, width = 12, command = self.snipImage, bd=7, relief=RAISED)
        self.snip_button.grid(row=2,column=0, pady=30,padx=20)
        
        self.menu = tk.Menu(self.main_window)

        self.info = tk.Menu(self.menu,tearoff=0)
        self.info.add_command(label="Muhammad Osama", command=self.opengit)

        self.menu.add_cascade(label="Developed By",menu=self.info)

        self.ex = tk.Menu(self.menu,tearoff=0)
        self.ex.add_command(label="Exit",command=self.eex)

        self.menu.add_cascade(label="Exit",menu=self.ex)

        self.main_window.config(menu=self.menu)

        #bring to front
        self.raise_above_all(self.main_window)

    def startMainLoop(self):
        """ Driver method """
        self.main_window.mainloop()

    #widget creation method
    def createWindow(self,title):
        window = tk.Tk()
        window.title(title)
        window.geometry("")
        return window

    def takeBoundedScreenShot(self, x1, y1, x2, y2):
        im = pyautogui.screenshot(region=(x1, y1, x2, y2))
        im.save("Capture.png")

    def snipImage(self):
        self.rect = None
        self.x = self.y = 0
        self.start_x = None
        self.start_y = None
        self.curX = None
        self.curY = None
        
        self.master_screen = Toplevel(self.main_window)
        self.master_screen.withdraw()
        self.master_screen.attributes("-transparent", "blue")
        self.picture_frame = Frame(self.master_screen, background = "blue")
        self.picture_frame.pack(fill=BOTH, expand=YES)
        
        self.master_screen.deiconify()
        self.main_window.withdraw()

        self.screenCanvas = Canvas(self.picture_frame, cursor="cross", bg="grey11")
        self.screenCanvas.pack(fill=BOTH, expand=YES)

        self.screenCanvas.bind("<ButtonPress-1>", self.on_button_press)
        self.screenCanvas.bind("<B1-Motion>", self.on_move_press)
        self.screenCanvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.master_screen.attributes('-fullscreen', True)
        self.master_screen.attributes('-alpha', .3)
        self.master_screen.lift()
        self.master_screen.attributes("-topmost", True)

    def on_button_release(self, event):
        separator = ttk.Separator(self.main_window, orient='horizontal') 
        separator.place(y=40,relx=0, rely=0.47, relwidth=1)

        self.inf = tk.Label(self.main_window,text="Screenshot Information", font=("HELVETICA",14,"bold"),bg=self.bg,fg=self.fg)
        self.inf.grid(row=3,column=0,padx=20,pady=20)

        self.lbl = tk.Label(self.main_window, text=str(self.start_x)+"\n"+str(self.start_y)+"\n"+str(self.curX)+"\n"+str(self.curY), font=("HELVETICA",12),bg=self.bg,fg=self.fg)
        self.lbl.grid(row=4,column=0,padx=20)

        separator = ttk.Separator(self.main_window, orient='horizontal') 
        separator.place(y=240,relx=0, rely=0.47, relwidth=1)

        self.inff = tk.Label(self.main_window,text="Mouse Position", font=("HELVETICA",14,"bold"),bg=self.bg,fg=self.fg)
        self.inff.grid(row=5,column=0,padx=20,pady=20)
        
        self.pos = tk.Label(self.main_window,text="", font=("HELVETICA",12),bg=self.bg,fg=self.fg)

        if self.start_x <= self.curX and self.start_y <= self.curY:
            self.pos["text"] = "From Left to Downward"
            self.takeBoundedScreenShot(self.start_x, self.start_y, self.curX - self.start_x, self.curY - self.start_y)

        elif self.start_x >= self.curX and self.start_y <= self.curY:
            self.pos["text"] = "From Right to Downward"
            self.takeBoundedScreenShot(self.curX, self.start_y, self.start_x - self.curX, self.curY - self.start_y)

        elif self.start_x <= self.curX and self.start_y >= self.curY:
            self.pos["text"] = "From Left to Upward"
            self.takeBoundedScreenShot(self.start_x, self.curY, self.curX - self.start_x, self.start_y - self.curY)

        elif self.start_x >= self.curX and self.start_y >= self.curY:
            self.pos["text"] = "From Right to Upward"
            self.takeBoundedScreenShot(self.curX, self.curY, self.start_x - self.curX, self.start_y - self.curY)

        self.pos.grid(row=6,column=0,padx=20,pady=10)
        
        self.master_screen.withdraw()

        messagebox.showinfo("Done!","Screenshot Taken and Saved!")

        self.main_window.deiconify()
        return event

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = self.screenCanvas.canvasx(event.x)
        self.start_y = self.screenCanvas.canvasy(event.y)

        self.rect = self.screenCanvas.create_rectangle(self.x, self.y, 1, 1, outline='red', width=3, fill="blue")

    def on_move_press(self, event):
        self.curX, self.curY = (event.x, event.y)
        # expand rectangle as you drag the mouse
        self.screenCanvas.coords(self.rect, self.start_x, self.start_y, self.curX, self.curY)

    def raise_above_all(self, window):
        """ brings window to the front """
        window.attributes('-topmost', 1)
        window.attributes('-topmost', 0)

    def opengit(self):
        webbrowser.open("https://www.flowcode.com/page/osamayousuf")

    def eex(self):
        self.main_window.destroy()
        sys.exit()

app = Application()
app.startMainLoop()
