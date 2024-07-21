import folium
import plotly.graph_objs as go
import plotly.io as pio

def generate_interactive_map(gpx, map_path, elevation_path, speed_path):
    first_point = gpx.tracks[0].segments[0].points[0]
    map_ = folium.Map(location=[first_point.latitude, first_point.longitude], zoom_start=15)
    points = []
    elevations = []
    speeds = []
    times = []

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append((point.latitude, point.longitude))
                elevations.append(point.elevation)
                speeds.append(point.speed)
                times.append(point.time)

    folium.PolyLine(points).add_to(map_)
    folium.Marker(points[0], draggable=True, popup="Start").add_to(map_)
    folium.Marker(points[-1], draggable=True, popup="End").add_to(map_)
    map_.save(map_path)

    # Generate elevation chart
    elevation_fig = go.Figure(data=[go.Scatter(x=times, y=elevations, mode='lines', name='Elevation')])
    pio.write_html(elevation_fig, file=elevation_path, auto_open=False)

    # Generate speed chart
    speed_fig = go.Figure(data=[go.Scatter(x=times, y=speeds, mode='lines', name='Speed')])
    pio.write_html(speed_fig, file=speed_path, auto_open=False)