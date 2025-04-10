# Çizge Teorisi ile İstanbul Toplu Taşıma Rota Bulucu 🚇

Bu proje, İstanbul'daki ilçeleri temsil eden bir graf üzerinde en kısa rotayı bulmak için Dijkstra ve A* algoritmalarını kullanır. Toplu taşıma verileri Google Maps Directions API üzerinden alınır.

## Özellikler
- İlçeler arası en kısa rota (süre bazlı)
- A* ve Dijkstra algoritması karşılaştırması
- Toplu taşıma adımları (hat, ajans, durak bilgisi)
- Harita üzerinde rota görselleştirme (Folium ile)

## Kurulum
1. Python paketlerini yükle: 

```bash
pip install -r requirements.txt 
``` 

2. `.env` dosyası oluştur:
```markdown
```env
GOOGLE_MAPS_API_KEY=buraya_anahtarını_yaz
```

3. Projeyi çalıştır:
```markdown
pip install -r requirements.txt
python main.py
```

```markdown
## Not
- `.env` dosyası **yüklü değildir**, gizli bilgi içerir.
- Haritalar `outputs/route_map.html` içinde kaydedilir.
```

