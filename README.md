# Gölge Boksu Hareket Sınıflandırması

Bu proje, gölge boksu (shadow boxing) videolarındaki hareketleri (direct, kroşe, aparkat, gard, eğilme, belirsiz) sınıflandırmak amacıyla geliştirilmiş bir görüntü işleme ve derin öğrenme sistemidir. Çalışma kapsamında pose tahmini, iskelet çıkarımı ve farklı görüntü tabanlı Transformer mimarileri kullanılmıştır.

## 🔍 Proje Amacı

Gölge boksu yapan bireylerin çeşitli hareketlerini sınıflandırmak, bu alanda otomatik analiz ve değerlendirme yapılmasına olanak tanımaktır. Projede 5 farklı hareket sınıfı ve 1 adet belirsiz sınıfı bulunmaktadır:

- direct
- hook (kroşe)
- uppercut (aparkat)
- gard
- slip (eğilme)
- uncertain (belirsiz)

## 📁 Proje Adımları

### 1. Veri Toplama (Web Scraping)

YouTube üzerinden Selenium ve yt-dlp kullanılarak sınıflara özgü anahtar kelimelerle videolar otomatik olarak indirildi.

```bash
python scrape.py -s "uppercut boxing" -l 20 -o raw_videos
```

### 2. Frame’lere Ayırma

İndirilen videolar OpenCV ile her 10. kare alınarak frame’lere bölündü.

```bash
python extract_frames.py
```

### 3. Pose Tahmini ve İskelet Çizimi

MediaPipe ile önemli eklem noktaları alınarak sadece iskelet gösterimi olan yeni görseller üretildi. Bu sayede model yalnızca duruşları öğrenmeye odaklandı.

### 4. Görsel Etiketleme

Basit bir klavye destekli arayüz ile kullanıcı, her iskelet görüntüsünü uygun sınıf klasörüne manuel olarak taşıdı (ör. Q → direct, W → hook vb.).

### 5. Veri Dengeleme ve Çoğaltma

Veri dengesizliği olan sınıflarda `torchvision.transforms` ile görüntü artırımı (augmentation) uygulandı.

### 6. Eğitim ve Modeller

Projede aşağıdaki 5 farklı görüntü tabanlı model kullanılarak eğitimler gerçekleştirildi:

| Model        | Özellikler                        |
|--------------|----------------------------------|
| ViT          | Patch tabanlı saf transformer    |
| DeiT         | Data-efficient ViT               |
| Swin         | Kaydırmalı pencere mimarisi      |
| BEiT         | BERT tabanlı görsel öğrenme      |
| ConvNeXt     | CNN + Transformer harmanı        |

Her model `224x224` giriş boyutu ile eğitilmiş, `Adam` optimizer ve `CrossEntropyLoss` ile optimize edilmiştir.

### 7. Değerlendirme Metrikleri

Aşağıdaki performans metrikleri her model için raporlanmıştır:

- Accuracy (Doğruluk)
- Precision / Recall / F1-Score
- ROC AUC Skoru
- Sensitivity & Specificity
- Confusion Matrix (Karışıklık Matrisi)
- Eğitim ve Doğrulama Kayıp Grafikleri

### 8. Eğitim ve Test Ortamı

- Google Colab Pro (A100 GPU)
- Python 3.10
- PyTorch, torchvision, timm, mediapipe, matplotlib, seaborn

## 📊 Örnek Sonuçlar (ViT)

```
Accuracy: %85
Direct → Sensitivity: 0.91
Uppercut → Specificity: 0.98
...
```

## 💾 Model Kayıt

Eğitim sonrası her model `.pth` formatında Google Drive'a kaydedilir:

```python
torch.save(model.state_dict(), "/content/drive/MyDrive/vit_model_skeleton.pth")
```

## 📂 Klasör Yapısı

```
.
├── raw_videos/         # İndirilen YouTube videoları
├── framevideo/         # Frame'e ayrılmış videolar
├── etiketler/          # Etiketlenmiş orijinal görseller
├── iskelet/            # MediaPipe iskelet görselleri
├── train/val/          # Eğitim ve doğrulama verileri
├── model_kodlari/      # ViT, Swin, DeiT, BEiT, ConvNeXt
```

## ✍️ Yazar

**Hakan Fırat** – [github.com/hakan8755](https://github.com/hakan8755)

## 📄 Lisans

Bu proje MIT Lisansı ile lisanslanmıştır.
