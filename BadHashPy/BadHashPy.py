import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import hashlib
import pyperclip

# Create the main application window
root = TkinterDnD.Tk()
root.title("File Hash Generator")
root.resizable(False, False)  # Disable resizing horizontally
root.attributes('-toolwindow', True)  # Remove maximize button

# Function to compute file hashes
def compute_hashes(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return {
            "MD5": hashlib.md5(data).hexdigest(),
            "SHA-1": hashlib.sha1(data).hexdigest(),
            "SHA-256": hashlib.sha256(data).hexdigest(),
        }
    except Exception:
        return {"MD5": "Error", "SHA-1": "Error", "SHA-256": "Error"}

# Function to handle file drop event
def on_drop(event):
    file_path = event.data.strip()
    entry_file.delete(0, tk.END)
    entry_file.insert(0, file_path)

    # Compute hashes and display them
    hashes = compute_hashes(file_path)
    entry_md5.delete(0, tk.END)
    entry_md5.insert(0, hashes["MD5"])
    entry_sha1.delete(0, tk.END)
    entry_sha1.insert(0, hashes["SHA-1"])
    entry_sha256.delete(0, tk.END)
    entry_sha256.insert(0, hashes["SHA-256"])

    # Update window height dynamically
    root.update_idletasks()
    root.geometry(f"600x{root.winfo_reqheight()}")

# Function to copy text to clipboard
def copy_to_clipboard(entry):
    pyperclip.copy(entry.get())

# Title label (centered)
title_label = tk.Label(root, text="Drag and drop a file to generate hashes:", font=("Arial", 12, "bold"))
title_label.pack(pady=5)

# Helper function to create labeled entry fields with equal widths
def create_labeled_entry(root, label_text):
    frame = tk.Frame(root)
    lbl = tk.Label(frame, text=label_text, font=("Arial", 10), anchor="e", width=10)
    entry = tk.Entry(frame, width=50)  # Ensure consistent width
    lbl.pack(side=tk.LEFT, padx=5)
    entry.pack(side=tk.RIGHT, fill="x", expand=True)
    frame.pack(pady=2, fill="x")
    return entry

# Drag-and-drop file box
entry_file = create_labeled_entry(root, "Filename:")
entry_file.drop_target_register(DND_FILES)
entry_file.dnd_bind('<<Drop>>', on_drop)

# Helper function to create labeled entry fields with copy buttons
def create_labeled_entry_with_button(root, label_text):
    frame = tk.Frame(root)
    lbl = tk.Label(frame, text=label_text, font=("Arial", 10), anchor="e", width=10)
    entry = tk.Entry(frame, width=50)  # Ensure consistent width
    btn = tk.Button(frame, text="Copy", command=lambda: copy_to_clipboard(entry))
    lbl.pack(side=tk.LEFT, padx=5)
    entry.pack(side=tk.LEFT, padx=5, fill="x", expand=True)
    btn.pack(side=tk.RIGHT)
    frame.pack(pady=2, fill="x")
    return entry

# Hash boxes with copy buttons
entry_md5 = create_labeled_entry_with_button(root, "MD5:")
entry_sha1 = create_labeled_entry_with_button(root, "SHA-1:")
entry_sha256 = create_labeled_entry_with_button(root, "SHA-256:")

# Auto-adjust window height initially
root.update_idletasks()
root.geometry(f"600x{root.winfo_reqheight()}")

# Start the Tkinter main loop
root.mainloop()