import folium

def generate_map(gpx, map_path):
    first_point = gpx.tracks[0].segments[0].points[0]
    map_ = folium.Map(location=[first_point.latitude, first_point.longitude], zoom_start=15)
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                folium.Marker([point.latitude, point.longitude]).add_to(map_)
    map_.save(map_path)

def generate_interactive_map(gpx, map_path):
    first_point = gpx.tracks[0].segments[0].points[0]
    map_ = folium.Map(location=[first_point.latitude, first_point.longitude], zoom_start=15)
    points = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append((point.latitude, point.longitude))
    folium.PolyLine(points).add_to(map_)
    folium.Marker(points[0], draggable=True, popup="Start").add_to(map_)
    folium.Marker(points[-1], draggable=True, popup="End").add_to(map_)
    map_.save(map_path)