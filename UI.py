from tkinter import *
import keyboard
import json
import webbrowser


class InputBox:

    __slots__ = ("text", "frame_top", "ent_widget")

    def __init__(self, frame_top, text) -> None:
        self.text = text
        self.ent_widget = Entry(frame_top, bg='white', font=30)
        self.ent_widget.config(fg='grey')
        self.ent_widget.insert(0, text)
        self.ent_widget.pack(side='bottom', fill='x')

    def get(self):
        resp = self.ent_widget.get()
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
        self.ent_widget.bind("<Up>", self.next_widget)
        self.ent_widget.bind("<Down>", self.previous_widget)


class InputForm:
    def __init__(self):
        self.response = []

        def get_data(a='a'):
            for i in self.boxes:
                self.response.append(i.get())
            master.destroy()

        def get_token(a='a'):
            webbrowser.open('https://vkhost.github.io/')

        def load_cache(a='a'):
            with open('JSON/InputCache.json', 'r') as f:
                d = json.load(f)

                for i in self.boxes:
                    i.ent_widget.delete(0, END)
                    i.ent_widget.insert(0, d[i.text])
                    i.ent_widget.config(fg='black')

        def write_cache(a='a'):
            with open('JSON/InputCache.json') as f:
                data = json.load(f)

            for i in self.boxes:
                data[i.text] = i.get()

            with open('JSON/InputCache.json', 'w') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

        master = Tk()
        master['bg'] = '#fafafa'
        master.title('VkParse!')
        master.geometry('%dx%d+%d+%d' % (355, 510, 0, 0))
        master.resizable(width=False, height=False)

        our_img = PhotoImage(file="resources/kona2.gif")
        our_img = our_img.subsample(5, 5)
        our_label = Label(master)
        our_label.image = our_img
        our_label['image'] = our_label.image
        our_label.place(x=0, y=-23)

        frame_top = Frame(master, bg='#000000', bd=5)

        frame_top.place(relx=0, rely=0.65, relwidth=1, relheight=0.38)

        frame_top = Frame(master, bg='#000000', bd=5)

        lbl = Label(master)
        lbl.pack()

# -------- Buttons ------------
        data_butt = Button(master, text="Nuclear bomb to USA", command=get_data)
        data_butt.pack(side='bottom', fill='x')
        vk_butt = Button(master, text='Get token', command=get_token)
        vk_butt.pack(side='bottom', fill='x')
        load_butt = Button(master, text='Load cache', command=load_cache)
        load_butt.pack(side='bottom', fill='x')
        write_butt = Button(master, text='Write cache', command=write_cache)
        write_butt.pack(side='bottom', fill='x')

# -------- Input Boxes ----------
        self.token = InputBox(master, 'Your token')
        self.username = InputBox(master, 'Your name')
        self.friend_name = InputBox(master, 'Friend name')
        self.friend_id = InputBox(master, 'Friend id')
        self.start_mes_id = InputBox(master, 'Start message id')
        self.mes_count = InputBox(master, 'Messages count')
        self.user_dir = InputBox(master, 'Directory to save output')

        self.boxes = [self.token,
                      self.username,
                      self.friend_name,
                      self.friend_id,
                      self.start_mes_id,
                      self.mes_count,
                      self.user_dir]

        for i in self.boxes:
            i.run()

        keyboard.add_hotkey(hotkey='esc', callback=master.destroy)
        keyboard.add_hotkey(hotkey='Enter', callback=get_data)

        mainloop()

