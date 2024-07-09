import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import moviepy.editor as mp
from .gpx_parser import parse_gpx, trim_gpx
from .map_generator import generate_interactive_map
import webbrowser
from datetime import timedelta

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("GPX Video Overlay")
        self.video_path = None
        self.gpx_path = None
        self.create_widgets()

    def create_widgets(self):
        tk.Button(self.root, text="Select Video", command=self.select_video).pack()
        tk.Button(self.root, text="Select GPX", command=self.select_gpx).pack()
        self.start_time = tk.Entry(self.root)
        self.start_time.pack()
        self.end_time = tk.Entry(self.root)
        self.end_time.pack()
        tk.Button(self.root, text="Generate Video", command=self.generate_video).pack()

    def select_video(self):
        self.video_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.MP4")])
        if self.video_path:
            self.preview_video()

    def preview_video(self):
        if self.video_path:
            video = mp.VideoFileClip(self.video_path)
            self.show_video_preview(video)
            self.set_start_end_time(video.duration)

    def show_video_preview(self, video):
        preview_window = tk.Toplevel(self.root)
        preview_window.title("Video Preview")
        video_label = tk.Label(preview_window, text="Video Preview")
        video_label.pack()
        video.preview()
        self.create_time_selector(preview_window, video.duration)

    def create_time_selector(self, window, duration):
        tk.Label(window, text="Start Time:").pack()
        self.start_time_scale = tk.Scale(window, from_=0, to=duration, orient=tk.HORIZONTAL)
        self.start_time_scale.pack()
        tk.Label(window, text="End Time:").pack()
        self.end_time_scale = tk.Scale(window, from_=0, to=duration, orient=tk.HORIZONTAL)
        self.end_time_scale.pack()

    def set_start_end_time(self, duration):
        self.start_time.delete(0, tk.END)
        self.start_time.insert(0, "0")
        self.end_time.delete(0, tk.END)
        self.end_time.insert(0, str(duration))

    def select_gpx(self):
        self.gpx_path = filedialog.askopenfilename(filetypes=[("GPX files", "*.gpx")])
        if self.gpx_path:
            self.preview_gpx()

    def preview_gpx(self):
        if self.gpx_path:
            gpx = parse_gpx(self.gpx_path)
            generate_interactive_map(gpx, "temp_map.html")
            webbrowser.open("temp_map.html")
            self.set_start_end_time_gpx(gpx)
            self.create_gpx_time_selector(gpx)

    def set_start_end_time_gpx(self, gpx):
        start_time = gpx.tracks[0].segments[0].points[0].time
        end_time = gpx.tracks[0].segments[0].points[-1].time
        self.start_time.delete(0, tk.END)
        self.start_time.insert(0, str(start_time))
        self.end_time.delete(0, tk.END)
        self.end_time.insert(0, str(end_time))

    def create_gpx_time_selector(self, gpx):
        start_time = gpx.tracks[0].segments[0].points[0].time
        end_time = gpx.tracks[0].segments[0].points[-1].time
        duration = (end_time - start_time).total_seconds()

        gpx_window = tk.Toplevel(self.root)
        gpx_window.title("GPX Time Selector")

        tk.Label(gpx_window, text="Start Time:").pack()
        self.gpx_start_time_scale = tk.Scale(gpx_window, from_=0, to=duration, orient=tk.HORIZONTAL)
        self.gpx_start_time_scale.pack()

        tk.Label(gpx_window, text="End Time:").pack()
        self.gpx_end_time_scale = tk.Scale(gpx_window, from_=0, to=duration, orient=tk.HORIZONTAL)
        self.gpx_end_time_scale.set(duration)
        self.gpx_end_time_scale.pack()

        tk.Button(gpx_window, text="Update GPX", command=lambda: self.update_gpx(gpx)).pack()

    def update_gpx(self, gpx):
        start_offset = self.gpx_start_time_scale.get()
        end_offset = self.gpx_end_time_scale.get()

        gpx_start_time = gpx.tracks[0].segments[0].points[0].time
        new_start_time = gpx_start_time + timedelta(seconds=start_offset)
        new_end_time = gpx_start_time + timedelta(seconds=end_offset)

        trimmed_gpx = trim_gpx(gpx, new_start_time, new_end_time)
        generate_interactive_map(trimmed_gpx, "temp_map.html")
        webbrowser.open("temp_map.html")

    def generate_video(self):
        # Implementation for generating video
        print("Video generated successfully.")

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()