import networkx as nx
import matplotlib.pyplot as plt
import random
import requests
import folium
from geopy.distance import geodesic
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GOOGLE_MAPS_API_KEY", "create api key")


# İstanbul ilçeleri
nodes = [
    "Adalar", "Arnavutköy", "Ataşehir", "Avcılar", "Bağcılar", "Bahçelievler", "Bakırköy", "Başakşehir", "Bayrampaşa", "Beşiktaş", 
    "Beykoz", "Beylikdüzü", "Beyoğlu", "Büyükçekmece", "Çekmeköy", "Esenler", "Esenyurt", "Eyüpsultan", "Fatih", "Gaziosmanpaşa", 
    "Güngören", "Kadıköy", "Kağıthane", "Kartal", "Küçükçekmece", "Maltepe", "Pendik", "Sancaktepe", "Sarıyer", "Silivri", 
    "Sultanbeyli", "Sultangazi", "Şile", "Şişli", "Tuzla", "Ümraniye", "Üsküdar", "Zeytinburnu"
]

# İlçe koordinatları
coordinates = {
    "Adalar": (40.8683, 29.1228),
    "Arnavutköy": (41.1850, 28.7427),
    "Ataşehir": (40.9923, 29.1244),
    "Avcılar": (40.9791, 28.7214),
    "Bağcılar": (41.0390, 28.8567),
    "Bahçelievler": (41.0015, 28.8598),
    "Bakırköy": (40.9780, 28.8722),
    "Başakşehir": (41.0938, 28.8028),
    "Bayrampaşa": (41.0467, 28.8985),
    "Beşiktaş": (41.0440, 29.0104),
    "Beykoz": (41.1394, 29.1003),
    "Beylikdüzü": (40.9833, 28.6390),
    "Beyoğlu": (41.0380, 28.9850),
    "Büyükçekmece": (41.0201, 28.5850),
    "Çekmeköy": (41.0468, 29.2350),
    "Esenler": (41.0438, 28.8787),
    "Esenyurt": (41.0340, 28.6758),
    "Eyüpsultan": (41.0670, 28.9480),
    "Fatih": (41.0163, 28.9497),
    "Gaziosmanpaşa": (41.0870, 28.9128),
    "Güngören": (41.0218, 28.8694),
    "Kadıköy": (40.9829, 29.0420),
    "Kağıthane": (41.0794, 28.9671),
    "Kartal": (40.8990, 29.1897),
    "Küçükçekmece": (40.9796, 28.7947),
    "Maltepe": (40.9357, 29.1312),
    "Pendik": (40.8787, 29.2722),
    "Sancaktepe": (41.0025, 29.2315),
    "Sarıyer": (41.1740, 29.0520),
    "Silivri": (41.0731, 28.2464),
    "Sultanbeyli": (40.9608, 29.2677),
    "Sultangazi": (41.1062, 28.8655),
    "Şile": (41.1746, 29.6134),
    "Şişli": (41.0605, 28.9872),
    "Tuzla": (40.8150, 29.3057),
    "Ümraniye": (41.0166, 29.1245),
    "Üsküdar": (41.0320, 29.0238),
    "Zeytinburnu": (40.9944, 28.9045)
}

# Örnek bağlantılar
edges = [
    ("Adalar", "Kadıköy"),
    ("Arnavutköy", "Başakşehir"),
    ("Ataşehir", "Kadıköy"),
    ("Avcılar", "Beylikdüzü"),
    ("Bağcılar", "Güngören"),
    ("Bahçelievler", "Bakırköy"),
    ("Bakırköy", "Zeytinburnu"),
    ("Başakşehir", "Esenyurt"),
    ("Bayrampaşa", "Gaziosmanpaşa"),
    ("Beşiktaş", "Şişli"),
    ("Beykoz", "Üsküdar"),
    ("Beylikdüzü", "Avcılar"),
    ("Beyoğlu", "Kağıthane"),
    ("Büyükçekmece", "Silivri"),
    ("Çekmeköy", "Sancaktepe"),
    ("Esenler", "Bayrampaşa"),
    ("Esenyurt", "Avcılar"),
    ("Eyüpsultan", "Kağıthane"),
    ("Fatih", "Eminönü"),
    ("Gaziosmanpaşa", "Sultangazi"),
    ("Güngören", "Bahçelievler"),
    ("Kadıköy", "Üsküdar"),
    ("Kağıthane", "Şişli"),
    ("Kartal", "Maltepe"),
    ("Küçükçekmece", "Avcılar"),
    ("Maltepe", "Pendik"),
    ("Pendik", "Tuzla"),
    ("Sancaktepe", "Çekmeköy"),
    ("Sarıyer", "Beşiktaş"),
    ("Silivri", "Büyükçekmece"),
    ("Sultanbeyli", "Pendik"),
    ("Sultangazi", "Gaziosmanpaşa"),
    ("Şile", "Ümraniye"),
    ("Şişli", "Beyoğlu"),
    ("Tuzla", "Pendik"),
    ("Ümraniye", "Kadıköy"),
    ("Üsküdar", "Kadıköy"),
    ("Zeytinburnu", "Fatih")
]

G = nx.Graph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)

# İBB API'den durak bilgisi çekme
def get_stop_details(stop_name):
    ibb_api_url = f"https://data.ibb.gov.tr/api/metrobus/stop?name={stop_name}"
    response = requests.get(ibb_api_url)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0].get("name", stop_name) 
    return stop_name

# Toplu taşıma verisi çekme fonksiyonu (Google Maps Directions API)
def get_travel_time_and_steps(origin, destination):
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&mode=transit&key={api_key}"
    response = requests.get(url)
    data = response.json()
    try:
        travel_time = data['routes'][0]['legs'][0]['duration']['value']
        steps = data['routes'][0]['legs'][0]['steps']
        return travel_time, steps
    except (IndexError, KeyError):
        return random.randint(300, 1200), []  # API başarısız olursa rastgele süre ve boş adımlar

# Durak isimlerini düzeltmek için
def correct_stop_names(steps):
    corrected_steps = []
    for step in steps:
        if 'transit_details' in step:  # transit_details var mı kontrol et
            start_stop = step['transit_details'].get('departure_stop', {}).get('name', 'Bilinmeyen Durak')
            end_stop = step['transit_details'].get('arrival_stop', {}).get('name', 'Bilinmeyen Durak')
            corrected_start = get_stop_details(start_stop)
            corrected_end = get_stop_details(end_stop)
            step['transit_details']['departure_stop']['name'] = corrected_start
            step['transit_details']['arrival_stop']['name'] = corrected_end
        corrected_steps.append(step)
    return corrected_steps

# Çizge ağırlıklarını dinamik trafik verisine göre güncelleme
for u, v in G.edges():
    travel_time, _ = get_travel_time_and_steps(u, v)
    G[u][v]['weight'] = travel_time / 60

# A* algoritması için heuristik (düz bir çizgideki uzaklık)
def heuristic(node1, node2):
    coord1 = coordinates.get(node1, (0, 0))
    coord2 = coordinates.get(node2, (0, 0))
    if coord1 == (0, 0) or coord2 == (0, 0):
        return 0  # Eğer koordinat bulunamazsa sıfır döndür
    return geodesic(coord1, coord2).kilometers

# Kullanıcıdan başlangıç ve bitiş duraklarını al
start_node = input("Başlangıç durağı: ").strip().title()
end_node = input("Bitiş durağı: ").strip().title()

if start_node not in nodes or end_node not in nodes:
    print("Geçersiz başlangıç veya bitiş durağı.")
    exit()


# Djikstra Algoritması
try:
    shortest_path = nx.dijkstra_path(G, start_node, end_node, weight='weight')
    shortest_path_length = nx.dijkstra_path_length(G, start_node, end_node, weight='weight')

    print(f"En kısa yol ({start_node} -> {end_node}): {shortest_path}")
    print(f"En kısa yol uzunluğu: {round(shortest_path_length, 1)} dakika")

    # A* Algoritması
    shortest_path_astar = nx.astar_path(G, start_node, end_node, heuristic=heuristic, weight='weight')
    shortest_path_length_astar = nx.astar_path_length(G, start_node, end_node, heuristic=heuristic, weight='weight')

    print(f"A*: En kısa yol ({start_node} -> {end_node}): {shortest_path_astar}")
    print(f"A*: En kısa yol uzunluğu: {round(shortest_path_length_astar, 1)} dakika")

    # Toplu taşıma araçlarını yazdırma
    _, steps = get_travel_time_and_steps(f"{start_node}, Istanbul", f"{end_node}, Istanbul")
    if steps:
        steps = correct_stop_names(steps)  # Durak isimlerini düzelt
        print("Kullanılacak toplu taşıma araçları:")
        for step in steps:
            if 'transit_details' in step:  # transit_details var mı kontrol et
                travel_mode = step['transit_details'].get('line', {}).get('vehicle', {}).get('type', 'Yürüyüş')
                line_name = step['transit_details'].get('line', {}).get('short_name', 'Bilinmeyen Hat')
                start_stop = step['transit_details'].get('departure_stop', {}).get('name', 'Bilinmeyen Durak')
                end_stop = step['transit_details'].get('arrival_stop', {}).get('name', 'Bilinmeyen Durak')
                agency_name = step['transit_details'].get('line', {}).get('agencies', [{}])[0].get('name', 'Bilinmeyen Ajans')
                print(f"{travel_mode} ({line_name} - {agency_name}): {start_stop} -> {end_stop}")
            else:
                print("Yürüyüş adımı veya transit olmayan bir detay.")
    else:
        print("Toplu taşıma bilgisi alınamadı.")

    # Harita üzerinde rota görselleştirme
    def visualize_route_on_map(origin, destination, api_key):
        url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&mode=transit&key={api_key}"
        response = requests.get(url)
        data = response.json()

        try:
            steps = data['routes'][0]['legs'][0]['steps']
            route_points = []
            for step in steps:
                start_lat = step['start_location']['lat']
                start_lng = step['start_location']['lng']
                route_points.append((start_lat, start_lng))

            start_location = route_points[0]
            map_route = folium.Map(location=start_location, zoom_start=12)
            folium.PolyLine(route_points, color="blue", weight=5, opacity=0.7).add_to(map_route)
            return map_route
        except (IndexError, KeyError):
            print("Rota verisi alınamadı.")
            return None

        # Rota haritasını oluştur ve kaydet
    map_route = visualize_route_on_map(start_node, end_node, api_key)

    if map_route:
        import os

        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)  # outputs klasörü yoksa oluştur

        output_path = os.path.join(output_dir, "route_map.html")
        map_route.save(output_path)
        print(f"Rota haritası '{output_path}' olarak kaydedildi.")


except nx.NetworkXNoPath:
    print(f"{start_node} ile {end_node} arasında yol bulunamadı.")
