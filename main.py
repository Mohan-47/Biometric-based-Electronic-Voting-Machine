'''
Biometric EVM 

Hardware Used -
1. Raspberry Pi 4 Model B -
2. R307 Fingerprint Sensor -
3. 3.3V 2A Power + Type-C 
4. USB - TTL Converter (CP2102, CH9102, etc)(Optional)

Libraries Required :
pillow==10.3.0
pyfingerprint==1.5
pyserial==3.5

(Mentioned in requirements.txt)

'''

from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
import os
import time 
import tkinter as tk
from tkinter import messagebox, PhotoImage
import random

curr_Path = os.path.abspath(__file__).replace('main.py','')

result_file = curr_Path + 'voting_results.txt'

num_of_votes = [0]*5

candidates = ["BJP", "INC", "AAP", "DMK", "TMC"]

voted_fingerprints = set()

position = None

accuracy = None

verified = False

# def get_hash(finger):
#     hash = hashlib.sha256(finger).hexdigest()

#Initialize the sensor
try:
    f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)
    #Sensor information
    print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

    if(f.verifyPassword() == False ):
        raise ValueError("The fingerprint sensor password is wrong!")
        
except Exception as e:
    print("The fingerprint sensor could not be initialized.")
    print("Exception message: " + str(e))

def check_voter():
    global position
    global accuracy
    global voted_fingerprints
    global verified

    # Wait for voter to place the finger on sensor.
    try:
        print("Place the finger on sensor for verification!")
        messagebox.showinfo("Verification","Place the finger on sensor for verification!")
        
        while (f.readImage() == False):
            pass

        # Converts the image in image buffer to characteristics and stores it in specified char buffer.

        f.convertImage(FINGERPRINT_CHARBUFFER1)

        # Search the scanned finger in stored templates.
        result = f.searchTemplate()

        # searchTemplate returns two values position and accuracy
        position = result[0]
        accuracy = result[1]

        if( position == -1):
            print("No match found. You are ineligible to vote")
            messagebox.showinfo("Verification Failed", "No match found. You are ineligible to vote")
            verified = False 
            return False
        elif position in voted_fingerprints:
            print("You have already voted.")
            messagebox.showinfo("Already Voted", "You have already voted.")
            verified = False
            return False
        else:
            messagebox.showinfo("Found a match at position "+ str(position) + " with accuracy "+ str(accuracy) + "%")
            
            print("Found a match at position "+ str(position) + " with accuracy "+ str(accuracy) + "%")
            verified = True
            return True
    except Exception as e:
        messagebox.showinfo("Verification Failed", "The fingerprint sensor could not be initialized.")
        print(str(e))
        
#Voting for different parties and storing result in txt db

def vote(candidate_index):

    global position
    global num_of_votes
    global voted_fingerprints
    global verified

    # for i in range(0,5):
    #     print(f'{i+1}.{candidates[i]}')
    
    # x = int(input("Enter your choice:"))
    # if x not in [1,2,3,4,5]:
    #     print("Invalid choice")
    # else:
    #     num_of_votes[x-1] += 1
    #     # Add the fingerprint position to the set of voted fingerprints
    #     voted_fingerprints.add(position)
    #     print('You have voted successfully!')

    if not verified:
        messagebox.showinfo("Not Verified", "Please verify yourself before voting.")
        return

    num_of_votes[candidate_index] += 1
    voted_fingerprints.add(position)

    with open(result_file , 'w') as file:
        for i, candidate in enumerate(candidates):
            file.write(f"{candidate}: {num_of_votes[i]}\n")

    messagebox.showinfo("Vote Submitted", "Your vote has been successfully submitted.")
    print('You have voted successfully!')
    verified = False


def load_logo(candidate):
    logo_path = f"{curr_Path}{candidate}.png"
    if os.path.exists(logo_path):
        logo = PhotoImage(file=logo_path)
        logo = logo.subsample(3, 3)  # Resize the logo
        return logo
    return None

def generate_random_color():
    """Generate a random color in hex format."""
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

#GUI Setup 
root = tk.Tk()
root.title("Biometric EVM")
root.geometry("800x600")
root.configure(bg="#333333")
root.resizable(False,False)

header_frame = tk.Frame(root, bg="#111111", pady=20)
header_frame.pack(fill="x")
header_label = tk.Label(header_frame, text="BIOMETRIC EVM", font=("Stencil Std", 24), fg="white", bg="#111111")
header_label.pack()
    
# Verification button
verify_button = tk.Button(root, text="Verify Voter", font=("Helvetica", 16), command=check_voter, bg="#4CAF50", fg="white", pady=10, padx=20)
verify_button.pack(pady=20)

#Logo and button frame 
logo_button_frame = tk.Frame(root, bg="#333333")
logo_button_frame.pack(pady=20)

for i,candidate in enumerate(candidates):
    logo = load_logo(candidate)
    logo_label = tk.Label(logo_button_frame, image=logo, bg="#f0f0f0")
    logo_label.image = logo
    logo_label.grid(row=0, column=i, padx=10,pady = 10)

    random_color = generate_random_color()
    vote_button = tk.Button(logo_button_frame, text=candidate, font=("Helvetica", 16), command=lambda i=i: vote(i) , width = 10,bg=random_color, fg="white")
    vote_button.grid(row=1, column=i, padx=10, pady = 10)
    

root.mainloop()
    