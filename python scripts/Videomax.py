from tkinter import *
from tkinter import ttk
from pytube import YouTube
from tkinter.messagebox import showinfo, showerror, askokcancel
from threading import Thread
from os import rename
from os.path import splitext

picture = 'icons'
icon1 = picture  + "\iconss.ico"
icon2 = picture + "\icon.png"
# the function for closing the application
def close_window():
    # if askokcancel is True, close the window
    if askokcancel(title='Close Application', message='Do you want to close Videomax downloader?'):
        # this distroys the window
        window.destroy()
        
def download_video():
    # the try statement to excute the download the video code
    # getting video url from entry
    mp4_link = url_entry.get()
    # checking if the entry and combobox is empty
    if mp4_link == '':
        # display error message when url entry is empty
        showerror(title='Error', message='Please enter the Valid MP4 URL')
    # else let's download the audio file  
    else:
        # this try statement will run if the mp3 url is filled
        try:
            # this function will track the audio file download progress
            def on_progress(stream, chunk, bytes_remaining):
                # the total size of the audio
                total_size = stream.filesize
                # this function will get the size of the audio file
                def get_formatted_size(total_size, factor=1024, suffix='B'):
                    # looping through the units
                    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
                        if total_size < factor:
                            return f"{total_size:.2f}{unit}{suffix}"
                        total_size /= factor
                    # returning the formatted audio file size
                    return f"{total_size:.2f}Y{suffix}"
                    
                # getting the formatted audio file size calling the function
                formatted_size = get_formatted_size(total_size)
                # the size downloaded after the start
                bytes_downloaded = total_size - bytes_remaining
                # the percentage downloaded after the start
                percentage_completed = round(bytes_downloaded / total_size * 100)
                # updating the progress bar value
                progress_bar['value'] = percentage_completed
                # updating the empty label with the percentage value
                progress_label.config(text=str(percentage_completed) + '%, File size:' + formatted_size)
                # updating the main window of the app
                window.update()
                
            # creating the YouTube object and passing the the on_progress function
            video = YouTube(mp4_link, on_progress_callback=on_progress)     
            # extracting and downloading the audio file 
            output = video.streams.get_highest_resolution().download()
		    # this renames the mp3 file
            rename(output, video.title)
            # popup for dispalying the mp3 downlaoded success message
            showinfo(title='Download Complete', message=f'{video.title} video has been downloaded successfully.')
            # ressetting the progress bar and the progress label
            progress_label.config(text='')
            progress_bar['value'] = 0           
        # the except will run when an expected error occurs during downloading
        except:
            showerror(title='Download Error', message='An error occurred while trying to ' \
                    'download the video\nThe following could ' \
                    'be the causes:\n->Invalid link\n->No internet connection\n'\
                     'Make sure you have stable internet connection and the video link is valid')
                # ressetting the progress bar and the progress label
            progress_label.config(text='')
            progress_bar['value'] = 0
# the function to run the download_audio function as a thread   
def downloadThread():
    t1 = Thread(target=download_video)
    t1.start()   
        

# creates the window using Tk() fucntion
window = Tk()

# this will listen to the close window event
window.protocol('WM_DELETE_WINDOW', close_window)

# creates title for the window
window.title('Video Downloader powered by Vanguard')

# the icon for the application, this will replace the default tkinter icon
window.iconbitmap(window, icon1)

# dimensions and position of the window
window.geometry('500x400+430+180')
# makes the window non-resizable
window.resizable(height=FALSE, width=FALSE)

# creates the canvas for containing all the widgets
canvas = Canvas(window, width=500, height=400)
canvas.pack()

"""Styles for the widgets"""
# style for the label 
label_style = ttk.Style()
label_style.configure('TLabel', foreground='#000000', font=('OCR A Extended', 15))

# style for the entry
entry_style = ttk.Style()
entry_style.configure('TEntry', font=('Dotum', 15))

# style for the button
button_style = ttk.Style()
button_style.configure('TButton', foreground='#000000', font='DotumChe')

# loading the MP3 logo
logo = PhotoImage(file=icon2)
# creates dimensions for the logo
logo = logo.subsample(2, 2)
# adding the logo to the canvas
canvas.create_image(180, 80, image=logo)

# the Downloader label just next to the logo
mp3_label = ttk.Label(window, text='Downloader', style='TLabel')
canvas.create_window(340, 125, window=mp3_label)


# creating a ttk label
url_label = ttk.Label(window, text='Enter Video URL:', style='TLabel')



# creating a ttk entry
url_entry = ttk.Entry(window, width=72, style='TEntry')

menu =  Menu(window, tearoff =0)
menu.add_command(label="Cut",\
              accelerator="Ctrl+X", \
              command = lambda:url_entry.event_generate("<<Cut>>")
              )
menu.add_command(label="Copy", \
              accelerator="Ctrl+C", \
              command = lambda:url_entry.event_generate("<<Copy>>")
              )
menu.add_command(label="Paste",\
             accelerator="Ctrl+V", \
              command= lambda:url_entry.event_generate("<<Paste>>"))
menu.add_separator()
menu.add_command(label ="Rename")
def do_popup(event):
   try:
        menu.tk_popup(event.x_root, event.y_root)
   finally:
       menu.grab_release()
window.bind("<Button-3>", do_popup)
# adding the label to the canvas
canvas.create_window(114, 200, window=url_label)
# adding the entry to the canvas
canvas.create_window(250, 230, window=url_entry)

# creating the empty label for displaying download progress
progress_label = Label(window, text='')
# adding the label to the canvas
canvas.create_window(240, 280, window=progress_label)

# creating a progress bar to display progress
progress_bar = ttk.Progressbar(window, orient=HORIZONTAL, length=450, mode='determinate')
# adding the progress bar to the canvas
canvas.create_window(250, 300, window=progress_bar)

# creating the button
download_button = ttk.Button(window, text='Download Video', style='TButton', command=downloadThread)
# adding the button to the canvas
canvas.create_window(240, 330, window=download_button)



# this runs the app infinitely
window.mainloop()

