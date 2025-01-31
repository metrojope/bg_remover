from rembg import remove
from PIL import Image, ImageTk
import os
import requests
from io import BytesIO
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# Function to remove the background from an image
def remove_background(input_image):
    return remove(input_image)

# Function to load an image from a local path or URL
def load_image_from_path(path):
    if path.startswith('http://') or path.startswith('https://'):
        response = requests.get(path)
        return Image.open(BytesIO(response.content))
    else:
        return Image.open(path)

# Function to handle the background removal and preview
def on_remove_background(event=None):
    input_path = local_entry.get() or url_entry.get()
    if not input_path:
        messagebox.showerror("Error", "Please enter a valid image path or URL")
        return

    try:
        input_image = load_image_from_path(input_path)
        input_image.thumbnail((300, 300))
        input_photo = ImageTk.PhotoImage(input_image)
        original_label.config(image=input_photo)
        original_label.image = input_photo

        output_image = remove_background(input_image)
        output_image.thumbnail((300, 300))
        output_photo = ImageTk.PhotoImage(output_image)
        output_label.config(image=output_photo)
        output_label.image = output_photo

        download_button.config(state=tk.NORMAL)

        # Clear the search bars
        local_entry.delete(0, tk.END)
        url_entry.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to handle the download of the image with the background removed
def on_download():
    input_path = local_entry.get() or url_entry.get()
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    base_name = os.path.basename(input_path)
    name, ext = os.path.splitext(base_name)
    output_name = f"{name}_nobg.png"
    output_path = os.path.join(desktop_path, output_name)

    try:
        input_image = load_image_from_path(input_path)
        output_image = remove_background(input_image)
        output_image.save(output_path)
        messagebox.showinfo("Success", f"Image with removed background saved to {output_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to handle browsing for a local image file
def on_browse():
    file_path = filedialog.askopenfilename()
    local_entry.delete(0, tk.END)
    local_entry.insert(0, file_path)

# Create the main application window
root = tk.Tk()
root.title("Background Remover")

# Set a fixed size for the window
root.geometry("800x700")

# Create a frame for the input fields and buttons
frame = tk.Frame(root)
frame.pack(pady=20)

# Entry for local image path
local_label = tk.Label(frame, text="Local Image Path:")
local_label.pack(pady=5)
local_entry = tk.Entry(frame, width=50)
local_entry.pack(pady=5)
local_entry.bind("<Return>", on_remove_background)

# Button to browse for a local image file
browse_button = tk.Button(frame, text="Browse", command=on_browse)
browse_button.pack(pady=5)

# Entry for image URL
url_label = tk.Label(frame, text="Image URL:")
url_label.pack(pady=5)
url_entry = tk.Entry(frame, width=50)
url_entry.pack(pady=5)
url_entry.bind("<Return>", on_remove_background)

# Button to preview the background removal
remove_button = tk.Button(root, text="Preview Background Removal", command=on_remove_background)
remove_button.pack(pady=10)

# Frame to hold the image previews
image_frame = tk.Frame(root)
image_frame.pack(pady=10)

# Label to display the original image
original_label = tk.Label(image_frame, text="Original Image", width=300, height=300)
original_label.pack(side=tk.LEFT, padx=10)

# Label to display the image without background
output_label = tk.Label(image_frame, text="Image without Background", width=300, height=300)
output_label.pack(side=tk.LEFT, padx=10)

# Button to download the image with the background removed
download_button = tk.Button(root, text="Download Image", command=on_download, state=tk.DISABLED)
download_button.pack(pady=10)

# Start the main event loop
root.mainloop()