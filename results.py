# import os

# p = os.path.abspath(__file__).replace('results.py','')

# voting_results_file = p + 'voting_results.txt'

# def show_results():
#     try:
#         with open(voting_results_file, 'r') as file:
#             print("Voting Results:")
#             for line in file:
#                 print(line.strip())
#     except FileNotFoundError:   
#         print("No voting results found.")

# if __name__ == '__main__':
#     show_results()

import os
import tkinter as tk
from tkinter import messagebox

# Get the path of the current file and the results file
p = os.path.abspath(__file__).replace('results.py','')
voting_results_file = p + 'voting_results.txt'

def show_results():
    results_text = ""
    try:
        with open(voting_results_file, 'r') as file:
            for line in file:
                results_text += line.strip() + '\n'
    except FileNotFoundError:
        results_text = "No voting results found."

    return results_text

def display_results():
    results_text = show_results()
    results_label.config(text=results_text)

# Set up the main Tkinter window
root = tk.Tk()
root.title("Voting Results")
root.geometry("400x300")
root.configure(bg="#333333")

# Header frame
header_frame = tk.Frame(root, bg="#111111", pady=20)
header_frame.pack(fill="x")
header_label = tk.Label(header_frame, text="Voting Results", font=("Stencil Std", 24), fg="white", bg="#111111")
header_label.pack()

# Results frame
results_frame = tk.Frame(root, bg="#333333", padx=20, pady=20)
results_frame.pack(fill="both", expand=True)
results_label = tk.Label(results_frame, text="", font=("Helvetica", 16), fg="white", bg="#333333", justify="left")
results_label.pack()

# Load the results on startup
display_results()

root.mainloop()
