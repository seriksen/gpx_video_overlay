import moviepy.editor as mp

def overlay_map_on_video(video_path, map_path, output_path, pos, size, start_time, end_time):
    video = mp.VideoFileClip(video_path).subclip(start_time, end_time)
    map_clip = mp.ImageClip(map_path).set_duration(video.duration).resize(size).set_pos(pos)
    final_video = mp.CompositeVideoClip([video, map_clip])
    final_video.write_videofile(output_path, codec='libx264', fps=24, bitrate="5000k")