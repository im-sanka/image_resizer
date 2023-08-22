import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import io
import zipfile
import os  # For extracting the filename

def resize_images():
    max_option = size_var.get()
    maxsize = (max_option, max_option)
    output_folder = format_var.get()

    files = filedialog.askopenfilenames()

    if not files:
        return

    output_files = []

    for file in files:
        with Image.open(file) as im:
            im.thumbnail(maxsize)
            output_buffer = io.BytesIO()

            if output_folder == "JPEG" and im.mode == "RGBA":
                im = im.convert("RGB")

            im.save(output_buffer, format=output_folder)
            output_files.append((output_buffer, os.path.basename(file)))  # Using basename

    if len(output_files) == 1:
        output_filename = filedialog.asksaveasfilename(defaultextension=f".{output_folder.lower()}")
        with open(output_filename, 'wb') as f:
            f.write(output_files[0][0].getvalue())
    else:
        output_filename = filedialog.asksaveasfilename(defaultextension=".zip")
        with zipfile.ZipFile(output_filename, 'w') as zf:
            for i, (output_buffer, name) in enumerate(output_files):
                zf.writestr(f"{name.rsplit('.', 1)[0]}_resized.{output_folder.lower()}", output_buffer.getvalue())  # Modify the name logic slightly

    messagebox.showinfo("Info", "Images resized successfully!")

app = tk.Tk()
app.title("Image Resizer")

# The frame will help in centering the content
frame = tk.Frame(app)
frame.pack(pady=50, padx=50)  # This will help center the content

size_var = tk.IntVar(app)
size_var.set(128)

tk.Label(frame, text="First, choose the size you are aiming for:").pack(pady=10, anchor=tk.CENTER)
tk.Radiobutton(frame, text="128x128", variable=size_var, value=128).pack(anchor=tk.W)
tk.Radiobutton(frame, text="256x256", variable=size_var, value=256).pack(anchor=tk.W)
tk.Radiobutton(frame, text="512x512", variable=size_var, value=512).pack(anchor=tk.W)
tk.Radiobutton(frame, text="1024x1024", variable=size_var, value=1024).pack(anchor=tk.W)
tk.Radiobutton(frame, text="2048x2048", variable=size_var, value=2048).pack(anchor=tk.W)

format_var = tk.StringVar(app)
format_var.set("JPEG")

tk.Label(frame, text="Second, select the output format:").pack(pady=10, anchor=tk.CENTER)
tk.Radiobutton(frame, text="JPEG", variable=format_var, value="JPEG").pack(anchor=tk.W)
tk.Radiobutton(frame, text="PNG", variable=format_var, value="PNG").pack(anchor=tk.W)

tk.Button(frame, text="Select images here!", command=resize_images).pack(pady=40)

app.mainloop()
