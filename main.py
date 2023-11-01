from tkinter import *
from tkinter import filedialog
from pytube import YouTube
from tkinter import ttk
import os
import threading

def handle_next_step():
    next_step_button.place_forget()
    welcome_label_photo.place_forget()
    select_directory_button.place(x=125, y=25)
    select_directory_button.config(state="normal")
    image_directory.place(x=275,y=100)
    url_label.place_forget()
    textfield_for_URL.place_forget()
    start_download_button.place_forget()
    show_download_status("")

def start_download():
    url_entry = textfield_for_URL.get()

    def download_thread():
        reset_prog_bar()
        show_download_status("Downloading...")

        try:
            yt = YouTube(url_entry)
            stream = yt.streams.filter(only_audio=True).first()
            out_file = stream.download(output_path=directory_path)
            artist = yt.author
            song_title = yt.title
            base, ext = os.path.splitext(out_file)
            new_file = os.path.join(directory_path, f"{artist} - {song_title}.mp3")
            os.rename(out_file, new_file)
            update_prog_bar()
        except Exception as e:
            show_download_status("Error: " + str(e))

    download_thread_instance = threading.Thread(target=download_thread)
    download_thread_instance.start()
    progress_bar.place(x=125, y=550)

def select_directory():
    global directory_path
    directory_path = filedialog.askdirectory()
    if directory_path:
        show_directory_label.config(text="The directory is " + str(directory_path))
        create_download_widgets()

def create_download_widgets():
    url_label.place(x=125, y=400)
    textfield_for_URL.place(x=125, y=450)
    start_download_button.place(x=123, y=500)
    download_status_label.place(x=125, y=600)

def reset_prog_bar():
    progress_var.set(0)
    progress_bar.place_forget()

def show_download_status(message):
    download_status_label.config(text=message)

def update_prog_bar():
    progress_bar.place(x=125, y=570)
    if progress_var.get() < 100:
        show_download_status("Wait a few seconds")
        progress_var.set(progress_var.get() + 1)
        window.after(3, update_prog_bar)
    else:
        show_download_status("Download complete")

window = Tk()
icon = PhotoImage(file='mp3.png')
window.title("YouTube MP3 Downloader")
window.iconphoto(True, icon)

welcome_image = PhotoImage(file='welcome.png')
welcome_label_photo = Label(window, image=welcome_image)
welcome_label_photo.place(x=150, y=150)

directory_path = None
progress_var = IntVar()

show_directory_label = Label(text="")

url_label = Label(text="Enter the video URL",font=("Verdana", 20,"bold"),width=30,bg="grey")
textfield_for_URL = Entry()
textfield_for_URL.config(font=("Verdana", 20,"bold"),width=30)
download_status_label = Label(text="",font=("Verdana", 20,"bold"),width=30)
progress_bar = ttk.Progressbar(window, variable=progress_var, maximum=100,length=580)

next_step_button = Button(text="Next Step", command=handle_next_step, font=("Verdana", 20,"bold"),width=30,bg="grey")
next_step_button.place(x=120, y=145)

start_download_button = Button(text="Start Download", command=start_download,font=("Verdana", 20,"bold"),width=30,bg="grey")
select_directory_button = Button(text="Select the directory", state="disabled", command=select_directory,font=("Verdana", 20,"bold"),width=30,bg="grey")
icon_directory = PhotoImage(file='magnifying.png')
image_directory = Label(window,image=icon_directory)

window.geometry("800x900")
window.resizable(False, False)
window.mainloop()
