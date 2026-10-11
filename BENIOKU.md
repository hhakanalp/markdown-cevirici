# Markdown Çevirici (Windows ve macOS)

Belgeleri (PDF, Word, PowerPoint, Excel, HTML…) Markdown'a çeviren masaüstü uygulaması.
Microsoft MarkItDown kütüphanesini kullanır.

## Yol 1: Kendi bilgisayarınızda oluşturun

Bilgisayarınızda Python 3.10 veya üstü kurulu olmalı (https://www.python.org/downloads/).

**Windows:** `UYGULAMAYI_OLUSTUR.bat` dosyasına çift tıklayın.
Sonuç: `dist\Markdown Cevirici\Markdown Cevirici.exe`

**macOS:** Terminal'i açın, `bash ` yazın (sonunda bir boşluk bırakın),
`UYGULAMAYI_OLUSTUR_MAC.command` dosyasını Terminal penceresine sürükleyin ve Enter'a basın.
Sonuç: `dist/Markdown Cevirici.app`

## Yol 2: GitHub derlesin (Python kurmanız gerekmez)

1. GitHub'da yeni bir depo oluşturun ve bu klasördeki tüm dosyaları yükleyin
   (`.github` klasörü de dahil).
2. Deponun **Actions** sekmesine gidin. "Uygulamayi derle" işi kendiliğinden başlar (5–10 dakika).
3. İş bitince sayfanın altındaki **Artifacts** bölümünden
   `Markdown-Cevirici-Windows` ve `Markdown-Cevirici-macOS` dosyalarını indirin.

## İlk açılışta güvenlik uyarısı

Uygulama dijital olarak imzalı olmadığı için:

- **Windows:** "Windows bilgisayarınızı korudu" uyarısında **Ek bilgi → Yine de çalıştır**.
- **macOS:** Uygulamaya sağ tıklayıp **Aç** seçin, çıkan pencerede yine **Aç**.
  Açılmazsa Terminal'de: `xattr -cr "/Applications/Markdown Cevirici.app"`
