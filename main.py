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
    try:
        if path.startswith('http://') or path.startswith('https://'):
            response = requests.get(path)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            return Image.open(BytesIO(response.content))
        else:
            # Check if the file exists and is accessible
            if not os.path.exists(path):
                raise FileNotFoundError(f"File not found: {path}")
            if not os.access(path, os.R_OK):
                raise PermissionError(f"Permission denied: {path}")
            return Image.open(path)
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error downloading image from URL: {e}")
    except FileNotFoundError as fnfe:
        raise Exception(f"File not found: {fnfe}")
    except PermissionError as pe:
        raise Exception(f"Permission denied: {pe}")
    except Exception as e:
        raise Exception(f"Error loading image: {e}")

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
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to handle the download of the image with the background removed
def on_download():
    input_path = local_entry.get() or url_entry.get()
    base_name = os.path.basename(input_path)
    name, ext = os.path.splitext(base_name)
    output_name = f"{name}_nobg.png"

    # Ask the user to select a save directory
    save_directory = filedialog.askdirectory()
    if not save_directory:
        messagebox.showerror("Error", "Please select a directory to save the file")
        return

    output_path = os.path.join(save_directory, output_name)

    try:
        input_image = load_image_from_path(input_path)
        output_image = remove_background(input_image)
        output_image.save(output_path)
        messagebox.showinfo("Success", f"Image with removed background saved to {output_path}")

        # Clear the search bars after successful download
        local_entry.delete(0, tk.END)
        url_entry.delete(0, tk.END)
    except PermissionError as pe:
        messagebox.showerror("Permission Error", f"Permission denied: {pe}")
    except FileNotFoundError as fnfe:
        messagebox.showerror("File Not Found Error", f"File not found: {fnfe}")
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
root.geometry("800x600")

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