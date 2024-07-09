from flask import Flask, request, render_template, send_file
import moviepy.editor as mp
from .gpx_parser import parse_gpx, trim_gpx
from .map_generator import generate_interactive_map
import os
from datetime import timedelta

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_video', methods=['POST'])
def upload_video():
    video = request.files['video']
    video_path = os.path.join('uploads', video.filename)
    video.save(video_path)
    video_clip = mp.VideoFileClip(video_path)
    duration = video_clip.duration
    # Set the default directory for file dialogs
    default_directory = os.getcwd()
    return {'video_path': video_path, 'duration': duration, 'default_directory': default_directory}

@app.route('/upload_gpx', methods=['POST'])
def upload_gpx():
    gpx_file = request.files['gpx']
    gpx_path = os.path.join('uploads', gpx_file.filename)
    gpx_file.save(gpx_path)
    gpx = parse_gpx(gpx_path)
    generate_interactive_map(gpx, 'static/temp_map.html')
    start_time = gpx.tracks[0].segments[0].points[0].time
    end_time = gpx.tracks[0].segments[0].points[-1].time
    # Set the default directory for file dialogs
    default_directory = os.getcwd()
    return {'gpx_path': gpx_path, 'start_time': str(start_time), 'end_time': str(end_time), 'default_directory': default_directory}

@app.route('/update_gpx', methods=['POST'])
def update_gpx():
    gpx_path = request.form['gpx_path']
    start_offset = float(request.form['start_offset'])
    end_offset = float(request.form['end_offset'])
    gpx = parse_gpx(gpx_path)
    gpx_start_time = gpx.tracks[0].segments[0].points[0].time
    new_start_time = gpx_start_time + timedelta(seconds=start_offset)
    new_end_time = gpx_start_time + timedelta(seconds=end_offset)
    trimmed_gpx = trim_gpx(gpx, new_start_time, new_end_time)
    generate_interactive_map(trimmed_gpx, 'static/temp_map.html')
    return {'message': 'GPX updated successfully'}

@app.route('/generate_video', methods=['POST'])
def generate_video():
    video_path = request.form['video_path']
    gpx_path = request.form['gpx_path']
    start_time = float(request.form['start_time'])
    end_time = float(request.form['end_time'])
    output_path = 'output_video.mp4'
    # Implement the video generation logic here
    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)