import googlemaps
import folium

api_key = 'your api key'
gmaps = googlemaps.Client(key=api_key)


def read_landmarks(file_path):
    with open(file_path, 'r') as file:
        landmarks = [line.strip() for line in file.readlines() if line.strip()]
    return landmarks


def create_map(landmarks, output_file='landmark_map.html'):
    if landmarks:
        first_location = gmaps.geocode(landmarks[0])
        map_location = [first_location[0]['geometry']['location']['lat'], first_location[0]['geometry']['location']['lng']]
    else:
        map_location = [48.8566, 2.3522]  
        
    map = folium.Map(location=map_location, zoom_start=12)
    icon_url = 'http://example.com/my_custom_icon.png'

    custom_icon = folium.CustomIcon(
        icon_image=icon_url,
        icon_size=(28, 30),  
        icon_anchor=(14, 30)  
    )

    for landmark in landmarks:
        location = gmaps.geocode(landmark,language='en')
        if location:
            latlng = location[0]['geometry']['location']
            folium.Marker([latlng['lat'], latlng['lng']], popup=landmark, icon=folium.Icon(icon='heart', color='red', prefix='fa')).add_to(map)

    map.save(output_file)
    print(f"Map with landmarks saved to {output_file}")


def main():
    landmarks = read_landmarks('unique_labels.txt')
    create_map(landmarks)

if __name__ == '__main__':
    main()


