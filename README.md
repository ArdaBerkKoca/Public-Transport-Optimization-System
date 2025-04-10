# Çizge Teorisi ile İstanbul Toplu Taşıma Rota Bulucu 🚇  
## Public Transport Optimization System for Istanbul using Graph Theory 🌍

Bu proje, İstanbul'daki ilçeleri temsil eden bir graf üzerinde en kısa rotayı bulmak için Dijkstra ve A* algoritmalarını kullanır.  
Toplu taşıma verileri Google Maps Directions API üzerinden alınır.

This project uses Graph Theory to find the shortest public transportation route between districts in Istanbul using Dijkstra and A* algorithms.  
Transit data is retrieved via the Google Maps Directions API.

---

## Özellikler / Features
- İlçeler arası en kısa rota (süre bazlı)  
  → Shortest path between districts (based on duration)  
- A* ve Dijkstra algoritması karşılaştırması  
  → Comparison between A* and Dijkstra algorithms  
- Toplu taşıma adımları (hat, ajans, durak bilgisi)  
  → Transit steps with vehicle, agency, and stop names  
- Harita üzerinde rota görselleştirme (Folium ile)  
  → Visual route map rendering via Folium

---

## Kurulum / Installation

### 1. Gerekli kütüphaneleri yükle:  
Install the required libraries:

```bash
pip install -r requirements.txt
```

---

### 2. `.env` dosyası oluştur ve API anahtarını ekle:  
Create a `.env` file and add your Google Maps API key:

```env
GOOGLE_MAPS_API_KEY=your_actual_api_key_here
```

---

### 3. Projeyi çalıştır / Run the project:

```bash
python main.py
```

---

## Notlar / Notes
- `.env` dosyası **gizli bilgi içerdiği için** versiyon kontrolüne dahil edilmemelidir.  
  → `.env` contains private API keys and **must be excluded from GitHub** (see `.gitignore`).
- Oluşturulan harita `outputs/route_map.html` dizininde saklanır.  
  → Generated maps are saved to the `outputs/route_map.html` path.

---

> Bu proje hem akademik hem de pratik kullanım amaçlıdır. Geliştirmeye ve katkıya açıktır!  
> This project is open for contributions and enhancements!
