import os
import subprocess
import  datetime
import tkinter as tk
from util import *
import cv2
from PIL import Image, ImageTk


class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry('1200x520+150+100')

        self.login_btn = get_button(self.main_window, 'connexion', 'green', self.login)
        self.login_btn.place(x=850, y=300)

        self.register_btn = get_button(self.main_window, "s'inscrire", 'black', self.register)
        self.register_btn.place(x=850, y=400)

        self.webcam_label = get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height='500')

        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'

    def add_webcam(self, label):
        # create the variable only once
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label

        self.process_webcam()

    # function to put the webcam in the label
    def process_webcam(self):
        ret, frame = self.cap.read()
        # verify  video capture is not null
        if ret and frame is not None:
            self.most_recent_cap_arr = frame

            img_ = cv2.cvtColor(self.most_recent_cap_arr, 4)
            self.most_recent_cap_pil = Image.fromarray(img_)
            imgTk = ImageTk.PhotoImage(image=self.most_recent_cap_pil)
            self._label.imgTk = imgTk
            self._label.configure(image=imgTk)
        else:
            print('Caméra réquis')
            exit(0)

        # repeat the process each 20ms
        self._label.after(20, self.process_webcam)

    def login(self):
        unknown_img_path = './.tmp.jpg'

        cv2.imwrite(unknown_img_path, self.most_recent_cap_arr)

        output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]))
        name = output.split(',')[1][:-5]

        if name in ['unknown_person', 'no_persons_found']:
            msg_box('Oups...', "You're not register or try again ")
        else:
            msg_box('Login Successfully', "Welcome {}.".format(name))
            with open(self.log_path, 'a') as file:
                file.write(f"{name}, {datetime.datetime.now()}\n")
                file.close()

        os.remove(unknown_img_path)

    def register(self):
        self.register_window = tk.Toplevel(self.main_window)
        self.register_window.geometry('1200x520+100+60')

        self.accept_btn = get_button(self.register_window, "Accept", 'black', self.accept_register_new_user)
        self.accept_btn.place(x=850, y=300)

        self.try_again_btn = get_button(self.register_window, "Réssayer", 'red', self.try_again_register_user)
        self.try_again_btn.place(x=850, y=400)

        self.capture_label = get_img_label(self.register_window)
        self.capture_label.place(x=10, y=0, width=700, height='500')

        self.add_img_to_label(self.capture_label)

        self.register_username_input = get_entry_text(self.register_window)
        self.register_username_input.place(x=850, y=150)

        self.register_username_label = get_text_label(self.register_window, 'entry your name : ')
        self.register_username_label.place(x=850, y=100)

    def add_img_to_label(self, label):
        imgTk = ImageTk.PhotoImage(image=self.most_recent_cap_pil)
        label.imgTk = imgTk
        label.configure(image=imgTk)

        self.register_new_capture = self.most_recent_cap_arr.copy()

    def accept_register_new_user(self):
        name = self.register_username_input.get(1.0, 'end-1c')
        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)), self.register_new_capture)
        msg_box('Success', 'User was registered successfully')
        self.register_window.destroy()

    def try_again_register_user(self):
        self.register_window.destroy()

    def start(self):
        self.main_window.mainloop()


if __name__ == '__main__':
    app = App()
    app.start()
