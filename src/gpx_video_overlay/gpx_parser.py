import gpxpy
from datetime import timedelta

def parse_gpx(file_path):
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
    return gpx

def trim_gpx(gpx, start_time, end_time):
    trimmed_gpx = gpxpy.gpx.GPX()
    for track in gpx.tracks:
        new_track = gpxpy.gpx.GPXTrack()
        for segment in track.segments:
            new_segment = gpxpy.gpx.GPXTrackSegment()
            for point in segment.points:
                if start_time <= point.time <= end_time:
                    new_segment.points.append(point)
            if new_segment.points:
                new_track.segments.append(new_segment)
        if new_track.segments:
            trimmed_gpx.tracks.append(new_track)
    return trimmed_gpx