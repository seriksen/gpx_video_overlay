import tkinter as tk
from tkinter import filedialog
import moviepy.editor as mp
from .gpx_parser import parse_gpx, trim_gpx
from .map_generator import generate_map, generate_interactive_map
from .video_processor import overlay_map_on_video
from datetime import timedelta
import webbrowser

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("GPX Map Overlay")
        self.video_path = ""
        self.gpx_path = ""
        self.map_path = "map.html"
        self.output_path = "output_video.mp4"
        self.pos = ("right", "bottom")
        self.size = (200, 200)
        self.create_widgets()

    def create_widgets(self):
        tk.Button(self.root, text="Select Video", command=self.select_video).pack()
        tk.Button(self.root, text="Select GPX File", command=self.select_gpx).pack()
        tk.Button(self.root, text="Edit GPX", command=self.edit_gpx).pack()
        tk.Button(self.root, text="Generate Map", command=self.generate_map_only).pack()
        tk.Label(self.root, text="Map Position (x, y):").pack()
        self.pos_x = tk.Entry(self.root)
        self.pos_x.pack()
        self.pos_y = tk.Entry(self.root)
        self.pos_y.pack()
        tk.Label(self.root, text="Map Size (width, height):").pack()
        self.size_width = tk.Entry(self.root)
        self.size_width.pack()
        self.size_height = tk.Entry(self.root)
        self.size_height.pack()
        tk.Label(self.root, text="Video Start Time (seconds):").pack()
        self.start_time = tk.Entry(self.root)
        self.start_time.pack()
        self.end_time_label = tk.Label(self.root, text="Video End Time (seconds):")
        self.end_time_label.pack()
        self.end_time = tk.Entry(self.root)
        self.end_time.pack()
        tk.Button(self.root, text="Set End Time", command=self.set_end_time).pack()
        tk.Button(self.root, text="Generate Video", command=self.generate_video).pack()

    def select_video(self):
        self.video_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
        if self.video_path:
            self.preview_video()

    def select_gpx(self):
        self.gpx_path = filedialog.askopenfilename(filetypes=[("GPX files", "*.gpx")])

    def preview_video(self):
        if self.video_path:
            video = mp.VideoFileClip(self.video_path)
            video.preview()

    def set_end_time(self):
        if self.video_path:
            video = mp.VideoFileClip(self.video_path)
            self.end_time.delete(0, tk.END)
            self.end_time.insert(0, str(video.duration))

    def edit_gpx(self):
        if not self.gpx_path:
            print("Please select a GPX file.")
            return
        gpx = parse_gpx(self.gpx_path)
        generate_interactive_map(gpx, self.map_path)
        webbrowser.open(self.map_path)

    def generate_map_only(self):
        if not self.gpx_path:
            print("Please select a GPX file.")
            return
        gpx = parse_gpx(self.gpx_path)
        start_time = float(self.start_time.get())
        end_time = float(self.end_time.get())
        gpx_start_time = gpx.tracks[0].segments[0].points[0].time
        gpx_end_time = gpx_start_time + timedelta(seconds=(end_time - start_time))
        trimmed_gpx = trim_gpx(gpx, gpx_start_time, gpx_end_time)
        generate_map(trimmed_gpx, self.map_path)
        print("Map generated successfully. Check the file:", self.map_path)

    def generate_video(self):
        if not self.video_path or not self.gpx_path:
            print("Please select both video and GPX files.")
            return
        gpx = parse_gpx(self.gpx_path)
        start_time = float(self.start_time.get())
        end_time = float(self.end_time.get())
        gpx_start_time = gpx.tracks[0].segments[0].points[0].time
        gpx_end_time = gpx_start_time + timedelta(seconds=(end_time - start_time))
        trimmed_gpx = trim_gpx(gpx, gpx_start_time, gpx_end_time)
        generate_map(trimmed_gpx, self.map_path)
        pos = (int(self.pos_x.get()), int(self.pos_y.get()))
        size = (int(self.size_width.get()), int(self.size_height.get()))
        overlay_map_on_video(self.video_path, self.map_path, self.output_path, pos, size, start_time, end_time)
        print("Video generated successfully.")

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()