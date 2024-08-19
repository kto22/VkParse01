
from tkinter import filedialog, PhotoImage, Label, Frame, Entry, Button, Tk
import os


class App:

    def __init__(self, master):

        our_img = PhotoImage(file="kona2.gif")
        our_img = our_img.subsample(5, 5)
        our_label = Label(root)
        our_label.image = our_img
        our_label['image'] = our_label.image
        our_label.place(x=0, y=0)

        frame_top = Frame(root, bg='#000000', bd=5)
        lbl = Label(root, text="nya~ nipaaa~~ (づ｡◕‿‿◕｡)づ", font=("Arial Bold", 20))
        lbl.grid(column=0, row=0)

        frame_top.place(relx=0, rely=0.79, relwidth=1, relheight=0.21)

        self.direct = Entry(frame_top, bg='white', font=30)
        self.direct.pack()

        btn = Button(frame_top, text='Nipaaah~~~', command=self.main)
        btn.pack(padx=2, pady=12)

    def main(self):

        user_dir = self.direct.get()
        if not os.path.isdir(f"{user_dir}"):
            user_dir = filedialog.askdirectory()

        check_dir(f"{user_dir}/sorted00")
        check_dir(f"{user_dir}/sorted00/anime")
        check_dir(f"{user_dir}/sorted00/not_anime")

        if os.path.isdir(f'{user_dir}/temp00'):
            os.rmdir(f'{user_dir}/temp00')

        os.mkdir(f'{user_dir}/temp00')
        os.mkdir(f'{user_dir}/temp00/temp01')

        t1 = time()

        for filename in os.listdir(user_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', 'tiff')):
                os.replace(f'{user_dir}/{filename}', f'{user_dir}/temp00/temp01/temp.jpg')
                datagen = ImageDataGenerator(rescale=1. / 255)
                img_generator = datagen.flow_from_directory(f'{user_dir}/temp00',
                                                            target_size=(150, 150),
                                                            batch_size=1,
                                                            class_mode='binary')

                predictions = model.predict(img_generator)

                pred_num = predictions[0][0]
                print(pred_num)

                if float(pred_num) < 0.4:
                    os.replace(f'{user_dir}/temp00/temp01/temp.jpg', f'{user_dir}/sorted00/anime/{filename}')
                else:
                    os.replace(f'{user_dir}/temp00/temp01/temp.jpg', f'{user_dir}/sorted00/not_anime/{filename}')

        os.rmdir(f'{user_dir}/temp00/temp01')
        os.rmdir(f'{user_dir}/temp00')
        print(time()-t1)


root = Tk()

root['bg'] = '#fafafa'

root.title('Neuronime!')

root.geometry('355x374')

root.resizable(width=False, height=False)

app = App(root)

root.mainloop()
