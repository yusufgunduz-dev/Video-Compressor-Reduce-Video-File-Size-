<div align="center">

<img src="assets/banner.svg" alt="Video Compressor masaüstü aracı" width="100%" />

# Video Compressor

**FFmpeg ile video sıkıştırma ve kesme için modern Python masaüstü uygulaması.**

![Python](https://img.shields.io/badge/Python-3776ab?style=flat-square&logo=python&logoColor=white)
![FFmpeg](https://img.shields.io/badge/FFmpeg-007808?style=flat-square&logo=ffmpeg&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-1f6feb?style=flat-square)
![License](https://img.shields.io/badge/Lisans-MIT-green?style=flat-square)

</div>

## Özellikler

- **Video sıkıştırma:** H.264 (`libx264`), `slow` preset ve ayarlanabilir CRF ile kaliteden en az ödün vererek dosya boyutunu küçültür. Ses AAC 48 kbps olarak yeniden kodlanır.
- **CRF ayarı:** 18 ile 51 arası kaydırıcı, varsayılan 36. Değer arttıkça dosya küçülür, kalite düşer.
- **Çözünürlük seçimi:** Orijinal, 1920, 1280 veya 854 piksel genişlik (oran korunur).
- **Video kesme (trim):** Başlangıç ve bitiş saniyesini girerek yalnızca istediğiniz bölümü kaydedin.
- **İlerleme çubuğu:** İşlem sırasında yüzde olarak ilerleme gösterir, arayüz donmaz.
- **Video bilgisi:** Seçilen dosyanın süre, çözünürlük ve boyut bilgilerini gösterir.
- **Koyu, açık ve sistem teması.**

## Gereksinimler

- Python 3
- [FFmpeg](https://ffmpeg.org/download.html): `PATH` içinde erişilebilir olmalı

## Kurulum

```bash
git clone https://github.com/yusufgunduz-dev/Video-Compressor-Reduce-Video-File-Size-.git
cd Video-Compressor-Reduce-Video-File-Size-

python -m venv venv
venv\Scripts\activate        # macOS ve Linux: source venv/bin/activate

pip install -r requirements.txt
```

## Kullanım

```bash
python main.py
```

1. **Dosya Seç** ile videoyu yükleyin.
2. **Sıkıştır** sekmesinde CRF değerini ve çözünürlüğü seçin, ardından kaydedilecek yeri belirleyin.
3. Yalnızca bir bölüm istiyorsanız **Kes** sekmesinde saniye aralığını girin.

## Proje Yapısı

```
main.py                    Arayüz (CustomTkinter)
app/core/video_processor.py   FFmpeg ile bilgi alma, sıkıştırma ve kesme
requirements.txt           Bağımlılıklar
```

## EXE Oluşturma

```bash
pyinstaller --noconfirm --onefile --windowed --collect-all customtkinter --name VideoCompressor main.py
```

## Lisans

[MIT](LICENSE)

---

<sub>Geliştirici: [Yusuf Gündüz](https://github.com/yusufgunduz-dev) · [Revolasoft](https://revolasoft.com)</sub>
