# Python 202 – Kütüphane Uygulaması (Aşama 1–2–3)

Bu repo, Global AI Hub **Python 202 Bootcamp** proje ödevinin 3 aşamasını kapsar:

1. **Aşama 1:** OOP ile terminal tabanlı kütüphane uygulaması (JSON kalıcılık)
2. **Aşama 2:** Open Library API ile ISBN'den otomatik kitap ekleme
3. **Aşama 3:** FastAPI ile REST API + `/docs` + API testleri

## 📚 Proje Hakkında

Bu proje, modern Python teknolojileri kullanılarak geliştirilmiş kapsamlı bir kütüphane yönetim sistemidir. Uygulama, kitapları ISBN numaralarıyla takip eder ve aşağıdaki özellikleri sunar:

- **Kitap Yönetimi:** Kitap ekleme, silme, listeleme ve arama işlemleri
- **Veri Kalıcılığı:** Kitap verileri JSON formatında saklanır
- **Otomatik Kitap Bilgisi:** Open Library API ile ISBN numarasından kitap bilgilerini otomatik çekme
- **Çift Arayüz:** Hem terminal tabanlı hem de web API arayüzü
- **Dokümantasyon:** FastAPI ile otomatik API dokümantasyonu (`/docs`)
- **Test Kapsamı:** Kapsamlı birim ve entegrasyon testleri

## 🚀 Kurulum

```bash
git clone https://github.com/ilkaycanguder/python202-library.git
cd python202-library

# (Önerilen) Sanal ortam
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Bağımlılıklar
pip install -r requirements.txt
```

## 💻 Kullanım

### Terminal Uygulaması

Terminal tabanlı arayüzü başlatmak için:

```bash
python main.py
```

Bu komut interaktif bir menü başlatır:

1. **Kitap Ekle (ISBN ile otomatik)** - Open Library API'den kitap bilgilerini çeker
2. **Kitap Sil (ISBN)** - ISBN numarasına göre kitap siler
3. **Kitapları Listele** - Tüm kitapları görüntüler
4. **Kitap Ara (ISBN)** - ISBN numarasına göre kitap arar
5. **Çıkış** - Uygulamadan çıkar

### REST API

API sunucusunu başlatmak için:

```bash
uvicorn api:app --reload
```

Sunucu varsayılan olarak http://127.0.0.1:8000 adresinde çalışır.

#### API Endpoint'leri

| Endpoint        | Metod  | Açıklama                                               |
| --------------- | ------ | ------------------------------------------------------ |
| `/books`        | GET    | Tüm kitapları listeler                                 |
| `/books`        | POST   | ISBN ile yeni kitap ekler (Open Library API'den çeker) |
| `/books/{isbn}` | PUT    | ISBN numarasına göre kitap bilgilerini günceller       |
| `/books/{isbn}` | DELETE | ISBN numarasına göre kitap siler                       |

#### API Dokümantasyonu

API dokümantasyonu için tarayıcınızda şu adresi açın:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 🏗️ Proje Yapısı

```
python202-library/
  ├── api.py                # FastAPI uygulaması
  ├── library/              # Temel kütüphane modülleri
  │   ├── __init__.py
  │   ├── library.py        # Kütüphane sınıfı (ana işlevler)
  │   └── models.py         # Veri modelleri (Book sınıfı)
  ├── library.json          # Kitap verilerinin saklandığı JSON dosyası
  ├── main.py               # Terminal arayüzü
  ├── README.md             # Proje dokümantasyonu
  ├── requirements.txt      # Bağımlılıklar
  ├── services/             # Harici servisler
  │   └── openlibrary.py    # Open Library API entegrasyonu
  └── tests/                # Test dosyaları
      ├── test_api.py       # API testleri
      ├── test_library.py   # Kütüphane sınıfı testleri
      └── test_openlibrary.py # Open Library servis testleri
```

## 🔧 Teknolojiler

- **Python 3.7+**: Modern Python özellikleri (dataclasses, typing)
- **FastAPI**: Yüksek performanslı web framework
- **Httpx**: Asenkron HTTP istekleri için modern HTTP istemcisi
- **Pydantic**: Veri doğrulama ve ayarlar yönetimi
- **Pytest**: Test framework ve test araçları
- **Uvicorn**: ASGI sunucusu (FastAPI için)
- **JSON**: Veri kalıcılığı için hafif format

## 🧪 Testler

Testleri çalıştırmak için:

```bash
pytest
```

Test kapsamı:

- **Library Sınıfı**: Kitap ekleme, silme, listeleme ve arama işlevleri
- **Open Library API**: API çağrıları ve veri işleme (mock kullanarak)
- **FastAPI Endpoint'leri**: HTTP istekleri ve yanıtları

## 📝 Notlar

- Uygulama, kitap verilerini `library.json` dosyasında saklar
- Open Library API, kitap bilgilerini ISBN numarasına göre çeker
- API çağrılarında hata yönetimi ve alternatif yollar uygulanmıştır
- Testlerde gerçek API çağrıları yerine mock kullanılmıştır

## 🔗 Faydalı Linkler

- [FastAPI Dokümantasyonu](https://fastapi.tiangolo.com/)
- [Open Library API](https://openlibrary.org/developers/api)
- [Httpx Dokümantasyonu](https://www.python-httpx.org/)
- [Pydantic Dokümantasyonu](https://pydantic-docs.helpmanual.io/)
