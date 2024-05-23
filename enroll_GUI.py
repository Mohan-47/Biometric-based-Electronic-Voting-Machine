import tkinter as tk
from tkinter import messagebox, PhotoImage
import time
from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER2


## Enrolls new finger
##

## Tries to initialize the sensor
try:
    f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')
    ## Gets some sensor information
    print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))   
except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)


def enroll_voter() :
## Tries to enroll new finger
 try:
    print('Waiting for finger...')
    messagebox.showinfo("Enrolling","Place the finger on sensor for enrollment!")

    ## Wait that finger is read
    while ( f.readImage() == False ):
        pass

    ## Converts read image to characteristics and stores it in charbuffer 1
    f.convertImage(FINGERPRINT_CHARBUFFER1)

    ## Checks if finger is already enrolled
    result = f.searchTemplate()
    positionNumber = result[0]

    if ( positionNumber >= 0 ):
        print('Template already exists at position #' + str(positionNumber))
        messagebox.showinfo("Existing",'Template already exists at position #' + str(positionNumber))
        exit(0)

    print('Remove finger...')
    messagebox.showinfo("remove",'Please remove your finger')
    time.sleep(2)

    print('Waiting for same finger again...')
    messagebox.showinfo("place",'Please place the same finger again')

    ## Wait that finger is read again
    while ( f.readImage() == False ):
        pass

    ## Converts read image to characteristics and stores it in charbuffer 2
    f.convertImage(FINGERPRINT_CHARBUFFER2)

    ## Compares the charbuffers
    if ( f.compareCharacteristics() == 0 ):
        raise Exception('Fingers do not match')
        messagebox.showinfo("error",'Fingers do not match')
    ## Creates a template
    f.createTemplate()

    ## Saves template at new position number
    positionNumber = f.storeTemplate()
    print('Finger enrolled successfully!')
    print('New template position #' + str(positionNumber))
    messagebox.showinfo("success",'Enrollment successful')
 except Exception as e:
    print('Operation failed!')
    messagebox.showinfo("failure",'Enrollment failed')
    print('Exception message: ' + str(e))
    exit(1)
    
    
root = tk.Tk()
root.title("Enrollment")
root.geometry("400x300")
root.configure(bg="white")
root.resizable(False,False)

header_frame = tk.Frame(root, bg="#111111", pady=20)
header_frame.pack(fill="x")
header_label = tk.Label(header_frame, text="Enrolling a finger", font=("Stencil Std", 24), fg="white", bg="#111111")
header_label.pack()

enroll_button = tk.Button(root, text="Enroll Voter", font=("Helvetica", 16), command=enroll_voter, bg="#4CAF50", fg="white", pady=10, padx=20)
enroll_button.pack(pady=20)

root.mainloop()