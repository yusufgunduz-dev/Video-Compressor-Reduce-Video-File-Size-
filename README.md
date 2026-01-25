# Video Sıkıştırma ve Düzenleme Aracı

Bu proje, videoları sıkıştırmak, boyutlarını küçültmek ve belirli aralıklarla kesmek için geliştirilmiş masaüstü bir Python uygulamasıdır. Modern arayüzü sayesinde kullanıcı dostudur ve FFmpeg altyapısını kullanarak yüksek kaliteli işlemler gerçekleştirir.

## Özellikler

*   **Video Sıkıştırma:** Gelişmiş CRF ve `slow` preset ayarları ile videonuzu kaliteden en az ödün vererek maksimum oranda sıkıştırır. Ses dosyalarını da optimize eder (AAC 48k).
*   **Video Kesme (Trim):** Videonun sadece belirli bir bölümünü (başlangıç ve bitiş saniyeleri) alıp kaydedebilirsiniz.
*   **Çözünürlük Ayarı:** Videoları 720p, 480p gibi çözünürlüklere yeniden boyutlandırabilirsiniz.
*   **Kullanıcı Dostu Arayüz:** CustomTkinter ile oluşturulmuş şık, koyu mod destekli arayüz.
*   **İlerleme Takibi:** İşlemler sırasında yüzdelik ilerleme çubuğu ile süreci takip edebilirsiniz.
*   **Arka Plan İşlemleri:** Konsol penceresi açılmadan, temiz bir deneyim sunar.

## Kurulum ve Gereksinimler

Bu projeyi bilgisayarınızda çalıştırmak için Python kurulu olmalıdır. Ayrıca sisteminizde **FFmpeg** yüklü ve `PATH` değişkenine eklenmiş olmalıdır.

1.  **Repo'yu klonlayın:**
    ```bash
    git clone https://github.com/Gunduzy12/Video-Compressor-Reduce-Video-File-Size-.git
    cd Video-Compressor-Reduce-Video-File-Size-
    ```

2.  **Sanal ortam oluşturun (Önerilen):**
    ```bash
    python -m venv venv
    # Windows için:
    venv\Scripts\activate
    # Mac/Linux için:
    source venv/bin/activate
    ```

3.  **Gerekli kütüphaneleri yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

## Kullanım

Uygulamayı başlatmak için ana dizindeki `main.py` dosyasını çalıştırın:

```bash
python main.py
```

1.  **Dosya Seç:** "Dosya Seç" butonuna tıklayarak işlem yapmak istediğiniz videoyu yükleyin.
2.  **Sıkıştırma Ayarları:**
    *   **CRF Değeri:** Sıkıştırma seviyesini belirler. Varsayılan **36**'dır. Değer arttıkça (örneğin 40-50) dosya boyutu küçülür ancak görüntü kalitesi düşer.
    *   **Çözünürlük:** İsterseniz videonun çözünürlüğünü değiştirebilirsiniz.
3.  **Kesme (Trim):** Sadece belirli bir aralığı almak istiyorsanız Başlangıç ve Bitiş sürelerini saniye cinsinden girin.
4.  **İşlemi Başlat:** Butona basın ve arkanıza yaslanın.

## EXE Oluşturma (Build)

Uygulamayı `.exe` formatına dönüştürmek isterseniz `pyinstaller` kullanabilirsiniz:

```bash
pyinstaller --noconfirm --clean GunduzAI_VideoTool.spec
```

## Katkıda Bulunma

1.  Forklayın
2.  Dal (Branch) oluşturun
3.  Değişikliklerinizi yapın ve gönderin
4.  Pull Request oluşturun

## Lisans

MIT Lisansı.
