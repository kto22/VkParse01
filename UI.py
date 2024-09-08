
from tkinter import filedialog, PhotoImage, Label, Frame, Entry, Button, Tk, END
import os


# Input boxes class
class InputBox:

    __slots__ = ("text", "frame_top", "ent_widget")

    def __init__(self, frame_top, text) -> None:
        self.text = text
        self.frame_top = frame_top
        self.ent_widget = Entry(frame_top, bg='white', font=30)
        self.ent_widget.config(fg='grey')
        self.ent_widget.insert(0, text)
        self.ent_widget.pack(side='top', fill='x')
        global resp
        resp = ""

    def get(self):
        resp = self.ent_widget.get()
        self.frame_top.destroy()
        return resp


    def handle_focus_in(self, master) -> None:
        if self.ent_widget.get() == '' or self.ent_widget.get() == self.text:
            self.ent_widget.delete(0, END)
            self.ent_widget.config(fg='black')

    def handle_focus_out(self, master) -> None:
        if self.ent_widget.get() == '':
            self.ent_widget.delete(0, END)
            self.ent_widget.config(fg='grey')
            self.ent_widget.insert(0, self.text)

    def next_widget(self, master) -> None:
        self.ent_widget.tk_focusNext().focus()

    def previous_widget(self, master) -> None:
        self.ent_widget.tk_focusPrev().focus()

    def run(self) -> None:
        self.ent_widget.bind("<FocusIn>", self.handle_focus_in)
        self.ent_widget.bind("<FocusOut>", self.handle_focus_out)
        self.ent_widget.bind("<Down>", self.next_widget)
        self.ent_widget.bind("<Up>", self.previous_widget)


# User interface class
class UI:

    __slots__ = ("token", "username", "friend_name", "friend_id", "start_mes_id", "mes_count", "user_dir")

    def __init__(self, master) -> None:

        # Main frame
        our_img = PhotoImage(file="resources/kona2.gif")
        our_img = our_img.subsample(5, 5)
        our_label = Label(root)
        our_label.image = our_img
        our_label['image'] = our_label.image
        our_label.place(x=0, y=18)

        frame_top = Frame(root, bg='#000000', bd=5)
        lbl = Label(root, text="nya~ nipaaa~~ (づ｡◕‿‿◕｡)づ", font=("Arial Bold", 20))
        lbl.grid(column=0, row=0)

        frame_top.place(relx=0, rely=0.60, relwidth=1, relheight=0.41)

        # Input Boxes
        self.token = InputBox(frame_top, 'Your token')
        self.token.run()

        self.username = InputBox(frame_top, 'Your name')
        self.username.run()

        self.friend_name = InputBox(frame_top, 'Friend name')
        self.friend_name.run()

        self.friend_id = InputBox(frame_top, 'Friend id')
        self.friend_id.run()

        self.start_mes_id = InputBox(frame_top, 'Start message id')
        self.start_mes_id.run()

        self.mes_count = InputBox(frame_top, 'Messages count')
        self.mes_count.run()

        self.user_dir = InputBox(frame_top, 'Directory to save output')
        self.user_dir.run()

        # Buttons
        btn = Button(frame_top, text='Nuclear bomb to USA', command=self.token.get)
        btn.pack(padx=2, pady=12)



root = Tk()
root['bg'] = '#fafafa'
root.title('VkParse!')
root.geometry('355x510')
root.resizable(width=False, height=False)
app = UI(root)
root.mainloop()

