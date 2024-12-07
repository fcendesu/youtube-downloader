import tkinter as tk
from tkinter import messagebox
import yt_dlp
import os

def download_videos():
    # Get the user input for YouTube links and resolution
    links = text_area.get("1.0", "end-1c").strip().split("\n")
    resolution = resolution_var.get()

    if not links:
        messagebox.showerror("Error", "Please enter at least one YouTube link.")
        return

    if not resolution:
        messagebox.showerror("Error", "Please select a resolution.")
        return

    # Set the download options to save in the current folder
    current_directory = os.getcwd()  # Get the current working directory
    ydl_opts = {
        'outtmpl': os.path.join(current_directory, '%(title)s.%(ext)s'),  # Save to the current folder
        'progress_hooks': [progress_hook],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for link in links:
            try:
                # Extract video information (without downloading)
                info_dict = ydl.extract_info(link, download=False)
                formats = info_dict.get('formats', [])
                
                # List available formats (resolution + quality)
                available_formats = []
                for f in formats:
                    format_note = f.get('format_note', '')
                    resolution = f.get('height', '')
                    quality = f.get('tbr', 'N/A')  # bitrate
                    if resolution and format_note:
                        available_formats.append((resolution, quality, f['format_id']))
                
                # Filter based on selected resolution (if available)
                filtered_formats = [f for f in available_formats if f[0] == resolution]
                
                if not filtered_formats:
                    messagebox.showerror("Error", f"Resolution {resolution} not available for {link}.")
                    continue
                
                # Choose the best quality format (highest bitrate if available)
                best_format = sorted(filtered_formats, key=lambda x: int(x[1]) if x[1] != 'N/A' else 0, reverse=True)[0]
                best_format_id = best_format[2]
                
                # Download the best format available
                ydl_opts['format'] = best_format_id
                ydl.download([link])

            except Exception as e:
                messagebox.showerror("Download Error", f"Failed to download {link}: {str(e)}")

def progress_hook(d):
    if d['status'] == 'downloading':
        progress_var.set(f"Downloading: {d['filename']} {d['downloaded_bytes']} bytes")
    elif d['status'] == 'finished':
        progress_var.set(f"Finished: {d['filename']}")

# Create the main window
root = tk.Tk()
root.title("YouTube Downloader")

# Create the GUI components
text_area = tk.Text(root, height=10, width=50)
text_area.pack(pady=10)

resolution_var = tk.StringVar()
resolution_menu = tk.OptionMenu(root, resolution_var, '360p', '480p', '720p', '1080p')
resolution_menu.pack(pady=10)

download_button = tk.Button(root, text="Download", command=download_videos)
download_button.pack(pady=10)

progress_var = tk.StringVar()
progress_label = tk.Label(root, textvariable=progress_var)
progress_label.pack(pady=10)

# Run the application
root.mainloop()
