import googlemaps
import folium

api_key = 'AIzaSyCftdIoVGOhvQcu3C6eZVLOLi5bV-qk_NU'
gmaps = googlemaps.Client(key=api_key)

# 函数用于从文件读取地标名字
def read_landmarks(file_path):
    with open(file_path, 'r') as file:
        landmarks = [line.strip() for line in file.readlines() if line.strip()]
    return landmarks

# 生成地图并标记地点
def create_map(landmarks, output_file='landmark_map.html'):
    # 如果有可用地标，使用第一个地标的位置初始化地图
    if landmarks:
        first_location = gmaps.geocode(landmarks[0])
        map_location = [first_location[0]['geometry']['location']['lat'], first_location[0]['geometry']['location']['lng']]
    else:
        # 默认回退位置
        map_location = [48.8566, 2.3522]  # Paris, France
        
    map = folium.Map(location=map_location, zoom_start=12)
    icon_url = 'http://example.com/my_custom_icon.png'

    # 创建一个自定义图标
    custom_icon = folium.CustomIcon(
        icon_image=icon_url,
        icon_size=(28, 30),  # 设置图标大小
        icon_anchor=(14, 30)  # 设置图标锚点
    )

    for landmark in landmarks:
        location = gmaps.geocode(landmark,language='en')
        if location:
            latlng = location[0]['geometry']['location']
            folium.Marker([latlng['lat'], latlng['lng']], popup=landmark, icon=folium.Icon(icon='star', color='red', prefix='fa')).add_to(map)

    map.save(output_file)
    print(f"Map with landmarks saved to {output_file}")

# 主函数
def main():
    landmarks = read_landmarks('unique_labels.txt')
    create_map(landmarks)

if __name__ == '__main__':
    main()


