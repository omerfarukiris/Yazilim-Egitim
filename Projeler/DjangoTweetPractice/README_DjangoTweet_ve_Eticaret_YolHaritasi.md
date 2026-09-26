xx# Django Öğrenme Yol Haritası — Önce DjangoTweet, Sonra Kendi E-Ticaret Projen

> **20 Eylül 2026 — NovaStore için güncel çalışma kararı:** E-ticaret sitesini doğrudan Django projesinin içinde geliştiriyoruz. Ortak iskelet `templates/base.html`, mağaza sayfaları `store/templates/store/`, ortak CSS `static/css/style.css` içinde olacak. Önce şablon ve statik dosya bağlantısını doğrulayıp ardından frontend'i küçük görevlerle geliştireceğiz. Güncel konum ve sıradaki görev için [27. bölüme](#27-novastoreda-güncel-durum-ve-sıradaki-görev) bak. Aşağıdaki ayrıntılı DjangoTweet rehberi ayrı bir öğrenme referansıdır; NovaStore dosyalarının yerine doğrudan kopyalanmaz.

Bu README iki ayrı amaç için hazırlanmıştır:

1. **Mevcut DjangoTweet projesinin mantığını gerçekten anlamak**
2. **İkinci projede, hazır kod kopyalamadan kendi e-ticaret sitesini geliştirmek**

Buradaki hedef yalnızca çalışan iki proje ortaya çıkarmak değildir.

Asıl hedef şudur:

> Bir Django projesine baktığımda hangi dosyanın ne yaptığını anlayabiliyorum ve yeni bir özellik gerektiğinde nereden başlamam gerektiğini biliyorum.

İkinci projede sana doğrudan bütün kodu vermek yerine daha çok **mentor / rehber** gibi ilerleyeceğim.

Yani çalışma biçimimiz şu olacak:

```text
Ben sana hedefi ve referansı vereceğim
        ↓
Sen önce kendin deneyeceksin
        ↓
Kodunu bana göstereceksin
        ↓
Ben hatalarını ve geliştirebileceğin yerleri söyleyeceğim
        ↓
Gerekirse küçük ipucu vereceğim
        ↓
Yine sen düzelteceksin
```

Hazır çözüm ancak gerçekten takıldığın noktada ve mümkün olduğunca küçük parçalar halinde kullanılacak.

---

# AŞAMA 1 — Mevcut DjangoTweet Projesini Anlamak

Önce şu an elimizde olan projeyi anlamamız gerekiyor.

Bu proje küçük görünse de Django'nun temel mantığının büyük bölümünü içeriyor:

- proje ve app yapısı,
- model,
- migration,
- veritabanı,
- form,
- view,
- URL,
- template,
- kullanıcı kayıt/giriş sistemi,
- authentication,
- authorization,
- CRUD işlemleri,
- CSRF,
- statik dosyalar,
- test,
- Git/GitHub,
- deploy.

Bu yüzden DjangoTweet'i yalnızca “tweet atan küçük bir site” olarak görme.

Aslında bu proje sonraki projelerin temelidir.

---

## 1. DjangoTweet tam olarak ne yapıyor?

Kullanıcı açısından uygulama şu özelliklere sahip:

```text
Siteyi aç
   ↓
Tweetleri gör

Hesap oluştur
   ↓
Giriş yap
   ↓
Tweet yaz
   ↓
Kendi tweetini düzenle
   ↓
Kendi tweetini sil
   ↓
Çıkış yap
```

Buradaki önemli güvenlik kuralı:

> Bir kullanıcı giriş yapmış olsa bile başka bir kullanıcının tweetini düzenleyemez veya silemez.

Bu ayrım ileride e-ticaret projesinde de çok önemli olacak.

Örneğin:

```text
müşteri → kendi siparişlerini görebilir
müşteri → başka müşterinin siparişini göremez
admin   → ürün yönetebilir
```

Yani DjangoTweet'teki kullanıcı/tweet sahipliği ileride farklı biçimlerde tekrar karşımıza çıkacak.

---

# 2. Django'nun büyük resmi

Django'daki temel istek akışı:

```text
KULLANICI / TARAYICI
        ↓
       URL
        ↓
       VIEW
      ↙    ↘
   FORM    MODEL
             ↓
         VERİTABANI
        ↓
     TEMPLATE
        ↓
HTML RESPONSE
        ↓
    KULLANICI
```

Bu diyagramı anlarsan Django'nun büyük kısmını anlarsın.

Şimdi her parçayı tek tek düşünelim.

---

## 2.1 URL ne yapar?

Örneğin kullanıcı:

```text
/addtweet/
```

adresine gider.

Django önce URL dosyalarına bakar.

```python
path(
    "addtweet/",
    views.addtweet,
    name="addtweet",
)
```

Burada Django'ya şunu söylüyoruz:

> `/addtweet/` adresine istek gelirse `addtweet` view'ını çalıştır.

URL'nin görevi işlemi yapmak değildir.

Sadece:

```text
ADRES → VIEW
```

eşlemesi yapar.

---

## 2.2 View ne yapar?

View iş mantığının merkezidir.

Örneğin:

```python
def addtweet(request):
```

şunları düşünebilir:

```text
Kullanıcı GET isteği mi attı?
        ↓
Boş form göster

Kullanıcı POST isteği mi attı?
        ↓
Gönderilen formu doğrula
        ↓
Doğruysa kaydet
        ↓
Liste sayfasına yönlendir
```

View gerektiğinde:

- Form ile konuşur.
- Model ile konuşur.
- Kullanıcıyı kontrol eder.
- Template açar.
- Redirect yapar.

---

## 2.3 Model ne yapar?

Model veritabanındaki yapıyı tarif eder.

Örneğin Tweet:

```text
Tweet
├── id
├── author
├── message
└── created_at
```

Python tarafında:

```python
class Tweet(models.Model):
```

şeklinde temsil edilir.

Modeli:

> “Tweet formu”

olarak düşünme.

Model:

> “Tweet verisinin veritabanındaki yapısı”

demektir.

---

## 2.4 Form ne yapar?

Form kullanıcıdan gelen veriyi kontrol eder.

Örneğin TweetForm:

```text
message
```

alanını kabul ediyor.

Ama:

```text
author
```

alanını kullanıcıdan istemiyoruz.

Neden?

Çünkü kullanıcı şöyle bir istek gönderebilirdi:

```text
message = Merhaba
author = başka_kullanıcı
```

Bunu istemiyoruz.

Bunun yerine backend:

```python
tweet.author = request.user
```

diyor.

Yani:

```text
Form → kullanıcının yazdığı mesaj

request.user → mesajın gerçek sahibi
```

---

## 2.5 Template ne yapar?

Template kullanıcıya gönderilecek HTML'i oluşturur.

Örneğin:

```django
{% for tweet in page_obj %}
```

Django sunucusunda çalışır.

Tarayıcıya bu kod gitmez.

Tarayıcı sonuç olarak normal HTML alır.

Template:

```text
Python verisi
      ↓
HTML görünümü
```

dönüşümünün yapıldığı yerdir.

---

# 3. Bir Tweet eklenirken tam olarak ne oluyor?

Bu akışı ezberlemek yerine adım adım takip et.

Kullanıcı formda:

```text
Bugün Django öğrendim.
```

yazıyor.

Ve **Paylaş** düğmesine basıyor.

### Adım 1 — Tarayıcı

Tarayıcı:

```text
POST /addtweet/
```

isteği gönderiyor.

### Adım 2 — URL

Django:

```python
path(
    "addtweet/",
    views.addtweet,
)
```

eşleşmesini buluyor.

### Adım 3 — View

Şu fonksiyon çalışıyor:

```python
addtweet(request)
```

### Adım 4 — Form

Gönderilen veri:

```python
TweetForm(request.POST)
```

içine giriyor.

### Adım 5 — Validation

```python
form.is_valid()
```

ile kontrol ediliyor.

Örneğin:

```text
Boş mu?
100 karakterden uzun mu?
```

### Adım 6 — Tweet nesnesi hazırlanıyor

```python
tweet = form.save(commit=False)
```

Henüz veritabanına yazılmıyor.

### Adım 7 — Sahibi atanıyor

```python
tweet.author = request.user
```

### Adım 8 — Veritabanına yazılıyor

```python
tweet.save()
```

### Adım 9 — Redirect

```python
return redirect(
    "tweetapp:listtweet"
)
```

Ana listeye dönülüyor.

---

# 4. `commit=False` neden var?

Bu satır başlangıçta garip gelebilir:

```python
tweet = form.save(commit=False)
```

Çünkü formda sadece:

```python
message
```

var.

Ama Tweet modelinde ayrıca:

```python
author
```

zorunlu.

Eğer doğrudan:

```python
form.save()
```

deseydik Tweet'i yazar atamadan kaydetmeye çalışacaktık.

Bu yüzden:

```text
Formdan Tweet oluştur
       ↓
Henüz kaydetme
       ↓
Yazarı request.user yap
       ↓
Şimdi kaydet
```

yapıyoruz.

---

# 5. `request.user` neden önemli?

Kullanıcı login olduğunda Django oturumdan hangi kullanıcının giriş yaptığını bilir.

View içerisinde:

```python
request.user
```

ile bu kullanıcıya ulaşabiliriz.

Örneğin:

```python
request.user.username
```

kullanıcı adını verir.

Bu özellik DjangoTweet'te:

```python
tweet.author = request.user
```

için kullanılıyor.

E-ticarette ileride:

```text
Sipariş kimin?
Sepet kimin?
Favoriler kimin?
```

gibi sorularda aynı mantık tekrar kullanılacak.

---

# 6. Authentication ve Authorization farkı

Bu farkı mutlaka öğren.

## Authentication

Soru:

```text
Bu kişi kim?
```

Örneğin:

```python
@login_required
```

kullanıcının giriş yapmış olmasını ister.

---

## Authorization

Soru:

```text
Bu kişi bu işlemi yapabilir mi?
```

Örneğin:

```python
tweet = get_object_or_404(
    Tweet,
    pk=pk,
    author=request.user,
)
```

Burada sadece login olması yetmiyor.

Tweetin sahibi de olması gerekiyor.

Bunu e-ticarette şöyle göreceğiz:

```text
Authentication
↓
Kullanıcı login olmuş mu?

Authorization
↓
Bu sipariş gerçekten bu kullanıcıya mı ait?
```

---

# 7. Migration mantığı

Modeli değiştirmek veritabanını otomatik değiştirmez.

Akış:

```text
models.py
   ↓
makemigrations
   ↓
migration dosyası
   ↓
migrate
   ↓
veritabanı
```

Şöyle düşün:

```text
models.py       → istediğim yapı
makemigrations → değişiklik planını oluştur
migrate         → planı veritabanına uygula
```

Bu mantık e-ticaret projesinde çok kullanılacak.

Çünkü ileride:

```text
Product
Category
Cart
CartItem
Order
OrderItem
```

gibi birçok model oluşturacağız.

---

# 8. DjangoTweet'ten e-ticarete ne taşıyacağız?

Aslında düşündüğünden çok daha fazlasını.

### DjangoTweet

```python
Tweet.objects.all()
```

### E-Ticaret

```python
Product.objects.all()
```

---

### DjangoTweet

```text
/tweets/5/edit/
```

### E-Ticaret

```text
/products/5/
```

---

### DjangoTweet

```text
Tweet sahibi
```

### E-Ticaret

```text
Sepet sahibi
Sipariş sahibi
```

---

### DjangoTweet

```text
Tweet listesi
```

### E-Ticaret

```text
Ürün listesi
```

---

### DjangoTweet

```text
TweetForm
```

### E-Ticaret

ileride örneğin:

```text
CheckoutForm
AddressForm
ProductForm (admin tarafında)
```

---

# 9. Bu projeyi ne zaman “anladım” diyeceğiz?

Şunları kendi cümlenle açıklayabiliyorsan temel proje amacına ulaşmışız demektir:

1. `models.py` ne yapıyor? models proje ıcın gereklı verılerı burada oluştururuz nıckname password gibi
2. `forms.py` ne yapıyor? oluşturudugumuzu bu modellerde eğerki input yanı kullanıcı verecekse burda olur
3. `views.py` ne yapıyor? urls yonlendırdıgı views.x fonksıyonu bruda olur path("" views.x)
4. `urls.py` ne yapıyor? urls 192.168.0.1/ path ıle buraya slaştan sonra sayfalar açarız
5. Template nedir? html kodları buarada tuutlur daha doğrusu fronted de dıyeebılırz
6. `request.user` nedir? kulalnıcının username ve passwordunu alır ama passowrd şifreli şekile
7. `commit=False` neden kullanılıyor?
8. `makemigrations` ile `migrate` arasındaki fark nedir? makemigrations migraetye hazırlar
9. `@login_required` ne yapıyor? fonksıyonun usutunde tanımlarnı kullanıcın gırış yapması gerektıgını vurguşar
10. Neden `author=request.user` kontrolü gerekiyor?
11. GET ve POST arasındaki fark nedir? get verı gonderırr post alır
12. Bir tweet gönderildiğinde hangi dosyalar sırayla devreye giriyor? urls views models forms templates

Bu sorular netleşmeden ikinci projeye çok hızlı geçmeyeceğiz.
Geçelim.

## 7. `commit=False` neden kullanılır?

Normalde:

```python
tweet = form.save()
```

dediğimizde formdaki bilgilerden bir `Tweet` nesnesi oluşturulur ve **hemen veritabanına kaydedilir**.

Ama bizim bazen kaydetmeden önce Tweet'e ekstra bir bilgi eklememiz gerekir.

Mesela:

```python
tweet = form.save(commit=False)
tweet.author = request.user
tweet.save()
```

Burada akış şu:

```text
form.save(commit=False)
↓
Tweet nesnesini oluştur
↓
Ama henüz veritabanına kaydetme

tweet.author = request.user
↓
Tweet'in sahibini ekle

tweet.save()
↓
Şimdi veritabanına kaydet
```

Yani `commit=False` şu anlama gelir:

> **“Nesneyi oluştur ama henüz veritabanına kaydetme.”**

### Neden buna ihtiyacımız var?

Diyelim formda sadece şu alan var:

```python
fields = ["message"]
```

Kullanıcı sadece:

```text
Bugün Django çalıştım.
```

yazıyor.

Ama modelde:

```python
message
author
```

alanları var.

Form `author` bilgisini kullanıcıdan almıyor. Çünkü kullanıcının kendisinin:

```text
Ben Ahmet'im
Ben Mehmet'im
```

diye author seçmesini istemiyoruz.

Biz Django tarafında otomatik olarak:

```python
tweet.author = request.user
```

diyoruz.

Bu nedenle önce:

```python
tweet = form.save(commit=False)
```

ile Tweet'i geçici olarak oluşturuyoruz.

Sonra author ekliyoruz:

```python
tweet.author = request.user
```

Son olarak:

```python
tweet.save()
```

ile kaydediyoruz.

Kısacası:

```text
commit=False
=
"Bir dakika, daha kaydetme.
Önce birkaç bilgi daha ekleyeceğim."
```

Şimdi sana küçük bir soru:

```python
tweet = form.save(commit=False)
tweet.author = request.user
tweet.save()
```

Burada neden doğrudan `form.save()` kullanmadık?

---

# AŞAMA 2 — Kendi E-Ticaret Projemizi Yapacağız

İkinci proje için geçici isim:

```text
NovaStore
```

İstersen daha sonra değiştirebiliriz.

Bu projenin temel amacı gerçek bir e-ticaret mantığını öğrenmek olacak.

Ama burada önemli bir kuralımız var.

---

# 10. Çalışma yöntemimiz: Kopyala-yapıştır yok

Bu projede çalışma şeklimiz:

```text
REFERANS
   ↓
İNCELEME
   ↓
KENDİN DENEME
   ↓
KOD İNCELEMESİ
   ↓
İPUCU
   ↓
DÜZELTME
```

Olacak.

Şu şekilde çalışmayacağız:

```text
Ben:
"Al bu 300 satır HTML."

Sen:
"Kopyaladım."

Ben:
"Al bu CSS."

Sen:
"Kopyaladım."

Sonuç:
Site çalışıyor ama neden çalıştığını bilmiyorsun.
```

Bunun yerine:

```text
Ben:
"Şu sitedeki navbar yapısını incele."

"Logo nerede?"
"Menü nasıl hizalanmış?"
"Mobilde ne oluyor?"
"Arama ve sepet nerede?"

Sonra:
"Kendi versiyonunu yaz."
```

diyeceğim.

Sen yazdıktan sonra koduna bakacağız.

---

# 11. Başlangıçtan itibaren Django içinde geliştirme

HTML ve CSS'i doğrudan NovaStore projesinde yazacağız. Önce bütün frontend'i ayrı bir sitede bitirip ardından Django'ya taşıma aşaması olmayacak. Daha önce yazılmış navbar HTML'i ve CSS dosyası bu düzene bir kez yerleştirilecek; yeniden yazılmayacak.

Django kullanmak HTML ve CSS ihtiyacını ortadan kaldırmaz:

- HTML: Sayfanın yapısı ve içerik grupları.
- CSS: Hizalama, boşluk, renk, boyut ve responsive görünüm.
- Django template: Ortak iskeletin paylaşılması ve ileride Python verilerinin HTML'e yerleştirilmesi.
- View ve URL: İstenen adres için hangi sayfanın gösterileceği.

İlk aşamada Django ile bir sayfa göstereceğiz; Product, sepet, ödeme ve kullanıcı özelliklerini aynı anda eklemeyeceğiz. Ürün alanları başlangıçta elle yazılmış örnek içerikler olabilir.

## 11.1 Oluşturduğumuz proje ve uygulama

Konuşmada kullanılan kurulum sırası:

```bash
django-admin startproject novastore
cd novastore
python3 manage.py startapp store
```

Bu komutlar zaten çalıştırıldı; mevcut projede tekrar çalıştırma. Yeni komutları `manage.py` dosyasının bulunduğu dış `novastore` klasöründe çalıştır. Projenin Python ortamı aktif olsun.

Dış `novastore` çalışma klasörüdür. İç `novastore` genel ayarları içerir. `store` mağaza uygulamasıdır. `settings.py` içindeki `INSTALLED_APPS` listesinde `"store"` bulunduğunu kontrol edeceğiz; mevcut uygulama kayıtları korunacak.

## 11.2 Kararlaştırdığımız hedef dosya yapısı

```text
DjangoTweetPractice/
├── README_DjangoTweet_ve_Eticaret_YolHaritasi.md
└── novastore/
    ├── manage.py
    ├── novastore/
    │   ├── settings.py
    │   └── urls.py
    ├── templates/
    │   └── base.html
    ├── static/
    │   └── css/
    │       └── style.css
    └── store/
        ├── migrations/
        ├── templates/
        │   └── store/
        │       └── index.html
        ├── views.py
        ├── urls.py             ← Sayfa bağlantısı adımında oluşturulacak
        ├── models.py
        └── ...
```

Bu ağaç hedef yapıdır; bütün dosyaların oluşturulduğu anlamına gelmez. `startapp`, uygulamaya ait `urls.py` dosyasını otomatik oluşturmaz.

- Proje genelindeki `templates/base.html`: HTML iskeleti, ortak navbar ve ileride footer.
- `store/templates/store/index.html`: Ana sayfanın hero, kategori ve ürün bölümleri.
- Proje genelindeki `static/css/style.css`: Ortak görünüm kuralları.
- Varsa `store/static/`: İleride sadece bu uygulamaya ait dosyalar için kullanılabilir; aynı CSS'i iki yere kopyalamayacağız. Böyle bir dosya eklenirse `store/static/store/` altında adlandırabiliriz.

Bir dosyanın ana sayfa olması klasör adıyla belirlenmez. Ana sayfa, URL yapılandırmasında boş yolun (`""`, tarayıcıda `/`) ilgili view'a bağlanmasıyla belirlenir.

## 11.3 Template ve static ayarları — os.path.join ile

Kullanıcının alışık olduğu `os.path.join` biçimiyle ilerliyoruz. Mevcut `BASE_DIR` tanımını koru. `settings.py` başında yoksa ekle:

```python
import os
```

`TEMPLATES` içindeki mevcut sözlükte yalnızca `DIRS` değerini düzenle:

```python
"DIRS": [os.path.join(BASE_DIR, "templates")],
```

Varsayılan `APP_DIRS=True` ayarı kalsın. Bu sayede kayıtlı `store` uygulamasının `templates` klasörü de aranır. Ortak klasör ile uygulama klasörünü birlikte kullanıyoruz.

Mevcut `STATIC_URL` ayarını koru. Ortak statik dosya klasörünü ekle; `STATICFILES_DIRS` zaten varsa ikinci tanım oluşturmak yerine mevcut listeyi düzenle:

```python
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
```

`BASE_DIR / "templates"` biçimi de `BASE_DIR` bir `Path` nesnesiyken geçerlidir; iki yöntemi aynı ayara birlikte yazmak gerekmez. `static` ve `templates` farklı amaçlarla kullanılır.

## 11.4 Mevcut HTML ve CSS'i yerleştirme

1. Navbarı yazdığın mevcut `index.html` dosyasını ortak `templates` klasörüne taşı ve adını `base.html` yap.
2. Mevcut `style.css` dosyasını ortak `static/css/` klasörüne taşı.
3. `base.html` başına `{% load static %}` ekle.
4. Eski `href="style.css"` bağlantısını aşağıdakiyle değiştir:

```django
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```

Bu etiket Django tarafından işlenir. Şablonu dosyaya çift tıklayarak veya Live Server ile açmak yerine Django üzerinden kontrol edeceğiz.

## 11.5 Ortak iskelet ve sayfa içeriği

`base.html` içindeki ortak header'ın ardından, body içinde değişebilir bir alan oluşturacağız:

```django
<main>
  {% block content %}{% endblock %}
</main>
```

`store/templates/store/index.html` ortak iskeleti devralacak:

```django
{% extends "base.html" %}

{% block content %}
  <!-- Ana sayfaya ait bölümleri burada kendin oluşturacaksın. -->
{% endblock %}
```

- `extends`: Ortak iskeleti devralır.
- `block`: Alt sayfanın dolduracağı alanı tanımlar.
- `include`: Ayrı bir şablon parçasını ekler. Navbarı ileride ayrı bir dosyaya ayırırsak kullanabiliriz; ilk adımda navbar base içinde kalacak.

Alt sayfada yeniden html, head ve body yazmayacağız. Navbarı da her sayfaya kopyalamayacağız.

## 11.6 İlk sayfanın kontrolü

Şablonlar hazırlandıktan sonra sırayla view, uygulama URL'si ve proje URL bağlantısını kuracağız. View `store/index.html` şablonunu render edecek. Her bağlantının neden yapıldığını ayrı görevde inceleyeceğiz.

```text
Tarayıcı: /
    ↓
novastore/urls.py
    ↓
store/urls.py
    ↓
store/views.py
    ↓
store/index.html → base.html iskeletini kullanır
    ↓
Tarayıcı HTML'i alır ve CSS'i ayrıca ister
```

Sunucuyu `python3 manage.py runserver` ile başlatıp `http://127.0.0.1:8000/` üzerinden kontrol edeceğiz. Ana sayfa bağlantısı kurulunca artık varsayılan Django başlangıç ekranı yerine kendi navbarımızı görmeyi bekleyeceğiz.

---

# 12. Referans siteler nasıl kullanılacak?

Burada amaç birebir kopyalamak değil.

Tasarım mantığını incelemek.

İnceleme sırası: Önce ekrandaki tek bir bölümü tarif et; ardından gerekiyorsa kaynakta yalnızca o bölümün küçük HTML parçasını bul. Bütün sitenin kaynak kodunu okumak gerekmiyor. Her referanstaki bütün alanları aynı gün incelemeyeceğiz.

## Referans 1 — Allbirds

Adres:

https://www.allbirds.com/

İncelenecek noktalar:

```text
Navbar
Hero
Men / Women ayrımı
New Arrivals
Best Sellers
Ürün kartları
CTA butonları
Footer
```

İlk görevlerde özellikle ana sayfanın bölüm mantığına bakacağız.

---

## Referans 2 — Apple Store

Adres:

https://www.apple.com/tr/store

İncelenecek noktalar:

```text
Kategori navigasyonu
Yatay ürün bölümleri
Kart yapıları
Boşluk kullanımı
Başlık hiyerarşisi
Ürün bilgisi
CTA yapısı
```

Apple'ı birebir tasarlamayacağız.

Özellikle:

> sade düzen ve spacing nasıl kullanılıyor?

sorusuna bakacağız.

---

## Referans 3 — Nike ürün listesi

Adres:

https://www.nike.com/tr/w

Burada özellikle ürün listeleme sayfasını inceleyeceğiz:

```text
Ürün grid yapısı
Filtreler
Kategori
Cinsiyet
Fiyat
Renk
Sıralama
Ürün kartı
```

İleride Django QuerySet filtrelemelerine geçtiğimizde bu ekran çok faydalı olacak.

---

# 13. Referans siteye bakarken ne yapmayacağız?

Şunları yapmayacağız:

```text
Inspect → bütün HTML'i kopyala
CSS'i kopyala
JavaScript'i kopyala
Aynı logoyu kullan
Aynı metinleri kullan
Aynı görselleri kullan
```

Bunun yerine:

```text
Bu tasarımın mantığı ne?
```

sorusuna cevap arayacağız.

Örneğin:

```text
4 ürün yan yana duruyor.
```

Bunu gördüğünde:

```text
"Muhtemelen grid veya flex kullanabilirim."
```

diye düşünmeni istiyorum.

---

# 14. Görevleri tek tek verme yöntemi

Her seferinde tek küçük görev verilecek. Öğrenci kodunu, gözlemini veya ekran görüntüsünü paylaşacak; bu adım kontrol edildikten sonra sıradakine geçilecek. Anlamadığı bir kavram olduğunda önce kısa açıklama ve küçük örnek verilecek.

## Navbar üzerinden izlediğimiz sıra

1. Allbirds navbarında logo, bağlantılar, boşluklar ve düğmelerin yerlerini gözlemle.
2. Kaynakta `data-header-content-desktop` ve `desktop-nav-container` gibi işaretlerle yalnızca ilgili parçayı bul.
3. `a`, `href`, `button`, `div` ve iç içe gruplamanın görevlerini açıkla.
4. Kendi HTML'inde `header → nav → logo bağlantısı` oluştur.
5. `nav-links` grubuna New, Men, Women ve Accessories bağlantılarını ekle.
6. `nav-actions` grubuna Search, Account ve Cart düğmelerini ekle.
7. Bu HTML'i Django'nun ortak base şablonuna yerleştir; sayfa ve CSS bağlantısını doğrula.
8. Flexbox ile önce üç ana grubu, sonra grupların içindeki öğeleri hizala.

İlk örnekte bağlantılar için `href="#"`, işlem düğmeleri için `type="button"` kullandık. Bunlar geçici yer tutucular; gerçek adres ve davranışlar sonraki görevlerde eklenecek.

Allbirds kaynak kodundaki `flex`, `hidden`, `lg:flex` gibi yardımcı sınıfları anlamak kavram öğrenmek içindir. NovaStore'da kendi sınıf adlarımızla normal CSS yazacağız; hazır navbar veya Bootstrap kullanmayacağız.

İlk CSS hedefleri:

| Seçilecek öğe                | Kavram                           | Beklenen sonuç                                   |
| ---------------------------- | -------------------------------- | ------------------------------------------------ |
| `nav`                        | `display: flex`                  | Logo, menü ve işlem grubu yan yana gelir.        |
| `nav`                        | `justify-content: space-between` | Gruplar arasına boşluk dağılır.                  |
| `nav`                        | `align-items: center`            | Yatay flex düzeninde gruplar dikeyde ortalanır.  |
| `.nav-links`, `.nav-actions` | `gap` ve flex                    | Her grubun kendi öğeleri arasında boşluk oluşur. |

Bu özellikler tek seferde hazır bir CSS dosyası olarak verilmeyecek. `space-between` görsel orta grubun her koşulda ekranın tam merkezinde olmasını garanti etmez; ilk hizalama anlaşıldıktan sonra gerekirse genişlik ve yerleşim kararını geliştireceğiz.

---

# 15. İlk frontend hedefimiz

İlk ana sayfa yaklaşık şu bölümlerden oluşacak:

```text
┌───────────────────────────────────────┐
│               NAVBAR                  │
├───────────────────────────────────────┤
│                                       │
│                HERO                   │
│                                       │
│         Yeni Koleksiyonu Keşfet       │
│             [ SHOP NOW ]              │
│                                       │
├───────────────────────────────────────┤
│              CATEGORY                 │
│                                       │
│     MEN       WOMEN     ACCESSORY     │
│                                       │
├───────────────────────────────────────┤
│            NEW ARRIVALS               │
│                                       │
│ [ürün] [ürün] [ürün] [ürün]          │
│                                       │
├───────────────────────────────────────┤
│             BEST SELLERS              │
│                                       │
├───────────────────────────────────────┤
│               FOOTER                  │
└───────────────────────────────────────┘
```

Bu yapıyı küçük görevlerle sen yazacaksın.

HTML'in büyük bölümleri `header → main → footer` olacak. `nav` header içinde, hero ve diğer içerik bölümleri main içinde bulunacak. Hero, sayfanın ana tanıtım alanıdır; başlık, görsel ve yönlendirme butonları içerebilir. `hero` özel bir HTML etiketi değildir.

`container` da HTML etiketi değil, içeriğin genişliğini sınırlamak ve ortalamak için verebileceğimiz sınıf adıdır. Header, section ve footer içinde gerektiği yerde kullanılabilir; navbar'dan sonra gelmesi zorunlu ayrı bir bölüm değildir.

---

# 16. Django içinde frontend görev sırası

Ön koşul: Ortak base, ana sayfa view/URL bağlantısı ve CSS yüklenmesi kontrol edilmiş olacak.

1. Navbar: Var olan HTML'i Flexbox ile hizala; boşluk ve boyutları düzenle.
2. Hero: Ana sayfanın content bloğunda başlık, açıklama, görsel ve buton alanı oluştur.
3. Kategoriler: Men, Women ve Accessories kartlarını oluştur.
4. Ürün kartı: Önce tek kartın görsel, ad ve fiyat yapısını kur.
5. Ürün grid'i: Kartları New Arrivals ve Best Sellers bölümlerinde düzenle.
6. Footer: Ortak base şablonunda oluştur.
7. Responsive görünüm: Dar ve geniş ekranlarda yerleşimi kontrol et.
8. Mobil navbar: Mobil menü görünümünü ve gerekli küçük JavaScript davranışını ekle.

Her madde gerektiğinde daha küçük görevlere bölünecek. Sayfayı Django sunucusunda kontrol edeceğiz. Örnek ürünler model aşamasına kadar elle yazılmış olabilir.

---

# 17. Kod incelemesinde neye bakacağız?

Sen kodu yazdıktan sonra sadece:

```text
çalışıyor / çalışmıyor
```

demeyeceğim.

Şunlara bakacağız:

```text
HTML semantik mi?
Class isimleri anlaşılır mı?
Aynı CSS tekrar edilmiş mi?
Flex/Grid doğru yerde mi?
Responsive tasarım mantıklı mı?
Gereksiz div var mı?
Dosya yapısı düzenli mi?
Kod okunabilir mi?
```

---

# 18. Takıldığında yardım seviyeleri

Benim yardımımı 4 seviyeye ayırabiliriz.

## Seviye 1 — Yönlendirme

Örneğin:

> Dört kartı yan yana getirmek için CSS Grid araştır. `grid-template-columns` özelliğine bak.

Kod vermem.

---

## Seviye 2 — Küçük ipucu

Örneğin:

```css
.products {
  display: grid;
}
```

Devamını sen tamamlarsın.

---

## Seviye 3 — Küçük örnek

Ana projenin kodunu vermek yerine bağımsız örnek:

```html
<div class="example-grid">
  <div>A</div>
  <div>B</div>
</div>
```

üzerinden mantığı gösteririm.

Sonra kendi projene sen uygularsın.

---

## Seviye 4 — Çözümü birlikte düzeltme

Uzun süre takılırsan senin kodunun üzerinde birlikte düzeltiriz.

Ama yine:

```text
Bütün dosyayı sil → benim kodumu yapıştır
```

yaklaşımını mümkün olduğunca kullanmayacağız.

---

# 19. Hazır görünümü veritabanı verileriyle birleştirme

Django baştan beri projede var. Bu aşamada yeni proje kurmayacağız veya tamamlanmış HTML'i başka klasöre taşımayacağız. Var olan şablonun elle yazılmış örnek içeriklerini dinamik verilerle değiştireceğiz.

Örneğin ürün kartındaki sabit ad ve fiyat yerine `{{ product.name }}` ve `{{ product.price }}` kullanacağız. View ürünleri sorgulayacak, template'e gönderecek; template bir döngüyle kartları oluşturacak. CSS ve ortak base iskeleti kullanılmaya devam edecek.

Öğrenilecek bağlantı:

```text
Product / Category → QuerySet → view context → template döngüsü → ürün kartları
```

---

# 20. İlk e-ticaret modelleri

Başlangıçta çok büyük sistem kurmayacağız.

İlk modeller:

```text
Category
Product
```

olacak.

Sonra:

```text
Cart
CartItem
```

gelecek.

Daha sonra:

```text
Order
OrderItem
```

eklenecek.

Muhtemel ilişki:

```text
Category
   ↓
Product

User
  ↓
Cart
  ↓
CartItem
  ↓
Product

User
  ↓
Order
  ↓
OrderItem
```

Bunları tek seferde yazmayacağız.

Her modeli neden eklediğimizi konuşacağız.

---

# 21. E-ticaret backend görev sırası

İlk görünüm hazır olduğunda veri ve işlev ekleme sırası (proje/app kurulumu zaten yapıldı):

```text
1. Mevcut ana sayfa view/template akışını tekrar et
2. Category modeli
3. Product modeli
4. Admin paneli
5. Product list view
6. Product detail view
7. Category filtreleme
8. Search
9. Login / Signup
10. Cart
11. CartItem
12. Sepete ekleme
13. Sepetten çıkarma
14. Adet artırma / azaltma
15. Checkout
16. Order
17. OrderItem
18. Kullanıcının siparişleri
19. Yetki kontrolleri
20. Testler
21. GitHub
22. Deploy
```

---

# 22. Filtre sistemini nasıl öğreneceğiz?

Nike gibi ürün listelerinde şunlar bulunuyor:

```text
Kategori
Cinsiyet
Renk
Fiyat
Sıralama
```

Biz önce küçük başlayacağız.

Örneğin:

```text
?category=shoes
```

Sonra Django:

```python
Product.objects.filter(
    category=...
)
```

mantığına geçecek.

Sonra:

```text
?min_price=
?max_price=
?q=
```

gibi özellikler eklenebilir.

Ama her özelliği ayrı ayrı yapacağız.

---

# 23. Sepet sistemi özellikle önemli olacak

DjangoTweet'te öğrendiğimiz:

```text
request.user
```

sepet sisteminde tekrar karşımıza çıkacak.

Mantık:

```text
Login olan kullanıcı
        ↓
Kendi sepeti
        ↓
CartItem'lar
        ↓
Product'lar
```

Burada şu soruları birlikte çözeceğiz:

```text
Sepet model mi olmalı?
CartItem neden ayrı model?
Ürün adedi nerede tutulmalı?
Aynı ürün tekrar eklenirse ne olacak?
Ürün silinirse CartItem ne olacak?
```

Hazır şemayı doğrudan vermek yerine önce bu soruları senin düşünmeni isteyeceğim.

---

# 24. Projenin zorluk seviyesini kademeli artıracağız

## Seviye 1 — Django içinde temel sayfa ve frontend

```text
Template / base / extends / block
View ve URL ile ana sayfayı gösterme
Static dosyaları bağlama
HTML / CSS / Responsive
```

## Seviye 2 — Ürün verileri ve dinamik sayfalar

```text
Product
Category
List
Detail
```

## Seviye 3 — Kullanıcı sistemi

```text
Signup
Login
Logout
Account
```

## Seviye 4 — Sepet

```text
Cart
CartItem
Quantity
Total
```

## Seviye 5 — Sipariş

```text
Checkout
Order
OrderItem
```

## Seviye 6 — Gelişmiş özellikler

```text
Search
Filter
Pagination
Favorites
Reviews
Stock
```

## Seviye 7 — Production

```text
Tests
GitHub
PostgreSQL
Deploy
Environment variables
Static/media
```

---

# 25. Bu projede AI nasıl kullanılacak?

Amaç AI kullanmamak değil.

Ama:

```text
AI = benim yerime projeyi yaz
```

şeklinde kullanmayacağız.

Bunun yerine:

```text
AI = öğretmen
AI = code reviewer
AI = debugger
AI = kavram açıklayıcı
AI = görev veren mentor
```

olarak kullanacağız.

İdeal soru:

> Product kartlarını yaptım fakat mobilde taşıyor. Kodum bu. Neyi yanlış düşünüyorum?

Kötü kullanım:

> Bana komple profesyonel e-ticaret sitesi yaz.

Birinci kullanım öğrenmeni sağlar.

İkinci kullanım çoğunlukla çalışan ama senin sahip olmadığın bir kod tabanı üretir.

---

# 26. Proje boyunca senden beklediğim şey

Bir şey çalışmadığında önce birkaç dakika kendin incele.

Şunlara bak:

```text
Browser DevTools
Console
Django terminal output
Traceback
HTML structure
CSS selector
Network request
```

Sonra bana:

```text
Ben bunu yapmaya çalışıyorum.
Beklediğim sonuç bu.
Aldığım sonuç bu.
Kodum burada.
Şunları denedim.
```

şeklinde gelirsen çok daha hızlı ve öğretici ilerleyebiliriz.

---

# 27. NovaStore'da güncel durum ve sıradaki görev

20 Eylül 2026 tarihli konuşma ve paylaşılan ekran görüntülerine göre ilerleme:

## Tamamlandığı görülen adımlar

- [x] Allbirds navbarı ve hero kavramı incelendi.
- [x] `header`, `nav`, `main`, `footer`, `section` ve container mantığı konuşuldu.
- [x] Nova Store logo bağlantısı, `nav-links` ve `nav-actions` içeren navbar HTML'i öğrenci tarafından yazıldı.
- [x] `novastore` Django projesi ve `store` uygulaması oluşturuldu.
- [x] Proje genelindeki ve uygulama içindeki `templates` / `static` klasörleri son ekran görüntüsünde görüldü.
- [x] Ortak base, uygulamaya özel ana sayfa ve ortak CSS düzeni seçildi.

## Anlatılan, henüz sonucu doğrulanmayan adımlar

- [ ] `INSTALLED_APPS` içinde `store` kaydı.
- [ ] Mevcut navbar HTML'inin ortak `templates/base.html` dosyasına taşınması.
- [ ] CSS'in ortak `static/css/style.css` konumuna taşınması.
- [ ] `TEMPLATES[...]["DIRS"]` içinde ortak templates yolu ve `APP_DIRS=True`.
- [ ] `STATICFILES_DIRS` içinde ortak static yolu.
- [ ] Base şablonunda `load static` ve Django static etiketiyle CSS bağlantısı.

Bir ayarın nasıl yapılmış olması gerektiğini konuşmamız, o ayarın uygulanıp çalıştığını doğruladığımız anlamına gelmez. Bunlar yapılmışsa tekrar oluşturmak yerine yerlerini ve sonuçlarını kontrol edeceğiz.

## Şu anki tek görev

**Ortak HTML ve CSS bağlantısının hazırlığını tamamla.** 11. bölümdeki hedef yapıyla klasörlerini karşılaştır. `base.html`, `style.css` ve ilgili ayarları kontrol edip dosya ağacını ve değiştirdiğin kısa parçaları paylaş. Tam ayar dosyasını veya gizli anahtarları paylaşmak gerekmiyor.

## Bu görevden sonraki sıra

1. `base.html` içine main ve content bloğunu ekle.
2. `store/templates/store/index.html` oluştur; base'i extends ederek content bloğuna küçük bir deneme başlığı yaz.
3. `store/views.py` içinde bu şablonu gösteren ana sayfa view'ını yaz.
4. Uygulama `urls.py` dosyasını oluştur ve proje URL dosyasından bağla.
5. Django sunucusunda `/` adresinin kendi sayfanı gösterdiğini ve CSS'in yüklendiğini doğrula.
6. Navbarın Flexbox hizalamasına dön.

Her adım ayrı görev olarak verilecek. Burada hedef bütün siteyi hemen bitirmek değil, yazılan her parçanın görevini anlayarak çalışan ana sayfaya ulaşmak.

---

# 28. Son hedef

Bu iki proje sonunda hedef şu değil:

> DjangoTweet yaptım ve e-ticaret sitesi yaptım.

Hedef:

> Bir web uygulamasını parçalara ayırabiliyorum.

> Frontend gördüğümde yapısını analiz edebiliyorum.

> Bir özelliği modele, view'a, URL'ye ve template'e nasıl bağlayacağımı biliyorum.

> Bir hata aldığımda önce nerede aramam gerektiğini biliyorum.

> AI'dan komple çözüm istemek yerine doğru yerde yardım alabiliyorum.

Bu seviyeye geldiğinde üçüncü projeyi çok daha bağımsız yapabilirsin.

---

# AŞAMA 1 İÇİN DETAYLI DJANGOTWEET REHBERİ

Aşağıda mevcut DjangoTweet rehberinin ayrıntılı sürümü bulunmaktadır. Bu bölüm DjangoTweet için başvuru kaynağıdır; NovaStore kurulumuna devam ederken içindeki proje oluşturma ve tam dosya örneklerini yeniden uygulama. NovaStore için yukarıdaki AŞAMA 2 ve güncel görev sırası geçerlidir.

> **Bu sürüm nasıl kullanılmalı?**
> Bu dosya “kodu kopyala ve çalıştır” rehberi değildir. Her bölümde önce **ne yapacağımızı**, sonra **neden yaptığımızı**, en son da **nasıl kontrol edeceğimizi** takip et.
>
> Django öğrenirken en önemli şey dosya isimlerini ezberlemek değil, aşağıdaki akışı anlamaktır:
>
> ```text
> Tarayıcıdan istek
>        ↓
> URL
>        ↓
> View
>        ↓
> Form / Model
>        ↓
> Veritabanı
>        ↓
> Template
>        ↓
> Tarayıcıya HTML yanıtı
> ```
>
> Bu README'de orijinal projedeki **tam kodlar, güvenlik kontrolleri, otomatik testler, Git/GitHub, Render yayını, hata çözme tablosu ve alıştırmalar korunmuştur**. Anlatımı daha anlaşılır yapmak için ana bölümlerin başına ek açıklamalar eklendi.
>
> **Çalışma kuralı:** Bir bölümü anlamadan sonraki bölüme geçmek zorunda değilsin. Özellikle ilk çalışmada 2–13. bölümler Django'nun temelini oluşturur. 14–15 bilgiyi sağlamlaştırır; 16–19 Git ve yayındır.

Bu dosya senin çalışma kitabın. Amaç, hazır projeyi çalıştırmakla yetinmeden **hangi dosyayı neden oluşturduğunu, bir isteğin nasıl işlendiğini ve siteyi nasıl yayınladığını anlayarak** aynı fikri yeniden kurman. Temel proje için gereken komutlar, backend ve frontend dosyalarının tam içerikleri, kontroller ve hata çözümleri burada. Kaynak bağlantıları ek okuma içindir; adımları tamamlamak için başka bir örnekte eksik kod araman gerekmiyor.

**Çalışma şekli:** Bu README mevcut eğitim projesinde durur. Uygulamayı sen, ayrı bir `Projeler/DjangoTweetPractice` klasöründe yazarsın. İstersen bu README'yi oraya kopyalayarak tek kaynaktan ilerle. Bu doküman güncellenirken mevcut uygulamanın Python, HTML, CSS veya veritabanı dosyaları değiştirilmedi.

**Sürüm ve kapsam:** Rehber 19 Eylül 2026 için Python **3.12** ve Django **5.2 LTS** ile hazırlanmıştır. Eski eğitim projen Django 4.2.30 kullanıyor; onun desteği sona erdiği için yeni çalışmayı 5.2 ile kuruyoruz. Bu bir mevcut veritabanını yükseltme rehberi değildir. [Django destek takvimi](https://www.djangoproject.com/download/#supported-versions).

**Doğrulama:** Bu dosyadaki 19 tam dosya örneği geçici, ayrı bir projeye çıkarılarak Python 3.12.14, Django 5.2.17, Gunicorn 23.0.0 ve WhiteNoise 6.12.0 ile çalıştırıldı. Django kontrolü, migration üretme/uygulama, statik toplama, 12 otomatik test ve Gunicorn yapılandırma kontrolü geçti. Render ortamı yerelde taklit edilerek HTTPS/CSRF, host doğrulama ve hash'li CSS/JS sunumu da kontrol edildi. Yeni örnek canlıya yayınlanmadı; tarayıcıda mobil görünüm kontrolü 12. bölümdeki elle yapılacak kontroller arasındadır. Render benzetiminde `check --deploy` yalnızca HSTS (`security.W004`) uyarısı verdi.

Yapacağın sitede herkes tweetleri görebilir. Hesap açan kullanıcı giriş yapabilir, en fazla 100 karakterlik tweet yazabilir, **yalnızca kendi tweetini** düzenleyebilir ve silebilir. Çıkış, form doğrulama, mobil görünüm ve boş liste tasarımı hazırdır. E-posta ile hesap doğrulama, parola sıfırlama e-postaları, resim yükleme ve gerçek zamanlı bildirimler bu ilk sürümün parçası değildir.

## İçindekiler

1. [Nasıl çalışmalısın?](#calisma)
2. [Büyük resim ve kavramlar](#kavramlar)
3. [Terminal, Python ve proje klasörü](#kurulum)
4. [Dosya haritası](#harita)
5. [Django ayarlarının tamamı](#ayarlar)
6. [Model, migration ve admin](#model)
7. [Form: gelen veriyi doğrulamak](#form)
8. [View: listeleme, ekleme, düzenleme, silme](#view)
9. [URL: adresleri view'lara bağlamak](#url)
10. [Frontend: HTML dosyalarının tamamı](#html)
11. [Frontend: CSS ve küçük JavaScript desteği](#css)
12. [İlk çalıştırma ve kullanıcı senaryoları](#ilk-test)
13. [Kod akışını adım adım takip etmek](#akis)
14. [Elle HTML, Form ve ModelForm karşılaştırması](#form-karsilastirma)
15. [Otomatik testler](#testler)
16. [Git ve GitHub](#git)
17. [Yayın ayarlarını anlamak](#yayin-mantigi)
18. [Render'da ücretsiz deneme yayını](#render)
19. [Yayını durdurmak ve yeniden açmak](#durdurma)
20. [Ertesi gün devam etmek](#devam)
21. [Hata çözme tablosu](#hatalar)
22. [Kendi başına alıştırmalar ve cevaplar](#alistirmalar)
23. [Mevcut projeyle farklar](#eski-proje)
24. [Resmî kaynaklar ve sözlük](#kaynaklar)

<a id="calisma"></a>

## 1. Nasıl çalışmalısın?

> ### Bu bölüm neden var?
>
> Bu proje birçok dosyadan oluşuyor. Hepsini aynı anda anlamaya çalışırsan `models.py`, `views.py`, HTML, Git ve Render birbirine karışabilir. Bu bölüm sana **hangi sırayla ilerlemen gerektiğini** söylüyor.
>
> Her adımda kendine üç soru sor:
>
> 1. **Şu anda hangi dosyayı değiştiriyorum?**
> 2. **Bu dosyanın projedeki görevi ne?**
> 3. **Yaptığım değişikliğin çalıştığını nasıl kontrol edeceğim?**
>
> Bir komutu veya kodu sadece çalıştırıp geçme. Örneğin `migrate` yazdığında “neden migrate gerekiyor?” sorusunu cevaplayabiliyorsan gerçekten öğreniyorsun.

Her bölümde şu sırayı izle: **amacı oku → kodu yaz → açıklamayı incele → kontrolü yap → soruyu cevapla**. Kodu yazmadan önce sonucu tahmin et. Hata aldığında hemen tüm dosyayı değiştirme; en sondaki hata satırını oku, ilgili dosyayı bul, tek değişiklik yap ve yeniden dene.

Önerilen oturumlar:

| Oturum | Bölümler | Bitirme ölçütü                                                          |
| ------ | -------- | ----------------------------------------------------------------------- |
| 1      | 2–6      | Ortam hazır, tablolar ve admin çalışıyor.                               |
| 2      | 7–9      | Form, view ve URL dosyaları tamam. HTML gelene kadar sayfa testi yapma. |
| 3      | 10–12    | Hazır frontend ile tüm temel işlemler çalışıyor.                        |
| 4      | 13–15    | Akışı anlatabiliyor, yetki testlerini çalıştırabiliyorsun.              |
| 5      | 16–19    | GitHub, yayın, canlı kontrol ve askıya alma tamam.                      |

Bir kod bloğunun üzerinde **Dosya** yazıyorsa o bloğu belirtilen dosyanın **tam içeriği** olarak kullan. **Terminal** yazıyorsa komutu terminalde çalıştır. Bir Python kod bloğunu terminale doğrudan yapıştırma. Üç ters tırnak işaretini dosyaya kopyalama. `...` ile eksik bırakılmış bir uygulama dosyası yoktur.

Yeni proje için bundan sonraki bütün göreli dosya yolları, aksi belirtilmedikçe **`manage.py` bulunan `DjangoTweetPractice` klasörüne göredir**. Bu klasör çalışma kökümüzdür. Eski projenin iç içe klasörlerini buraya karıştırma.

<a id="kavramlar"></a>

## 2. Büyük resim ve kavramlar

> ### Önce büyük resmi oturt
>
> Django'da kullanıcı doğrudan `models.py` veya veritabanıyla konuşmaz. Tarayıcı bir **HTTP isteği** gönderir; Django önce URL'ye bakar, ilgili view'ı çalıştırır, gerekiyorsa form ve model üzerinden veritabanına gider ve sonunda bir HTTP yanıtı döndürür.
>
> Bu bölüm ileride göreceğin bütün dosyaların birbirine **neden bağlı olduğunu** açıklar. Özellikle şu ayrımı unutma:
>
> - **Authentication:** Kullanıcı kim?
> - **Authorization:** Bu kullanıcı bu işlemi yapmaya yetkili mi?
>
> Giriş yapmış olmak tek başına başka kullanıcının tweetini düzenleme hakkı vermez. Bu yüzden sahiplik kontrolünü backend'de ayrıca yapacağız.

Bir ziyaretçi sayfayı açtığında:

```text
Tarayıcı → HTTP isteği → URL eşleşmesi → view
                                         ↓
                                 model ile veritabanı
                                         ↓
Tarayıcı ← HTML yanıtı ← template + veriler
```

Bir tweet gönderdiğinde ise formdan gelen veri önce doğrulanır; geçerliyse veritabanına yazılır. Sonra tarayıcı liste sayfasına yönlendirilir.

| Kavram         | Bu projedeki somut karşılığı                                                              |
| -------------- | ----------------------------------------------------------------------------------------- |
| Frontend       | Kullanıcının gördüğü HTML, CSS ve küçük karakter sayacı.                                  |
| Backend        | Python/Django ile istek işleme, doğrulama ve yetki kontrolü.                              |
| HTTP           | Tarayıcı ile sunucunun istek/yanıt iletişimi.                                             |
| GET            | Sayfa veya veri isteme; listeyi açma gibi. Veriyi silmemeli.                              |
| POST           | Form gönderme; tweet ekleme veya silme gibi.                                              |
| Model          | Bir tweetin hangi alanlara sahip olduğunu tanımlayan sınıf.                               |
| ORM            | `Tweet.objects...` ifadelerini veritabanı sorgularına çeviren Django katmanı.             |
| View           | İsteği alır, yapılacak işi belirler, bir yanıt döndürür.                                  |
| Template       | Django'nun verilerle doldurduğu HTML şablonu.                                             |
| URL name       | Bir adresin kod içinde kullanılan adı; `tweetapp:listtweet` gibi.                         |
| Migration      | Veritabanı yapısındaki değişikliğin sürümlenmiş tarifi.                                   |
| Session        | Giriş yapan kullanıcıyı sonraki isteklerde tanımaya yarayan mekanizma.                    |
| Cookie         | Tarayıcının sakladığı küçük değer; bu örnekte oturum kimliğini taşır.                     |
| CSRF           | Başka bir siteden kullanıcının oturumuyla istenmeyen işlem yaptırmayı önleyen kontroller. |
| Authentication | “Bu kullanıcı kim?” Giriş kontrolü.                                                       |
| Authorization  | “Bu kullanıcı bu tweeti silebilir mi?” Yetki kontrolü.                                    |

**Düşün:** Silme düğmesini CSS ile saklamak neden yeterli değildir? Kullanıcı adresi veya isteği elle gönderebilir. Yetkiyi backend'de de kontrol etmeliyiz.

<a id="kurulum"></a>

## 3. Terminal, Python ve proje klasörü

> ### Bu bölümün amacı
>
> Henüz Django kodu yazmıyoruz. Önce projenin çalışacağı **temiz ve tekrarlanabilir ortamı** hazırlıyoruz.
>
> Buradaki `.venv`, `requirements.txt`, klasör yolu ve Python sürümü ayrıntıları gereksiz görünmesin. Bunlar “benim bilgisayarımda çalışıyor ama başka yerde çalışmıyor” türü sorunları azaltır.
>
> Bu bölüm bittiğinde:
>
> ```text
> doğru klasör
> + doğru Python
> + aktif sanal ortam
> + gerekli paketler
> + Django proje/app iskeleti
> ```
>
> hazır olacak.

### 3.1 Ön koşullar

Komutlar macOS ve zsh içindir. VS Code, Python 3.12 ve Git gerekir. Başlangıç kontrolü:

**Terminal:**

```bash
python3.12 --version
git --version
```

İlk komut `Python 3.12.x` yazmalı. `command not found` alırsan önce Python kurulmalıdır. Bu bilgisayarda `/opt/homebrew/bin/python3.12` mevcut. Homebrew kurulu başka bir Mac'te `brew install python@3.12` kullanılabilir; Homebrew yoksa Python'un resmî macOS kurulum paketini kullan. [Python indirmeleri](https://www.python.org/downloads/macos/). Önce kurulumun çalıştığını doğrula, sonra aşağıya geç.

### 3.2 Yeni çalışma alanını oluştur

Eski terminalde sanal ortam açıksa önce `deactivate` yaz. Yeni bir terminal açtıysan buna gerek yok. **Eski DjangoTweet klasöründe dosyaların üzerine yazma.**

**Terminal:**

```bash
mkdir -p "/Users/omerfarukiris/Desktop/Yazılım/Projeler"
cd "/Users/omerfarukiris/Desktop/Yazılım/Projeler"
mkdir DjangoTweetPractice
cd DjangoTweetPractice
pwd
```

`mkdir`, klasör oluşturur; `cd`, bulunduğun klasörü değiştirir; `pwd`, nerede olduğunu gösterir. `DjangoTweetPractice` zaten varsa önce içeriğine bak: yeni proje komutlarını dolu klasörde tekrar çalıştırma. `Projeler` yolu başka bilgisayarda farklı olabilir; kendi çalışma klasörünü seç.

### 3.3 Sanal ortamı kur

> **Neden sanal ortam kullanıyoruz?**
> Bilgisayarında birden fazla Python projesi olabilir. Bir proje Django 4.2, başka bir proje Django 5.2 kullanabilir. Paketleri sistem Python'una karışık biçimde kurarsan sürüm çakışmaları yaşayabilirsin. `.venv`, bu projenin paketlerini kendi alanında tutar.

**Terminal:**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python --version
python -m pip --version
```

`.venv`, yalnızca bu çalışmanın Python paketlerini tutar. `source`, mevcut terminalin kullanacağı Python'u bu ortamdan seçer. Paketleri `python -m pip` ile kurmak, `pip` ile `python` arasındaki ortam karışıklığını azaltır. `.venv` GitHub'a gönderilmez; sunucuda paketler yeniden kurulur.

### 3.4 Bağımlılık dosyasını yaz ve kur

> **Neden `requirements.txt` var?**
> Kodun tek başına yeterli değildir; kodun hangi Python paketlerine ihtiyaç duyduğunu da kaydetmeliyiz. GitHub'dan projeyi alan biri veya Render sunucusu bu dosyaya bakarak aynı bağımlılıkları kurar.
>
> `pip freeze > requirements.txt` komutunun amacı “yeni paket yüklemek” değil, o anda çalışan ortamın **kesin paket sürümlerini kayıt altına almaktır**.

**Dosya: `requirements.txt` — başlangıç içeriği**

<!-- file: requirements.txt -->

```text
Django>=5.2,<5.3
gunicorn>=23,<24
whitenoise>=6.11,<7
```

- `Django`: uygulama çatısı.
- `gunicorn`: yayın ortamında Django'yu çalıştıracak WSGI sunucusu.
- `whitenoise`: yayın ortamında CSS/JS gibi statik dosyaları sunar.
- `>=5.2,<5.3`: 5.2 serisinin uygun güncel yamasını kurar; 5.3/6.x'e kendiliğinden geçmez.

**Terminal:**

```bash
python -m pip install -r requirements.txt
python -m django --version
python -m pip freeze > requirements.txt
```

Son komut dosyayı kurulu paketlerin **tam sürümleriyle yeniden yazar**. Bunu yeni ve temiz `.venv` içinde yaptığımız için başka projelerin paketlerini toplamıyoruz. Artık `requirements.txt`, kurulumu tekrarlamak için sürüm kaydıdır. Paket indirme aşamasında internet gerekir; hazır frontend dışarıdan bir CDN istemez.

### 3.5 Django iskeletini oluştur

> **`project` ve `app` aynı şey değildir.**
> `djangotweet` bütün sitenin ana yapılandırmasıdır. `tweetapp` ise sitenin belirli bir özelliğini yöneten uygulamadır.
>
> Basit düşün:
>
> ```text
> djangotweet = bina
> tweetapp    = binadaki bir bölüm
> ```
>
> İleride başka bir özellik eklersen yeni bir app oluşturabilirsin; örneğin `profiles`, `notifications` gibi.

**Terminal:**

```bash
python -m django startproject djangotweet .
python manage.py startapp tweetapp
mkdir -p templates/registration
mkdir -p tweetapp/templates/tweetapp
mkdir -p tweetapp/static/tweetapp
export DEBUG=True
```

`startproject djangotweet .` sonundaki **nokta**, `manage.py` dosyasını bulunduğun klasöre koyar; fazladan dış `djangotweet` klasörü oluşturmaz. `startapp`, tweet özelliğinin dosyalarını oluşturur. `export DEBUG=True`, bundan sonra bu terminalden çalıştırılan komutlara geliştirme ayarını verir; dosyaya yazmaz ve yeni terminale taşınmaz.

VS Code'da **File → Open Folder** ile `DjangoTweetPractice` klasörünü aç. Python yorumlayıcısını seçerken bu klasörün `.venv/bin/python` dosyasını kullan.

### 3.6 Git'in dışarıda bırakacağı dosyalar

**Dosya: `.gitignore`**

<!-- file: .gitignore -->

```gitignore
.venv/
__pycache__/
*.py[cod]
db.sqlite3
db.sqlite3-*
staticfiles/
.env
.env.*
*.log
.DS_Store
```

Kaynak `tweetapp/static/` klasörü Git'e gider. Üretilmiş `staticfiles/` klasörü gitmez. Migration dosyaları Git'e gider; kişisel kayıtların bulunduğu SQLite dosyası gitmez. `.gitignore`, önceden commit edilmiş bir dosyayı geçmişten kaldırmaz.

**Kontrol:** `ls` çıktısında `manage.py`, `requirements.txt`, `djangotweet`, `tweetapp`, `templates` görünmeli. Gizli dosyalar için `ls -a` kullan.

<a id="harita"></a>

## 4. Dosya haritası

> ### Bu haritayı neden şimdi görüyoruz?
>
> Bundan sonra birçok kez “bu dosya nereye yazılacaktı?” sorusu çıkacak. Dosya yolu Django'da önemlidir; özellikle template ve static dosyaları yanlış klasöre koyarsan kod doğru olsa bile Django onları bulamaz.
>
> Bu bölümü ezberleme. Gerektiğinde geri dönüp **referans haritası** olarak kullan.

Bu rehberin sonunda yapı şöyle olacak:

```text
Projeler/DjangoTweetPractice/     ← komutları burada çalıştır
├── .venv/                      ← yerel Python ortamı, Git'e gitmez
├── .gitignore
├── README.md                   ← bu dosyayı buraya kopyalayabilirsin
├── requirements.txt
├── manage.py                   ← Django yönetim komutları
├── db.sqlite3                  ← migrate üretir, Git'e gitmez
├── staticfiles/                ← collectstatic üretir, Git'e gitmez
├── djangotweet/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py                 ← startproject oluşturur, değiştirmiyoruz
│   └── asgi.py                 ← startproject oluşturur, değiştirmiyoruz
├── templates/
│   ├── base.html
│   ├── includes/form_fields.html
│   └── registration/
│       ├── login.html
│       └── signup.html
└── tweetapp/
    ├── apps.py                 ← startapp oluşturur, değiştirmiyoruz
    ├── models.py
    ├── admin.py
    ├── forms.py                ← sen oluşturacaksın
    ├── views.py
    ├── urls.py                 ← sen oluşturacaksın
    ├── tests.py
    ├── migrations/             ← makemigrations dosya üretir
    ├── templates/tweetapp/
    │   ├── listtweet.html
    │   ├── tweet_form.html
    │   └── tweet_confirm_delete.html
    └── static/tweetapp/
        ├── app.css
        └── app.js
```

`tweetapp/templates/tweetapp/` tekrar değildir: şablon adını uygulamaya özgü yapar. Böylece başka bir uygulamanın `listtweet.html` dosyasıyla karışmaz.

<a id="ayarlar"></a>

## 5. Django ayarlarının tamamı

> ### `settings.py` ne işe yarar?
>
> Bu dosya bir özellik yazdığımız yer değil; Django'ya **projenin nasıl çalışacağını tarif ettiğimiz merkezi ayar dosyasıdır**.
>
> Burada Django'ya şunları söylüyoruz:
>
> - Hangi uygulamalar var?
> - Template dosyalarını nerede arayacak?
> - Hangi veritabanını kullanacak?
> - Statik dosyalar nasıl sunulacak?
> - Giriş/çıkış sonrası kullanıcı nereye gidecek?
> - Yerel ortam ile yayın ortamı arasındaki güvenlik farkları ne?
>
> `settings.py` içindeki her satırı ezberlemene gerek yok. Önemli olan ayarların **hangi problemi çözdüğünü** anlamak.

**Amaç:** Django'ya uygulamaları, şablonları, veritabanını ve ortam ayarlarını tanıtmak. Aşağıdaki içerik **yeni çalışma projesi** içindir; eski projenin ayarları üzerine uygulanacak bir yama değildir.

**Dosya: `djangotweet/settings.py`**

<!-- file: djangotweet/settings.py -->

```python
import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.environ.get("DEBUG", "False").strip().lower() == "true"
ON_RENDER = os.environ.get("RENDER", "").lower() == "true" or bool(
    os.environ.get("RENDER_EXTERNAL_HOSTNAME")
)

SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    if DEBUG and not ON_RENDER:
        SECRET_KEY = "django-insecure-local-development-only-not-for-deployment"
    else:
        raise ImproperlyConfigured("SECRET_KEY ortam değişkenini tanımla.")

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"]
ALLOWED_HOSTS += [
    host.strip()
    for host in os.environ.get("ALLOWED_HOSTS", "").split(",")
    if host.strip()
]
render_hostname = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "").strip()
if render_hostname:
    ALLOWED_HOSTS.append(render_hostname)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tweetapp.apps.TweetappConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "djangotweet.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
WSGI_APPLICATION = "djangotweet.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "tr-tr"
TIME_ZONE = "Europe/Istanbul"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "tweetapp:listtweet"
LOGOUT_REDIRECT_URL = "tweetapp:listtweet"

if ON_RENDER:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
```

### Ayarların mantığı

> **Buradaki tablo önemli.**
> Kod bloğunu kopyaladıktan sonra asıl öğrenme bu bölümde başlıyor. Özellikle `DEBUG`, `SECRET_KEY`, `ALLOWED_HOSTS`, `INSTALLED_APPS`, `TEMPLATES` ve `STATIC_ROOT` kavramlarını birbirine karıştırma.
>
> `SECRET_KEY` kullanıcı parolası değildir. `ALLOWED_HOSTS` da “hangi kullanıcı giriş yapabilir?” listesi değildir. Bunlar uygulama ve sunucu güvenliğiyle ilgili farklı ayarlardır.

| Ayar                | Neyi çözüyor?                                                                                  |
| ------------------- | ---------------------------------------------------------------------------------------------- |
| `BASE_DIR`          | Dosyaların yerini terminalin bulunduğu yere göre değil, proje köküne göre bulur.               |
| `DEBUG`             | Geliştirmede ayrıntılı hata gösterir. Yayında `False` olmalıdır.                               |
| `SECRET_KEY`        | Django'nun imzalama işlemlerinde kullanılır; veritabanı şifresi değildir.                      |
| `ALLOWED_HOSTS`     | Uygulamanın kabul ettiği host adlarını belirler; kullanıcı giriş izni değildir.                |
| `INSTALLED_APPS`    | Django'nun tanıyacağı uygulamaları kaydeder.                                                   |
| `MIDDLEWARE`        | İstek/yanıt işlenirken devreye giren oturum, güvenlik ve benzeri katmanlardır. Sıra önemlidir. |
| `DIRS` / `APP_DIRS` | Ortak `templates/` klasörünü ve uygulama şablonlarını buldurur.                                |
| `LOGIN_URL`         | Giriş gerektiren bir sayfaya misafir geldiğinde hangi URL adına yönlendirileceğini belirler.   |
| `STATIC_ROOT`       | Kaynak CSS'nin yazıldığı yer değildir; yayın sırasında toplanmış dosyaların hedefidir.         |
| `STORAGES`          | Normal dosya depolamasını ve statik dosya depolamasını ayrı tanımlar.                          |

Yerel geliştirmede terminaldeki `export DEBUG=True` sayesinde geliştirme anahtarı kullanılabilir. **Render'da gerçek `SECRET_KEY` eksikse uygulama çalışmaz**; yanlışlıkla örnek anahtarla yayına çıkmayız. Örnek geliştirme değeri gerçek sır değildir.

`os.environ.get("DEBUG", "False")` bir metin okur. `.strip()` boşlukları siler, `.lower()` küçük harfe çevirir, `== "true"` ise Python boolean değeri üretir. `bool("False")` kullanmak yanlıştır: boş olmayan metin Python'da doğru sayılır.

Bu projede `.env` okuyucu kütüphane yok. Sadece `.env` dosyası oluşturmak değişkenleri yüklemez. Yerelde terminalden, Render'da Environment alanından vereceğiz.

Render HTTPS bağlantısını karşılayıp uygulamaya yönlendirdiği için proxy başlığını yalnızca o ortamda tanıyoruz. Yerel geliştirmede HTTP çalışmaya devam eder. Bu proxy ayarını başka bir sunucuya taşırken o sunucunun başlık davranışı ayrıca kontrol edilmelidir.

**Kontrol — terminal:**

```bash
python manage.py check
```

Bu aşamada oluşturulan varsayılan URL dosyası hâlâ durduğu için kontrol geçmelidir. `SECRET_KEY` hatası varsa yeni terminal açmış olabilirsin: `export DEBUG=True` çalıştır.

<a id="model"></a>

## 6. Model, migration ve admin

> ### Bu bölümde ilk gerçek verimizi tasarlıyoruz
>
> Şimdi “Tweet nedir?” sorusunu Python sınıfıyla tanımlayacağız. Model, yalnızca ekranda görünen form değildir; veritabanında tutulacak verinin **yapısını ve ilişkilerini** tarif eder.
>
> Bu bölümün akışı:
>
> ```text
> Tweet modelini yaz
>        ↓
> migration üret
>        ↓
> migration'ı veritabanına uygula
>        ↓
> admin panelinden sonucu kontrol et
> ```
>
> Böylece frontend yazmadan önce veri katmanının çalıştığını doğrulamış olacağız.

### 6.1 Veriyi tasarla

> **Neden `author` metin değil de `ForeignKey`?**
> Kullanıcı adını tweet içine düz metin olarak kopyalarsak kullanıcı adı değiştiğinde ilişkiler zorlaşır. `ForeignKey` ile tweet doğrudan kullanıcı kaydına bağlanır. Veritabanı aslında kullanıcının kimliğini (`author_id`) tutar.

Bir tweetin kimliği, yazarı, mesajı ve oluşturulma zamanı olsun. Kullanıcı adı metnini ayrı bir alana kopyalamak yerine gerçek kullanıcı kaydına bağlayacağız.

**Dosya: `tweetapp/models.py`**

<!-- file: tweetapp/models.py -->

```python
from django.conf import settings
from django.db import models


class Tweet(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tweets",
    )
    message = models.CharField("Mesaj", max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return f"{self.author}: {self.message[:30]}"
```

- `class Tweet(models.Model)`: Django modelini genişleten bir Python sınıfı.
- `author`: bir kullanıcı nesnesine bağlanan ilişki. Veritabanında `author_id` saklanır.
- `settings.AUTH_USER_MODEL`: projenin kullanıcı modeline işaret eder; varsayılan Django kullanıcısını kullanıyoruz.
- `ForeignKey`: bir kullanıcının birçok tweeti olabilir, her tweet bir yazara aittir.
- `CASCADE`: kullanıcı silinirse bağlı tweetleri de silinir. Bu, burada seçtiğimiz davranıştır.
- `related_name="tweets"`: bir kullanıcıdan `user.tweets.all()` ile tweetlerine ulaşabilirsin.
- `max_length=100`: model ve ModelForm için mesaj sınırı. Doğrudan `objects.create()` bütün form doğrulamalarını kendiliğinden çalıştırmaz.
- `auto_now_add`: kayıt ilk oluşturulunca tarih atanır. Düzenlemede aynı kalır.
- `ordering`: yeniler önce gelir; aynı zaman değerinde `id` sıralamayı kararlı tutar.
- `id`: ayrıca yazmasan da Django'nun eklediği birincil anahtar.
- `__str__`: admin ve kabukta okunabilir temsil; kaydetme işlemi yapmaz.

### 6.2 Tabloyu oluştur

> **Model yazmak veritabanını otomatik değiştirmez.**
> `models.py` istediğimiz şemayı anlatır. `makemigrations` bu değişikliğin tarifini üretir; `migrate` ise tarifi gerçek veritabanına uygular.
>
> Bunu şu şekilde ezberlemek yerine mantığını kur:
>
> ```text
> models.py       = istediğim yapı
> migration       = değişiklik planı
> migrate         = planı DB'ye uygula
> ```

**Terminal:**

```bash
python manage.py makemigrations tweetapp
python manage.py migrate
python manage.py showmigrations tweetapp
```

`makemigrations`, model farkından bir Python migration dosyası üretir. `migrate`, o dosyaları seçili veritabanına uygular. Son komutta `[X] 0001_initial` görmelisin. Auth/session tabloları da `migrate` ile kurulur.

**Model dosyası ≠ veritabanı tablosu.** Bir alan eklediğinde ikisini migration ile eşleştirirsin. HTML/CSS değiştirdiğinde migration gerekmez. Oluşturulan migration'ları silerek hataları çözmeye çalışma; özellikle kayıt bulunan veritabanında veri kaybı yaratabilirsin.

### 6.3 Yönetim panelini bağla

> **Admin neden kullanılıyor?**
> Kendi HTML sayfalarımız henüz hazır değil. Admin paneli sayesinde modelin gerçekten kayıt oluşturup oluşturamadığını hızlıca test ediyoruz. Yani admin burada uygulamanın son kullanıcı arayüzü değil, geliştirici/yönetici kontrol aracıdır.

**Dosya: `tweetapp/admin.py`**

<!-- file: tweetapp/admin.py -->

```python
from django.contrib import admin

from .models import Tweet


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "message", "created_at")
    search_fields = ("message", "author__username")
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)
```

**Terminal:**

```bash
python manage.py createsuperuser
python manage.py runserver
```

Kullanıcı adı ve parola belirle. Terminalde parola yazarken karakter görünmemesi normaldir. E-posta bu yerel denemede boş bırakılabilir. [Admin'i aç](http://127.0.0.1:8000/admin/), giriş yap, kendi kullanıcı hesabını yazar seçerek bir tweet oluştur. Sunucuyu `Ctrl+C` ile durdur.

**Kontrol:** Admin'de tweetin görünmeli. Böylece henüz kendi frontend'ini kurmadan model → veritabanı bağlantısını doğrulamış oldun.

**Düşün:** Bir kullanıcının kullanıcı adı değişirse her tweetin mesajını güncellemek gerekir mi? Hayır; yazar ilişkisi kullanıcı kaydının kimliğine bağlıdır.

<a id="form"></a>

## 7. Form: gelen veriyi doğrulamak

> ### Formun görevi sadece HTML üretmek değildir
>
> Kullanıcıdan gelen veriye doğrudan güvenmeyiz. Tarayıcıdaki HTML veya JavaScript kontrolleri kullanıcı tarafından değiştirilebilir veya tamamen atlanabilir.
>
> `TweetForm` iki işi birlikte yapacak:
>
> ```text
> Kullanıcıya giriş alanını göster
>            +
> Gelen message değerini backend'de doğrula
> ```
>
> `author` alanını özellikle forma koymuyoruz. Çünkü tweetin kimin adına yazılacağını kullanıcıdan almak istemiyoruz; bunu güvenilir oturum bilgisi olan `request.user` üzerinden backend belirleyecek.

**Dosya: `tweetapp/forms.py` — bu dosyayı oluştur**

<!-- file: tweetapp/forms.py -->

```python
from django import forms

from .models import Tweet


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Bugün ne öğrendin?",
                    "data-count-target": "message-count",
                    "aria-describedby": "message-count",
                }
            )
        }
        error_messages = {
            "message": {
                "required": "Boş tweet gönderemezsin.",
                "max_length": "Mesaj en fazla 100 karakter olabilir.",
            }
        }

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if not message:
            raise forms.ValidationError("Boş tweet gönderemezsin.")
        return message
```

`ModelForm`, model alanlarından form üretir. `fields` içine **yalnızca `message`** aldık. Kullanıcıya yazar seçtirmiyoruz; yazarı giriş yapmış kullanıcıdan backend belirleyecek. Böylece birisi isteğe başka bir `author` değeri eklese bile bu alan form tarafından kaydedilmez.

`widget`, alanın HTML'de nasıl görüneceğini seçer. Modelin `CharField` alanını çok satırlı `textarea` olarak gösteriyoruz. `clean_message`, doğrulanan değere ek kural uygular; `ValidationError` sayfada form hatası olarak gösterilir. Sadece HTML `required` veya JavaScript kontrolüne güvenmiyoruz; kullanıcı bunları atlayabilir.

**Kontrol — terminal:**

```bash
python manage.py shell
```

**Açılan Python kabuğunda, satır satır:**

```python
from tweetapp.forms import TweetForm
form = TweetForm({"message": "Merhaba Django"})
form.is_valid()
form.cleaned_data
bad = TweetForm({"message": "a" * 101})
bad.is_valid()
bad.errors
exit()
```

İlk doğrulama `True`, ikinci `False` olmalı. Henüz `save()` çağırmadığın için yeni kayıt oluşturmadın.

<a id="view"></a>

## 8. View: listeleme, ekleme, düzenleme, silme

> ### View neden projenin merkezinde?
>
> URL bize “hangi işlem istendi?” bilgisini getirir. View ise o isteğin **iş mantığını yönetir**.
>
> Bir view gerektiğinde:
>
> - request bilgisini okur,
> - formu doğrular,
> - model üzerinden veritabanını kullanır,
> - yetki kontrolü yapar,
> - template render eder veya başka sayfaya yönlendirir.
>
> Bu bölümde CRUD'un büyük kısmını göreceksin:
>
> ```text
> Create → tweet ekle
> Read   → tweetleri listele
> Update → tweet düzenle
> Delete → tweet sil
> ```
>
> Özellikle `@login_required`, `request.user`, `commit=False`, `instance=tweet`, `author=request.user` ve `@require_POST` satırlarının **neden** kullanıldığını anlamaya çalış.

**Dosya: `tweetapp/views.py`**

<!-- file: tweetapp/views.py -->

```python
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView

from .forms import TweetForm
from .models import Tweet


def listtweet(request):
    tweets = Tweet.objects.select_related("author").all()
    page_obj = Paginator(tweets, 10).get_page(request.GET.get("page"))
    return render(request, "tweetapp/listtweet.html", {"page_obj": page_obj})


@login_required
def addtweet(request):
    if request.method == "POST":
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.author = request.user
            tweet.save()
            messages.success(request, "Tweetin paylaşıldı.")
            return redirect("tweetapp:listtweet")
    else:
        form = TweetForm()
    return render(
        request,
        "tweetapp/tweet_form.html",
        {"form": form, "heading": "Yeni tweet", "button_label": "Paylaş"},
    )


@login_required
def edittweet(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk, author=request.user)
    if request.method == "POST":
        form = TweetForm(request.POST, instance=tweet)
        if form.is_valid():
            form.save()
            messages.success(request, "Tweetin güncellendi.")
            return redirect("tweetapp:listtweet")
    else:
        form = TweetForm(instance=tweet)
    return render(
        request,
        "tweetapp/tweet_form.html",
        {"form": form, "heading": "Tweeti düzenle", "button_label": "Kaydet"},
    )


@login_required
def confirm_delete(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk, author=request.user)
    return render(request, "tweetapp/tweet_confirm_delete.html", {"tweet": tweet})


@login_required
@require_POST
def deletetweet(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk, author=request.user)
    tweet.delete()
    messages.success(request, "Tweetin silindi.")
    return redirect("tweetapp:listtweet")


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")
```

### Her parçanın görevi

> **Bu tabloyu kodun sözlüğü gibi kullan.**
> View kodu ilk bakışta uzun görünebilir ama aslında birkaç küçük görevin birleşimidir. Her satırın “hangi sorunu çözdüğünü” ayırdığında fonksiyon çok daha okunabilir hale gelir.

| Kod                                           | Neden var?                                                                                 |
| --------------------------------------------- | ------------------------------------------------------------------------------------------ |
| `request`                                     | İstek metodu, form verisi ve oturumdaki kullanıcı burada.                                  |
| `select_related("author")`                    | Listeyi ve kullanıcılarını tek sorguda alarak her tweet için ayrı yazar sorgusunu azaltır. |
| `Paginator(..., 10)`                          | Sayfa başına 10 tweet gösterir; liste büyüdükçe hepsini tek sayfaya yüklemeyiz.            |
| `get_page`                                    | Eksik veya uygunsuz sayfa numarasını ele alır.                                             |
| `@login_required`                             | Giriş yapmamış ziyaretçiyi giriş ekranına yönlendirir.                                     |
| `TweetForm(request.POST)`                     | Gönderilmiş verilerle bağlı form oluşturur.                                                |
| `is_valid()`                                  | Form ve model alanı kurallarını denetler.                                                  |
| `save(commit=False)`                          | Nesneyi hazırlar ama henüz veritabanına yazmaz.                                            |
| `tweet.author = request.user`                 | Yazarı tarayıcıdan değil, doğrulanmış oturumdan belirler.                                  |
| `instance=tweet`                              | Yeni satır açmak yerine bulunan tweeti düzenler.                                           |
| `get_object_or_404(..., author=request.user)` | Kayıt yoksa veya başkasına aitse 404 döndürür.                                             |
| `@require_POST`                               | Silme adresine GET ile gelindiğinde 405 döndürür; kayıt silinmez.                          |
| `messages.success`                            | İşlemden sonra bir kere gösterilecek bildirim ekler.                                       |
| `redirect`                                    | Kaydın ardından yeni GET isteğine geçer; sayfayı yenilemek aynı POST'u tekrar göndermez.   |

`SignUpView` sınıf tabanlı view örneğidir: `CreateView`, form gösterme ve geçerli formu kaydetme akışını sağlar. `UserCreationForm`, kullanıcı adı ve iki parola alanını doğrular, parolayı uygun şekilde hash'leyerek kaydeder. `reverse_lazy`, URL adresini sınıf yüklenirken hemen çözmek yerine gerektiğinde çözer. Kayıt sonrası otomatik giriş yapmıyoruz; giriş sayfasına gönderiyoruz.

**Önemli akış:** Geçersiz POST'ta `else` ile yeni boş form üretmedik. Hatalı ama bağlı form en alttaki `render` ile geri gösterilir. Kullanıcı yazdıklarını ve hata mesajını görebilir.

**Düşün:** `author=request.user` filtresini kaldırırsan ne olur? Oturum açmış bir kullanıcı başka bir tweetin kimliğini bilerek düzenleme/silme yapabilir. Giriş yapmış olmak, her kayda yetkili olmak değildir.

<a id="url"></a>

## 9. URL: adresleri view'lara bağlamak

> ### URL dosyası bir yönlendiricidir
>
> `urls.py` veritabanı işlemi yapmaz ve HTML üretmez. Görevi:
>
> ```text
> Bu adres gelirse → şu view çalışsın
> ```
>
> şeklinde eşleme yapmaktır.
>
> Örneğin:
>
> ```text
> /tweets/5/edit/
> ```
>
> adresindeki `5`, `<int:pk>` ile view'a gönderilir. View da hangi tweetin düzenleneceğini bu kimlikle bulur.
>
> URL'leri HTML içine düz metin olarak yazmak yerine URL **name** kullanmamızın nedeni, ileride adres yolu değişse bile uygulamanın geri kalanını daha kolay koruyabilmektir.

**Dosya: `tweetapp/urls.py` — oluştur**

<!-- file: tweetapp/urls.py -->

```python
from django.urls import path

from . import views

app_name = "tweetapp"

urlpatterns = [
    path("", views.listtweet, name="listtweet"),
    path("addtweet/", views.addtweet, name="addtweet"),
    path("tweets/<int:pk>/edit/", views.edittweet, name="edittweet"),
    path("tweets/<int:pk>/delete/", views.confirm_delete, name="confirm_delete"),
    path("tweets/<int:pk>/delete/confirm/", views.deletetweet, name="deletetweet"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
]
```

**Dosya: `djangotweet/urls.py`**

<!-- file: djangotweet/urls.py -->

```python
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", include("tweetapp.urls")),
]
```

Giriş/çıkış davranışını Django'dan alıyoruz, HTML'ini kendimiz hazırlayacağız. Bu ilk sürüm yalnızca gereken auth adreslerini açar; e-posta ayarı ve şablonları olmayan parola sıfırlama adresleri eklemiyoruz.

`<int:pk>` adresin o bölümünü tam sayı olarak alıp view'a `pk` adıyla gönderir. `app_name` sayesinde `tweetapp:edittweet` gibi adlar kullanılır. Bir URL'nin yolunu değiştirdiğinde şablonda elle yazılmış her bağlantıyı aramak yerine URL adını koruyabilirsin.

| Adres                       | Metot      | Sonuç                                        |
| --------------------------- | ---------- | -------------------------------------------- |
| `/`                         | GET        | Herkese açık tweet listesi.                  |
| `/signup/`                  | GET / POST | Hesap oluşturma.                             |
| `/login/`                   | GET / POST | Giriş.                                       |
| `/logout/`                  | POST       | Çıkış; Django 5.2'de GET logout kullanılmaz. |
| `/addtweet/`                | GET / POST | Giriş yapan kullanıcı için tweet formu.      |
| `/tweets/1/edit/`           | GET / POST | Yalnızca sahibi için düzenleme.              |
| `/tweets/1/delete/`         | GET        | Sahibine silme onayı gösterir, silmez.       |
| `/tweets/1/delete/confirm/` | POST       | Sahibinin tweetini siler.                    |
| `/admin/`                   | GET / POST | Yetkili personel için yönetim paneli.        |

**Kontrol:** `python manage.py check` çalıştır. Sayfaları açmadan önce sonraki HTML dosyalarını tamamla; aksi halde `TemplateDoesNotExist` beklenir.

<a id="html"></a>

## 10. Frontend: HTML dosyalarının tamamı

> ### Backend çalışıyor; şimdi kullanıcıya göstereceğiz
>
> Model, form, view ve URL zincirini kurduk. Template'ler bu veriyi **HTML'e dönüştüren sunucu tarafı şablonlardır**.
>
> Django template kodu tarayıcıya aynen gitmez. Örneğin:
>
> ```django
> {% for tweet in page_obj %}
> ```
>
> sunucuda çalışır; tarayıcı yalnızca sonuç olarak oluşan HTML'i görür.
>
> Bu bölümde template inheritance (`extends`), URL üretme, CSRF, koşullar, döngüler ve kullanıcıya göre görünüm değiştirme kullanılıyor.

Frontend'i hazır bir başlangıç olarak kullanabilirsin. Tasarım: açık arka plan, koyu menü, mavi ana düğmeler, kart biçiminde tweetler, mobilde tek sütun. Harici font, Bootstrap, CDN, görsel veya npm kurulumu gerektirmez.

### 10.1 Ortak sayfa iskeleti

> **Neden `base.html`?**
> Menü, CSS/JS bağlantıları, mesaj alanı ve genel sayfa iskeleti her sayfada tekrar yazılmasın diye ortak bir temel şablon oluşturuyoruz. Alt sayfalar yalnızca değişen `content` bölümünü dolduracak.

**Dosya: `templates/base.html`**

<!-- file: templates/base.html -->

```html
{% load static %}
<!DOCTYPE html>
<html lang="tr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{% block title %}DjangoTweet{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'tweetapp/app.css' %}" />
    <script src="{% static 'tweetapp/app.js' %}" defer></script>
  </head>
  <body>
    <a class="skip-link" href="#main">İçeriğe geç</a>
    <header class="site-header">
      <nav class="nav container" aria-label="Ana menü">
        <a class="brand" href="{% url 'tweetapp:listtweet' %}">Django<span>Tweet</span></a>
        <div class="nav-links">
          <a href="{% url 'tweetapp:listtweet' %}">Akış</a>
          {% if user.is_authenticated %}
          <a href="{% url 'tweetapp:addtweet' %}">Yeni tweet</a>
          <span class="nav-user">@{{ user.username }}</span>
          <form method="post" action="{% url 'logout' %}" class="inline-form">
            {% csrf_token %}
            <button type="submit" class="nav-button">Çıkış yap</button>
          </form>
          {% else %}
          <a href="{% url 'login' %}">Giriş yap</a>
          <a class="button button-small" href="{% url 'tweetapp:signup' %}">Hesap oluştur</a>
          {% endif %}
        </div>
      </nav>
    </header>

    <main id="main" class="container main-content">
      {% if messages %}
      <div aria-live="polite" class="notices">
        {% for message in messages %}
        <p class="notice">{{ message }}</p>
        {% endfor %}
      </div>
      {% endif %} {% block content %}{% endblock %}
    </main>

    <footer class="site-footer container">
      <p>DjangoTweet · Öğren, paylaş, yeniden dene.</p>
    </footer>
  </body>
</html>
```

`{% load static %}`, `{% static ... %}` etiketini kullanılabilir yapar. `block` bölgelerini alt şablonlar doldurur. `user`, auth context processor ile şablona gelir. `is_authenticated` görünümü değiştirir; backend yetki kontrolünün yerine geçmez. Çıkış bir **POST formudur**; bağlantıyla GET göndermiyoruz.

`viewport` mobil ölçeklemeyi, `lang="tr"` sayfa dilini, `label` ve `aria` özellikleri erişilebilirliği destekler. “İçeriğe geç” bağlantısı klavye kullanıcısını menüyü tekrar dolaşmaktan kurtarır. `defer`, JavaScript'i HTML çözümlendikten sonra çalıştırır.

### 10.2 Tekrar kullanılan form alanları

> **Neden ayrı include?**
> Login, signup ve tweet formunda alanları/hataları benzer biçimde göstermek istiyoruz. Aynı HTML'i üç yerde kopyalarsak ileride bir değişiklik için üç dosyayı düzeltmek gerekir. `include` tekrar eden küçük parçayı tek yerde tutar.

Önce terminalde `mkdir -p templates/includes` çalıştır.

**Dosya: `templates/includes/form_fields.html`**

<!-- file: templates/includes/form_fields.html -->

```html
{% if form.non_field_errors %}
<div class="form-errors" role="alert">{{ form.non_field_errors }}</div>
{% endif %} {% for field in form %}
<div class="field">
  {{ field.label_tag }} {{ field }} {% if field.help_text %}
  <div class="help-text" id="{{ field.auto_id }}_helptext">{{ field.help_text|safe }}</div>
  {% endif %} {% if field.errors %}
  <div class="field-errors" role="alert">{{ field.errors }}</div>
  {% endif %}
</div>
{% endfor %}
```

`include`, ortak küçük şablonu sayfaya ekler. `form.non_field_errors`, tek bir alana bağlı olmayan hataları; `field.errors`, alan hatalarını gösterir. Buradaki `help_text|safe`, kendi formumuzun ve Django'nun ürettiği güvenilir yardım HTML'i içindir. **Kullanıcının tweetine `safe` ekleme**; normal `{{ tweet.message }}` HTML karakterlerini kaçırır.

### 10.3 Ana sayfa ve tweet kartları

> Bu şablonda iki farklı konu aynı anda görülüyor:
>
> 1. View'ın gönderdiği `page_obj` verisini ekrana basmak.
> 2. Oturumdaki kullanıcıya göre hangi aksiyonların görüneceğini belirlemek.
>
> Ancak tekrar önemli nokta: “Sil” veya “Düzenle” düğmesini HTML'de gizlemek **güvenlik değildir**. Gerçek yetki kontrolü view'daki `author=request.user` filtresidir.

**Dosya: `tweetapp/templates/tweetapp/listtweet.html`**

<!-- file: tweetapp/templates/tweetapp/listtweet.html -->

```html
{% extends "base.html" %} {% block title %}Akış · DjangoTweet{% endblock %} {% block content %}
<section class="hero">
  <div>
    <p class="eyebrow">KÜÇÜK NOTLAR, YENİ FİKİRLER</p>
    <h1>Bugün ne öğrendin?</h1>
    <p class="muted">100 karakterle paylaş. Öğrenme yolculuğuna bir not bırak.</p>
  </div>
  {% if user.is_authenticated %}
  <a class="button" href="{% url 'tweetapp:addtweet' %}">Bir tweet yaz</a>
  {% else %}
  <a class="button" href="{% url 'tweetapp:signup' %}">Aramıza katıl</a>
  {% endif %}
</section>

<div class="feed-layout">
  <section aria-labelledby="feed-title">
    <div class="section-heading">
      <h2 id="feed-title">Son paylaşımlar</h2>
      <span class="badge">{{ page_obj.paginator.count }} tweet</span>
    </div>
    {% for tweet in page_obj %}
    <article class="card tweet-card">
      <header class="tweet-header">
        <span class="avatar" aria-hidden="true">{{ tweet.author.username|first|upper }}</span>
        <div>
          <h3>@{{ tweet.author.username }}</h3>
          <time datetime="{{ tweet.created_at|date:'c' }}"
            >{{ tweet.created_at|date:"d.m.Y H:i" }}</time
          >
        </div>
      </header>
      <p class="tweet-message">{{ tweet.message }}</p>
      {% if user == tweet.author %}
      <footer class="tweet-actions">
        <a href="{% url 'tweetapp:edittweet' pk=tweet.pk %}">Düzenle</a>
        <a class="danger-link" href="{% url 'tweetapp:confirm_delete' pk=tweet.pk %}">Sil</a>
      </footer>
      {% endif %}
    </article>
    {% empty %}
    <div class="card empty-state">
      <h3>Henüz paylaşım yok.</h3>
      <p>İlk notu sen bırakabilirsin.</p>
      <a href="{% url 'tweetapp:addtweet' %}">İlk tweeti yaz →</a>
    </div>
    {% endfor %} {% if page_obj.has_other_pages %}
    <nav class="pagination" aria-label="Tweet sayfaları">
      {% if page_obj.has_previous %}
      <a class="button button-secondary" href="?page={{ page_obj.previous_page_number }}">Önceki</a>
      {% endif %}
      <span>{{ page_obj.number }} / {{ page_obj.paginator.num_pages }}</span>
      {% if page_obj.has_next %}
      <a class="button button-secondary" href="?page={{ page_obj.next_page_number }}">Sonraki</a>
      {% endif %}
    </nav>
    {% endif %}
  </section>
  <aside class="card sidebar">
    <p class="eyebrow">BU ALAN SENİN</p>
    <h2>Bir fikirle başla.</h2>
    <p>Bir kod ipucu, küçük bir keşif veya günün notu. Kısa yaz, açık anlat.</p>
    <ul>
      <li>En fazla 100 karakter.</li>
      <li>Paylaşımlar herkese açık.</li>
      <li>Kendi tweetlerini düzenleyip silebilirsin.</li>
    </ul>
  </aside>
</div>
{% endblock %}
```

`for ... empty`, hem dolu listeyi hem boş durumu ele alır. `page_obj` adı, view'daki context anahtarıyla aynıdır. Tarih filtreleri gösterimi değiştirir, veritabanındaki değeri değiştirmez. “Sil” bağlantısı **onay sayfasına** gider; asıl silmeyi bir sonraki POST yapar.

### 10.4 Ekleme ve düzenleme için ortak form

> Aynı form şablonunu hem “ekle” hem “düzenle” işleminde kullanıyoruz. Farkı view'dan gönderilen `heading` ve `button_label` belirliyor. Bu, gereksiz HTML tekrarını azaltır.

**Dosya: `tweetapp/templates/tweetapp/tweet_form.html`**

<!-- file: tweetapp/templates/tweetapp/tweet_form.html -->

```html
{% extends "base.html" %} {% block title %}{{ heading }} · DjangoTweet{% endblock %} {% block
content %}
<section class="card form-card">
  <p class="eyebrow">@{{ user.username }}</p>
  <h1>{{ heading }}</h1>
  <p class="muted">Paylaşımın herkese açık olacak.</p>
  <form method="post" novalidate>
    {% csrf_token %} {% include "includes/form_fields.html" %}
    <p id="message-count" class="character-count">En fazla 100 karakter.</p>
    <div class="form-actions">
      <button type="submit" class="button">{{ button_label }}</button>
      <a href="{% url 'tweetapp:listtweet' %}">Vazgeç</a>
    </div>
  </form>
</section>
{% endblock %}
```

`heading` ve `button_label`, aynı şablonun iki işlemde kullanılmasını sağlar. `novalidate`, tarayıcının gönderimi durduran yerleşik doğrulamasını kapatır; eğitimde backend hata mesajlarını gözlemlemek için kullanıyoruz. Backend doğrulaması devam eder. HTML `maxlength` yazmayı sınırlayabilir; 101 karakter denemesini Python form testiyle de yapacağız.

### 10.5 Silme onayı

> Silme işlemini tek bir GET bağlantısıyla yapmıyoruz. Önce GET ile kullanıcıya onay ekranı gösteriliyor; gerçek silme işlemi CSRF korumalı **POST** isteğiyle yapılıyor.
>
> Burada iki koruma birlikte var:
>
> ```text
> POST zorunluluğu
> +
> tweet sahibinin request.user olması
> ```
>
> Bunlar birbirinin yerine geçmez.

**Dosya: `tweetapp/templates/tweetapp/tweet_confirm_delete.html`**

<!-- file: tweetapp/templates/tweetapp/tweet_confirm_delete.html -->

```html
{% extends "base.html" %} {% block title %}Tweeti sil · DjangoTweet{% endblock %} {% block content
%}
<section class="card form-card">
  <h1>Bu tweet silinsin mi?</h1>
  <p>Bu işlem geri alınamaz.</p>
  <blockquote class="delete-preview">{{ tweet.message }}</blockquote>
  <form method="post" action="{% url 'tweetapp:deletetweet' pk=tweet.pk %}">
    {% csrf_token %}
    <div class="form-actions">
      <button type="submit" class="button button-danger">Evet, sil</button>
      <a href="{% url 'tweetapp:listtweet' %}">Vazgeç</a>
    </div>
  </form>
</section>
{% endblock %}
```

`action`, formun nereye gönderileceğini belirtir. Diğer formlarda yazmadığımızda mevcut sayfa adresine gider. CSRF belirteci, POST sırasında Django tarafından doğrulanır.

### 10.6 Giriş

**Dosya: `templates/registration/login.html`**

<!-- file: templates/registration/login.html -->

```html
{% extends "base.html" %} {% block title %}Giriş yap · DjangoTweet{% endblock %} {% block content %}
<section class="card form-card">
  <p class="eyebrow">TEKRAR MERHABA</p>
  <h1>Giriş yap</h1>
  <p class="muted">Notlarına kaldığın yerden devam et.</p>
  <form method="post" action="{% url 'login' %}" novalidate>
    {% csrf_token %} {% include "includes/form_fields.html" %} {% if next %}<input
      type="hidden"
      name="next"
      value="{{ next }}"
    />{% endif %}
    <button type="submit" class="button">Giriş yap</button>
  </form>
  <p class="form-note">Hesabın yok mu? <a href="{% url 'tweetapp:signup' %}">Hesap oluştur</a></p>
</section>
{% endblock %}
```

Misafir `/addtweet/` sayfasını açarsa girişe `?next=/addtweet/` bilgisiyle yönlenir. Gizli alan bunu POST'a taşır. Django'nun LoginView'ı dönüş adresini güvenlik kontrolünden geçirir; kendi kodunda kontrolsüz `redirect(request.GET["next"])` yazma.

### 10.7 Kayıt

**Dosya: `templates/registration/signup.html`**

<!-- file: templates/registration/signup.html -->

```html
{% extends "base.html" %} {% block title %}Hesap oluştur · DjangoTweet{% endblock %} {% block
content %}
<section class="card form-card">
  <p class="eyebrow">İLK ADIM</p>
  <h1>Hesap oluştur</h1>
  <p class="muted">Kullanıcı adını seç ve ilk paylaşımına hazırlan.</p>
  <form method="post" novalidate>
    {% csrf_token %} {% include "includes/form_fields.html" %}
    <button type="submit" class="button">Hesap oluştur</button>
  </form>
  <p class="form-note">Hesabın var mı? <a href="{% url 'login' %}">Giriş yap</a></p>
</section>
{% endblock %}
```

Kullanıcı adının daha önce alınması, parolaların uyuşmaması veya zayıf parola gibi hataları Django formu üretir. Bu hataları frontend'de bastırmıyoruz.

<a id="css"></a>

## 11. Frontend: CSS ve küçük JavaScript desteği

> ### CSS/JavaScript'in rolünü doğru ayır
>
> CSS görünümü düzenler. JavaScript burada kullanıcı deneyimini iyileştiren karakter sayacı gibi küçük işler yapar.
>
> **Güvenlik ve asıl doğrulama JavaScript'e bırakılmaz.** Kullanıcı JS'i kapatabilir. 100 karakter sınırı ve boş mesaj kontrolü backend'deki model/form tarafından da uygulanmalıdır.

### 11.1 Tam stil dosyası

**Dosya: `tweetapp/static/tweetapp/app.css`**

<!-- file: tweetapp/static/tweetapp/app.css -->

```css
:root {
  --bg: #f3f5fa;
  --surface: #ffffff;
  --ink: #15213a;
  --muted: #56647a;
  --line: #d8dfeb;
  --primary: #244dc2;
  --danger: #ad2036;
  --radius: 18px;
}
* {
  box-sizing: border-box;
}
body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family:
    system-ui,
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    sans-serif;
  line-height: 1.6;
}
a {
  color: var(--primary);
  text-underline-offset: 3px;
}
a:hover {
  text-decoration-thickness: 2px;
}
button,
input,
textarea {
  font: inherit;
}
button {
  cursor: pointer;
}
:focus-visible {
  outline: 3px solid #bc6511;
  outline-offset: 4px;
}
.container {
  width: min(1080px, calc(100% - 40px));
  margin-inline: auto;
}
.site-header {
  background: #142039;
  color: white;
}
.nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding-block: 22px;
}
.brand {
  color: white;
  font-size: 1.5rem;
  font-weight: 800;
  text-decoration: none;
  letter-spacing: -1px;
}
.brand span {
  color: #a8bfff;
}
.nav-links {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 18px;
}
.nav-links > a {
  color: white;
  text-decoration: none;
}
.nav-user {
  color: #ccd7f1;
  overflow-wrap: anywhere;
}
.inline-form {
  display: inline;
  margin: 0;
}
.nav-button {
  border: 1px solid #8190ad;
  border-radius: 9px;
  padding: 7px 12px;
  color: white;
  background: transparent;
}
.main-content {
  min-height: 70vh;
  padding-block: 38px;
}
.hero {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 28px;
  margin-bottom: 36px;
}
h1,
h2,
h3,
p {
  margin-top: 0;
}
h1 {
  font-size: clamp(1.8rem, 4vw, 2.8rem);
  line-height: 1.15;
  letter-spacing: -1px;
  margin-bottom: 16px;
}
h2 {
  font-size: 1.25rem;
}
h3 {
  font-size: 1rem;
}
.eyebrow {
  color: var(--primary);
  font-size: 0.74rem;
  font-weight: 800;
  letter-spacing: 0.12em;
}
.muted {
  color: var(--muted);
}
.hero .muted {
  margin-bottom: 0;
}
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 1px solid transparent;
  border-radius: 10px;
  padding: 11px 18px;
  color: white;
  background: var(--primary);
  text-decoration: none;
  font-weight: 650;
  white-space: nowrap;
}
.button:hover {
  background: #1a3c9c;
}
.button-small {
  padding: 8px 13px;
}
.button-secondary {
  background: white;
  color: var(--primary);
  border-color: var(--line);
}
.button-secondary:hover {
  background: #e8edfb;
}
.button-danger {
  background: var(--danger);
}
.button-danger:hover {
  background: #88182a;
}
.feed-layout {
  display: grid;
  grid-template-columns: minmax(0, 2fr) minmax(240px, 1fr);
  gap: 28px;
  align-items: start;
}
.feed-layout > * {
  min-width: 0;
}
.section-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 16px;
}
.section-heading h2 {
  margin: 0;
}
.badge {
  border-radius: 100px;
  background: #e3eafd;
  color: #264591;
  padding: 4px 11px;
  font-size: 0.8rem;
  white-space: nowrap;
}
.card {
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 24px;
}
.tweet-card {
  margin-bottom: 16px;
}
.tweet-header {
  display: flex;
  align-items: center;
  gap: 12px;
}
.tweet-header > div {
  min-width: 0;
}
.tweet-header h3 {
  margin: 0;
  overflow-wrap: anywhere;
}
.tweet-header time {
  font-size: 0.8rem;
  color: var(--muted);
}
.avatar {
  display: grid;
  place-items: center;
  flex: 0 0 42px;
  height: 42px;
  border-radius: 13px;
  background: #e5edff;
  color: var(--primary);
  font-weight: 800;
}
.tweet-message {
  margin: 20px 0 4px;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}
.tweet-actions {
  display: flex;
  gap: 18px;
  margin-top: 18px;
  padding-top: 14px;
  border-top: 1px solid var(--line);
  font-size: 0.875rem;
}
.danger-link {
  color: var(--danger);
}
.sidebar p,
.sidebar li {
  color: var(--muted);
}
.sidebar ul {
  padding-left: 20px;
  margin-bottom: 0;
}
.sidebar li + li {
  margin-top: 10px;
}
.empty-state {
  padding-block: 44px;
  text-align: center;
}
.empty-state p {
  color: var(--muted);
}
.form-card {
  width: min(100%, 580px);
  margin: 12px auto;
  padding: 32px;
}
.form-card h1 {
  font-size: 2rem;
}
.field {
  margin-bottom: 20px;
}
.field label {
  display: block;
  font-weight: 650;
  margin-bottom: 7px;
}
.field input,
.field textarea {
  width: 100%;
  min-width: 0;
  border: 1px solid #8997af;
  border-radius: 10px;
  padding: 11px 13px;
  background: #fff;
  color: var(--ink);
}
.field textarea {
  resize: vertical;
  min-height: 140px;
}
.help-text {
  color: var(--muted);
  font-size: 0.82rem;
  margin-top: 7px;
}
.help-text ul {
  padding-left: 19px;
}
.field-errors,
.form-errors {
  color: var(--danger);
  font-size: 0.875rem;
}
.errorlist {
  padding-left: 20px;
  margin-block: 8px;
}
.character-count {
  color: var(--muted);
  text-align: right;
  font-size: 0.82rem;
}
.form-actions {
  display: flex;
  align-items: center;
  gap: 22px;
  margin-top: 22px;
}
.form-note {
  margin: 24px 0 0;
  color: var(--muted);
}
.delete-preview {
  margin: 24px 0;
  padding: 18px;
  border-left: 4px solid var(--danger);
  background: #fff1f3;
  overflow-wrap: anywhere;
  white-space: pre-wrap;
}
.notices {
  margin-bottom: 24px;
}
.notice {
  padding: 13px 18px;
  border: 1px solid #a4c7b6;
  border-radius: 10px;
  color: #17583a;
  background: #eaf6ef;
}
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-top: 28px;
}
.site-footer {
  padding-block: 24px;
  color: var(--muted);
  font-size: 0.875rem;
  border-top: 1px solid var(--line);
}
.skip-link {
  position: absolute;
  left: 12px;
  top: -100px;
  z-index: 10;
  background: white;
  padding: 12px;
}
.skip-link:focus {
  top: 12px;
}
@media (max-width: 760px) {
  .nav {
    flex-direction: column;
    align-items: flex-start;
    gap: 14px;
  }
  .nav-links {
    gap: 12px;
  }
  .hero {
    flex-direction: column;
    align-items: flex-start;
  }
  .feed-layout {
    grid-template-columns: 1fr;
  }
  .sidebar {
    order: 2;
  }
  .main-content {
    padding-top: 26px;
  }
  .form-card {
    padding: 24px;
  }
}
@media (max-width: 380px) {
  .container {
    width: calc(100% - 24px);
  }
  .card {
    padding: 18px;
  }
  .nav-links {
    font-size: 0.875rem;
  }
}
```

### 11.2 CSS'yi anlamak ve kendine göre değiştirmek

> Tasarımı öğrenirken tek seferde onlarca değeri değiştirme. Bir değişkeni değiştir → tarayıcıda sonucu gör → sonra diğerine geç. Böylece hangi CSS kuralının ne yaptığını gözlemleyebilirsin.

- `:root` değişkenleri, renkleri tek yerden değiştirmeni sağlar. Önce `--primary` ile dene.
- `.class`, HTML'de aynı class'ı taşıyan öğeleri seçer. `#id`, tekil kimliği seçer.
- `padding`, kutunun iç boşluğu; `margin`, dış boşluk; `border`, kenarlıktır.
- `box-sizing: border-box`, belirtilen genişliğe iç boşluk ve kenarlığı dahil ederek ölçüyü yönetmeyi kolaylaştırır.
- `display: flex`, menü/düğmeler gibi tek yönde dizilen öğelere uygundur.
- `display: grid`, akış ve yan panel gibi sütunlu düzen kurar.
- `minmax(0, 2fr)`, uzun metnin sütunu büyütüp taşırmasını azaltır.
- `overflow-wrap: anywhere`, uzun kullanıcı adı veya tek kelimenin ekranı taşırmasını önler.
- `white-space: pre-wrap`, mesajdaki satır sonlarını korur.
- `@media`, ekran daraldığında tasarımı tek sütuna geçirir.
- `:focus-visible`, klavyeyle hangi öğede olduğunu görünür kılar; outline'ı kaldırma.

**Frontend görevin:** Önce hazır haliyle çalıştır. Sonra yalnızca renkler, başlık metinleri ve boşluklarla kendi tasarımını yap. Django URL adlarını ve form `name` değerlerini tasarım düzenlerken değiştirme.

### 11.3 Karakter sayacı

> Sayaç, kullanıcıya anlık geri bildirim verir; fakat “100 karakteri geçemezsin” kuralının asıl sahibi değildir. Backend doğrulaması olmasa kullanıcı isteği doğrudan göndererek JavaScript'i atlayabilir.

**Dosya: `tweetapp/static/tweetapp/app.js`**

<!-- file: tweetapp/static/tweetapp/app.js -->

```javascript
document.querySelectorAll('textarea[data-count-target]').forEach((input) => {
  const output = document.getElementById(input.dataset.countTarget);
  if (!output) return;

  const update = () => {
    const count = Array.from(input.value).length;
    output.textContent = `${count} / 100 karakter`;
  };

  input.addEventListener('input', update);
  update();
});
```

Bu kod yalnızca görüntü desteğidir: veritabanına yazmaz ve sunucu doğrulamasının yerini almaz. `dataset.countTarget`, form widget'ında verdiğimiz `data-count-target` değerini okur. `Array.from`, sayımı Unicode kod noktaları üzerinden yapar; bazı birleşik emojiler birden fazla karakter sayılabilir. JavaScript kapalıyken form hâlâ çalışmalıdır.

<a id="ilk-test"></a>

## 12. İlk çalıştırma ve kullanıcı senaryoları

> ### Artık parçaları birlikte test ediyoruz
>
> Tek tek dosyaların doğru görünmesi yeterli değildir. Gerçek kullanıcı senaryosunu baştan sona denemeliyiz:
>
> ```text
> kayıt → login → ekleme → listeleme → düzenleme → silme → logout
> ```
>
> Ayrıca ikinci kullanıcıyla başkasının tweetine erişmeyi denemek, yetki kontrolünün gerçekten backend'de çalıştığını doğrular.

**Terminal — proje kökünde ve `.venv` açıkken:**

```bash
export DEBUG=True
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py runserver
```

İkinci kontrol, modelde migration'a dönüştürülmemiş değişiklik kalıp kalmadığını denetler; yeni dosya yazmaz. “No changes detected” beklenir.

[Ana sayfayı aç](http://127.0.0.1:8000/). Sunucu komutu açık kaldığı sürece terminalde başka komut yazmak için yeni terminal kullan veya önce `Ctrl+C` ile sunucuyu durdur.

### Elle kontrol listesi

- [ ] Boş listede “Henüz paylaşım yok” görünür; admin'de tweet oluşturduysan kart görünür.
- [ ] Giriş yapmadan “Yeni tweet” adresine gitmek girişe yönlendirir.
- [ ] Kayıt formu uyuşmayan/zayıf parolayı gösterir; aynı kullanıcı adını ikinci kez kabul etmez.
- [ ] Yeni hesap oluşturunca giriş sayfası gelir; giriş yapınca menüde kullanıcı adın görünür.
- [ ] Tweet eklenir ve listede doğru yazara bağlanır.
- [ ] Listeyi yenilemek aynı tweeti tekrar oluşturmaz.
- [ ] Boş mesaj gönderince form hatası görünür, yeni kayıt oluşmaz.
- [ ] Düzenleme mevcut tweeti değiştirir, ikinci bir tweet oluşturmaz.
- [ ] Sil bağlantısı önce onay sayfası açar; “Vazgeç” kayıt silmez.
- [ ] Silme onayından sonra tweet kaybolur.
- [ ] Çıkış düğmesi çalışır; çıkınca korumalı sayfalar giriş ister.
- [ ] İkinci kullanıcı birincinin tweetini görebilir ama düzenleyemez/silemez.
- [ ] Tarayıcıyı 375 px genişliğe indirince yatay taşma olmaz; Tab tuşuyla düğmelere ulaşılır.
- [ ] 11 tweetten sonra sayfalama görünür.

İki kullanıcı kontrolü için normal pencere ve gizli pencere kullanabilirsin. Başkasının tweetine ait `/tweets/ID/edit/` adresini elle açmayı da dene: **404** beklenir. Düğmenin görünmemesi tek başına yeterli test değildir.

### Hangi veri nerede?

Kullanıcılar, parolaların hash'leri, tweetler ve oturum kayıtları SQLite veritabanında tutulur. Tarayıcıya parola kaydını göndermeyiz. Tarayıcı genellikle oturum kimliğini cookie'de taşır. `SECRET_KEY` kullanıcı giriş parolası değildir.

<a id="akis"></a>

## 13. Kod akışını adım adım takip etmek

> ### Bu bölüm öğrenme açısından en önemli bölümlerden biri
>
> Buraya kadar “hangi dosyaya ne yazılır?” gördün. Şimdi bir butona basıldığında sistemin **hangi sırayla hareket ettiğini** takip edeceğiz.
>
> Bir Django projesini gerçekten anlamanın en iyi yolu, tek bir isteği URL'den başlayıp response'a kadar izleyebilmektir.

### “Paylaş” düğmesine bastığında

1. Tarayıcı `/addtweet/` adresine POST gönderir. Form verisinde `message` ve CSRF belirteci vardır.
2. `djangotweet/urls.py`, yolu `tweetapp.urls` dosyasına devreder.
3. `tweetapp/urls.py`, `addtweet` view'ını seçer.
4. Middleware oturumu ve CSRF koşullarını işler; `login_required` kullanıcı girişini kontrol eder.
5. `TweetForm(request.POST)` alanları alır, `is_valid()` kuralları çalıştırır.
6. Geçersizse aynı form hataları ve verileriyle HTML olarak döner. Veritabanına yazılmaz.
7. Geçerliyse `commit=False` ile Tweet hazırlanır, yazar `request.user` olur, `save()` kaydı oluşturur.
8. `redirect` 302 yanıtı döndürür; tarayıcı `/` için yeni GET gönderir.
9. Liste view'ı kayıtları okur; şablon kartları oluşturur; tarayıcı HTML'i gösterir.

Bu akış **POST → redirect → GET** desenidir. Sayfa yenilendiğinde POST'un tekrar gönderilmesi riskini azaltır.

### Django şablonu tarayıcıya aynen gider mi?

Hayır. `{% for %}`, `{% url %}` ve `{{ tweet.message }}` sunucuda işlenir. Tarayıcı ortaya çıkan HTML'i alır. CSS ve JavaScript ayrı HTTP istekleriyle gelir. Tarayıcıda “Sayfa kaynağını görüntüle” ile bunu gözlemleyebilirsin.

### Küçük Python okuma rehberi

| Sözdizimi                   | Bu projede anlamı                                             |
| --------------------------- | ------------------------------------------------------------- |
| `from .models import Tweet` | Aynı uygulamanın models modülünden Tweet'i al.                |
| `{"form": form}`            | Şablona `form` adıyla nesne gönderen sözlük.                  |
| `@login_required`           | Altındaki fonksiyona giriş kontrolü ekleyen dekoratör.        |
| `return`                    | Fonksiyonu bu yanıtla bitir. Her olası istekte yanıt dönmeli. |
| `class Meta`                | Django'nun form/model hakkında okuyacağı yapılandırma.        |
| `pk=pk`                     | Solda fonksiyonun parametre adı, sağda view'a gelen değer.    |
| `request.GET.get("page")`   | Sorgu parametresi; URL'deki `?page=2` için `"2"` gelir.       |
| `request.POST`              | Form gönderiminin alan-değer verileri.                        |

<a id="form-karsilastirma"></a>

## 14. Elle HTML, Form ve ModelForm karşılaştırması

> ### Neden üç farklı yaklaşımı karşılaştırıyoruz?
>
> Django'da aynı sonucu farklı seviyelerde elle veya framework desteğiyle üretebilirsin. Ama neyi Django'nun yaptığı, neyi senin yaptığın net olmazsa `ModelForm` sihirli bir kutu gibi görünür.
>
> Bu bölüm sana:
>
> ```text
> raw POST
> forms.Form
> forms.ModelForm
> ```
>
> arasındaki sorumluluk farkını gösterir. Ana projede ModelForm kullanıyoruz; diğerlerini kavramı anlamak için inceliyoruz.

Eski eğitimde üç ayrı tweet ekleme yolu vardı. Yeni temel sürümde tek güvenilir akışla başladık. Üç yaklaşımın farkını aşağıdaki deneyle öğrenebilirsin; ana dosyaları değiştirmek zorunda değilsin.

| Yaklaşım                | Doğrulama nerede?                              | Kayıt nasıl yapılır?                              |
| ----------------------- | ---------------------------------------------- | ------------------------------------------------- |
| Elle HTML ve POST okuma | Kuralları backend'de sen yazarsın.             | `Tweet.objects.create(...)` gibi açık kayıt.      |
| `forms.Form`            | Alan kuralları ve `clean_...` metotları.       | Doğrulanan `cleaned_data` ile açık kayıt.         |
| `forms.ModelForm`       | Modelden türeyen kurallar + ek form kuralları. | `form.save()`; sahiplik için önce `commit=False`. |

Elle HTML'de `<input name="message">` gönderirsen `request.POST` anahtarı `message` olur. `id`, label'ın hangi alanı gösterdiğini belirtir; gönderilen verinin anahtarını `name` belirler. `request.POST["message"]` eksik alanda hata verir; `.get("message", "")` eksik değeri ele alır ama tek başına doğrulama yapmaz.

**Terminal:** `python manage.py shell`

**Python kabuğu deneyi — ana projeye dosya olarak ekleme:**

```python
from django import forms

class PlainTweetForm(forms.Form):
    message_input = forms.CharField(max_length=100, strip=True)

plain = PlainTweetForm({"message_input": "  Merhaba  "})
plain.is_valid()
plain.cleaned_data["message_input"]
exit()
```

`is_valid()` `True`, temizlenen değer `Merhaba` olur. Form alanı `message_input` olduğu için `cleaned_data["message"]` yazmak hatadır. Kaydetmek isteseydik temizlenen bu değeri modelin **`message`** alanına eşler, yazarı yine oturumdan alırdık. Form alanının adı ve model alanının adı ancak bu eşlemeyi doğru yaparsan farklı olabilir.

**Neden ana akışta ModelForm?** Mesaj sınırını hem modelde hem normal formda ayrı ayrı güncellemek zorunda kalmamak için. Bunun karşılığında hangi model alanlarının kullanıcıya açıldığını `fields` ile bilinçli seçmelisin.

<a id="testler"></a>

## 15. Otomatik testler

> ### Test neden gerekli?
>
> Tarayıcıda bir kez tıklayıp “çalışıyor” demek, tüm durumların çalıştığını kanıtlamaz. Kod değiştikçe daha önce çalışan bir özellik fark etmeden bozulabilir.
>
> Otomatik testler özellikle şunları tekrar tekrar doğrular:
>
> - sayfalar açılıyor mu,
> - form kuralları çalışıyor mu,
> - giriş zorunluluğu uygulanıyor mu,
> - kullanıcı yalnızca kendi tweetini değiştirebiliyor mu,
> - silme GET ile yapılamıyor mu,
> - CSRF gibi kritik davranışlar korunuyor mu.
>
> Testin geçmesi “hiç hata yok” anlamına gelmez; ama önemli davranışların değişmediğine dair güçlü bir güvenlik ağı sağlar.

Elle deneme görünümü anlamana yardımcı olur. Otomatik testler ise kodu değiştirdiğinde özellikle **kayıt sahipliği, giriş zorunluluğu ve silme yöntemi** gibi kuralların bozulduğunu yakalar.

**Dosya: `tweetapp/tests.py`**

<!-- file: tweetapp/tests.py -->

```python
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .forms import TweetForm
from .models import Tweet


class TweetFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.owner = User.objects.create_user("owner", password="Study-Test-928!")
        cls.other = User.objects.create_user("other", password="Study-Test-928!")
        cls.tweet = Tweet.objects.create(author=cls.owner, message="İlk not")

    def test_home_is_public_and_escapes_html(self):
        self.tweet.message = "<script>alert(1)</script>"
        self.tweet.save()
        response = self.client.get(reverse("tweetapp:listtweet"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "&lt;script&gt;")
        self.assertNotContains(response, "<script>alert(1)</script>")

    def test_anonymous_cannot_create(self):
        response = self.client.post(reverse("tweetapp:addtweet"), {"message": "Deneme"})
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        self.assertEqual(Tweet.objects.count(), 1)

    def test_author_cannot_be_forged(self):
        self.client.force_login(self.owner)
        response = self.client.post(
            reverse("tweetapp:addtweet"),
            {"message": "Yeni not", "author": self.other.pk},
        )
        self.assertRedirects(response, reverse("tweetapp:listtweet"))
        self.assertEqual(Tweet.objects.get(message="Yeni not").author, self.owner)

    def test_message_boundaries(self):
        for value in ("", "   ", "a" * 101):
            with self.subTest(value=value):
                self.assertFalse(TweetForm({"message": value}).is_valid())
        self.assertTrue(TweetForm({"message": "a" * 100}).is_valid())

    def test_invalid_post_displays_errors_without_saving(self):
        self.client.force_login(self.owner)
        response = self.client.post(reverse("tweetapp:addtweet"), {"message": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Boş tweet gönderemezsin.")
        self.assertEqual(Tweet.objects.count(), 1)

    def test_owner_can_edit_without_creating_another_tweet(self):
        self.client.force_login(self.owner)
        url = reverse("tweetapp:edittweet", args=[self.tweet.pk])
        response = self.client.post(url, {"message": "Güncellendi"})
        self.assertEqual(response.status_code, 302)
        self.tweet.refresh_from_db()
        self.assertEqual(self.tweet.message, "Güncellendi")
        self.assertEqual(Tweet.objects.count(), 1)

    def test_other_user_cannot_edit_or_delete(self):
        self.client.force_login(self.other)
        for name in ("edittweet", "deletetweet"):
            with self.subTest(name=name):
                url = reverse(f"tweetapp:{name}", args=[self.tweet.pk])
                response = self.client.post(url, {"message": "İzinsiz"})
                self.assertEqual(response.status_code, 404)
        self.tweet.refresh_from_db()
        self.assertEqual(self.tweet.message, "İlk not")

    def test_delete_confirmation_and_get_do_not_delete(self):
        self.client.force_login(self.owner)
        confirm = reverse("tweetapp:confirm_delete", args=[self.tweet.pk])
        delete = reverse("tweetapp:deletetweet", args=[self.tweet.pk])
        self.assertEqual(self.client.get(confirm).status_code, 200)
        self.assertEqual(self.client.get(delete).status_code, 405)
        self.assertTrue(Tweet.objects.filter(pk=self.tweet.pk).exists())

    def test_owner_can_delete_with_post(self):
        self.client.force_login(self.owner)
        url = reverse("tweetapp:deletetweet", args=[self.tweet.pk])
        self.assertEqual(self.client.post(url).status_code, 302)
        self.assertFalse(Tweet.objects.filter(pk=self.tweet.pk).exists())

    def test_csrf_is_required_for_delete(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.owner)
        url = reverse("tweetapp:deletetweet", args=[self.tweet.pk])
        self.assertEqual(client.post(url).status_code, 403)
        self.assertTrue(Tweet.objects.filter(pk=self.tweet.pk).exists())

    def test_signup_login_and_post_logout(self):
        password = "Study-New-User-827!"
        response = self.client.post(reverse("tweetapp:signup"), {
            "username": "learner",
            "password1": password,
            "password2": password,
        })
        self.assertRedirects(response, reverse("login"))
        response = self.client.post(reverse("login"), {
            "username": "learner", "password": password,
        })
        self.assertRedirects(response, reverse("tweetapp:listtweet"))
        self.assertIn("_auth_user_id", self.client.session)
        self.assertEqual(self.client.get(reverse("logout")).status_code, 405)
        self.client.post(reverse("logout"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_pagination(self):
        Tweet.objects.bulk_create([
            Tweet(author=self.owner, message=f"Not {number}")
            for number in range(10)
        ])
        response = self.client.get(reverse("tweetapp:listtweet"))
        self.assertEqual(len(response.context["page_obj"]), 10)
        response = self.client.get(reverse("tweetapp:listtweet"), {"page": 2})
        self.assertEqual(len(response.context["page_obj"]), 1)
```

**Terminal:**

```bash
python manage.py collectstatic --noinput
python manage.py test tweetapp
```

Bu testler için `collectstatic` çalıştırıyoruz çünkü test çalıştırıcısı `DEBUG=False` kullanır ve manifest tabanlı statik depolama, şablonları render ederken dosya manifestini arar. Normal `DEBUG=True` geliştirmesinde her CSS değişiminde collectstatic gerekmez.

Beklenti: **12 test, OK**. `TestCase`, ayrı test veritabanı kullanır; mevcut yerel kullanıcılarını silmez. Testteki parolalar yalnızca geçici test kullanıcıları içindir. `force_login`, çoğu testte giriş ekranını atlayarak doğrudan yetki kuralını denememizi sağlar; ayrıca gerçek kayıt/giriş akışı için ayrı test vardır.

Varsayılan Django test istemcisi CSRF denetimini atlar. Bu nedenle silme testi için özel `Client(enforce_csrf_checks=True)` oluşturduk. Test başarısı tüm olası hataların olmadığını kanıtlamaz; mobil görüntüyü ve Render ortamını ayrıca kontrol ederiz.

<a id="git"></a>

## 16. Git ve GitHub

> ### Burada üç kavramı birbirinden ayır
>
> ```text
> Git       = bilgisayarındaki sürüm geçmişi
> GitHub    = uzak depo
> Render    = kodun çalışan yayını
> ```
>
> `git add`, `git commit` ve `git push` aynı şey değildir. Özellikle `git push`, çalışma klasöründeki her değişikliği otomatik olarak göndermez; yalnızca commit edilmiş geçmişi uzak depoya taşır.

### 16.1 Kavramları ayır

> Bu akışta her okun ayrı bir anlamı var. Bir dosyayı kaydetmek commit değildir; commit etmek push değildir; GitHub'a push etmek de tek başına tarayıcıdaki canlı uygulamanın güncellendiği anlamına gelmez.

```text
Dosyada değişiklik
       ↓ git add
Bir sonraki kayda seçilmiş değişiklik
       ↓ git commit
Bilgisayarındaki Git geçmişi
       ↓ git push
GitHub'daki uzak depo
       ↓ Render deploy
Yayındaki uygulama
```

**`git push`, commit edilmemiş dosyaları göndermez.** `Everything up-to-date`, gönderilecek yeni commit olmadığını söyler; bütün dosyalarının kaydedildiğini söylemez.

### 16.2 Yeni proje için ayrı depo oluştur

Yeni çalışma kökünde:

```bash
git init
git branch -M main
git status
```

Git kimliğin tanımlı değilse, **gerçek adını ve tercih ettiğin GitHub e-postanı yazarak** bu iki komutu çalıştır. Örnek metinleri olduğu gibi bırakma:

```bash
git config user.name "ADIN SOYADIN"
git config user.email "GITHUB_EPOSTAN"
```

Sadece bu yeni depoda geçerlidir. GitHub'da profil ayarlarından gizli `noreply` e-postanı da kullanabilirsin.

```bash
git add .
git diff --cached --stat
git status
git commit -m "Build DjangoTweet practice app"
```

`git add .` burada yeni ve yalnızca bu projeye ait depoda kullanılıyor. Commit öncesinde `.venv`, `db.sqlite3`, `.env` ve `staticfiles` listede olmamalı. Yanlışlıkla seçilmiş bir dosyayı silmeden seçimden çıkarmak için sonraki commit'lerde `git restore --staged DOSYA` kullanılır. İlk commit öncesinde gerekirse `git rm --cached DOSYA` kullan; dosya diskte kalır.

GitHub'da **New repository** ile `DjangoTweetPractice` isimli boş depo oluştur. README/license/gitignore ekleme seçeneklerini işaretleme; dosyaların zaten yerelde. Oluşturulan sayfadan HTTPS depo URL'sini kopyala.

**Aşağıdaki `KULLANICI_ADIN` yerini kendi adınla değiştir:**

```bash
git remote add origin https://github.com/KULLANICI_ADIN/DjangoTweetPractice.git
git remote -v
git push -u origin main
```

`origin`, uzak deponun kısa adı. `-u`, yerel main ile uzak main arasındaki takip ilişkisini kurar. Sonraki gönderimlerde `git push` yeterlidir. GitHub oturum doğrulaması isterse Git Credential Manager/VS Code girişini kullan; HTTPS Git işlemleri normal hesap parolanı kabul etmez. Gerekirse GitHub'ın token veya SSH yöntemini kur; tokenı dosyaya veya README'ye yazma.

Başarı kontrolü: GitHub sayfasında `manage.py`, migration dosyaları, `requirements.txt` ve kodların görünmeli. `git status` temiz olmalı. `git log -1 --oneline` son kaydı gösterir. README'yi yeni projeye kopyaladıysan o da depoda bulunur.

### 16.3 Sonraki değişikliklerde

```bash
git status
git diff
git add .
git diff --cached --stat
git commit -m "Explain the change here"
git push
```

Commit mesajını gerçekte yaptığın değişiklikle değiştir. `git diff` içeriğinde gizli değer olabileceği için çıktıyı kontrol etmeden paylaşma. Uzak depo değişmişse `push rejected` alınabilir; hatayı okuyup önce uzak değişiklikleri incele. `--force` ile ezme.

<a id="yayin-mantigi"></a>

## 17. Yayın ayarlarını anlamak

> ### Yerelde çalışan proje neden doğrudan yayına çıkmıyor?
>
> Yerel geliştirmede hata mesajlarını görmek, localhost'tan bağlanmak ve basit HTTP kullanmak normaldir. İnternete açık sunucuda ise güvenlik, host kontrolü, HTTPS ve statik dosya sunumu farklı ele alınır.
>
> Bu yüzden yayın ayarlarını “Render için ezberlenen birkaç satır” olarak değil, **yerel ortam ile production ortamı arasındaki farklar** olarak öğren.

### Yerel bilgisayar ve sunucu

`runserver`, geliştirme sunucusudur. Terminalde durdurduğunda yerel site kapanır. Render kendi makinesinde uygulamayı çalıştırır; bilgisayarın kapalı olsa da yayın devam eder.

**Build**, paketleri ve yayın dosyalarını hazırlar. **Start**, hazır uygulamayı istek karşılamak üzere başlatır. Bunlar aynı işlem değildir.

### SECRET_KEY tam olarak nereye yazılır?

> `SECRET_KEY` kaynak koda gömülmemesi gereken bir uygulama sırrıdır. GitHub'a commit etmek yerine ortam değişkeni olarak veriyoruz. Böylece kod paylaşılabilir, gizli değer paylaşılmaz.

Yerelde yeni bir yayın anahtarı üret:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Çıktıyı `settings.py` içine yapıştırma. Render'ın **Environment Variables** bölümünde:

| Key          | Value                                                 |
| ------------ | ----------------------------------------------------- |
| `SECRET_KEY` | Ürettiğin anahtarın tamamı; etrafına ek tırnak koyma. |

Terminalde üretmek Render'a otomatik kaydetmez. Panelde değeri sen eklersin. Kodda `os.environ.get("SECRET_KEY")`, bu isimle tanımlanan ortam değerini okur. Render'daki Generate seçeneğiyle de değer üretilebilir; iki yöntemden biri yeterlidir. Yayın anahtarını kullanıcılarla paylaşma veya her deploy'da değiştirme; değiştirmek mevcut imzalı değerleri ve oturumları etkileyebilir.

### DEBUG ve host kontrolü

> `DEBUG=False` hataları çözmez; yalnızca production ortamında ayrıntılı hata ekranlarını kullanıcıya göstermememizi sağlar. `ALLOWED_HOSTS` ise Django'nun hangi host adlarıyla gelen isteklere cevap vereceğini sınırlar.

Render'da `DEBUG=False` kullan. `DEBUG` hatayı düzeltmez; teknik hata ayrıntılarının ziyaretçiye gösterilmesini belirler. Ayrıntıları sunucu loglarından inceleriz.

`ALLOWED_HOSTS` içine URL'nin tamamı değil **host adı** yazılır: `ornek.onrender.com`. `https://` ve `/` eklenmez. Yukarıdaki settings, Render'ın `RENDER_EXTERNAL_HOSTNAME` değişkenini otomatik alır. Özel domain eklersen panelde `ALLOWED_HOSTS=example.com,www.example.com` verebilirsin. Gelişigüzel `*` ekleyerek host kontrolünü kapatma.

### Statik dosyalar neden ayrı hazırlanıyor?

> Geliştirme sunucusu CSS/JS'yi kolaylık için otomatik sunabilir. Production ortamında bu davranışa güvenmeyiz. `collectstatic`, farklı uygulamalardaki statik dosyaları yayın için belirlenen ortak hedefe toplar; WhiteNoise da bunların sunulmasına yardımcı olur.

Geliştirmede Django kaynak statik dosyaları bulup sunabilir. Yayında `collectstatic`, uygulamaların statik dosyalarını `STATIC_ROOT` altına toplar. WhiteNoise bunları sunar; manifest depolama dosya adına içerik özeti ekleyerek güncel CSS'nin önbellekle karışmasını azaltır. `staticfiles/` içindeki üretilmiş dosyayı elle düzenleme; kaynak dosyayı düzenleyip yeniden topla.

### Yerelde yayın davranışını dene

Bu komutlarda `$()` bir komutun çıktısını ortam değişkenine atar; yalnızca aşağıdaki sabit anahtar üretme komutunu çalıştırır:

```bash
export SECRET_KEY="$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
DEBUG=False python manage.py collectstatic --noinput
DEBUG=False python manage.py check --deploy
DEBUG=False gunicorn djangotweet.wsgi:application --bind 127.0.0.1:8000
```

Yerelde Render algılanmadığı için HTTPS zorlaması ve secure cookie ayarları açılmaz; bu nedenle `check --deploy` burada bunlara ve HSTS'ye dair uyarılar verebilir. Render ortamında ise HTTPS/cookie ayarları açılır; HSTS canlı domain davranışı doğrulandıktan sonra ayrıca planlanır. Uyarıları susturmak için rastgele ayar ekleme.

Ana sayfa, giriş ve CSS'yi kontrol et. `Ctrl+C` ile Gunicorn'u durdur; istersen test anahtarını terminalden `unset SECRET_KEY` ile kaldır. `export DEBUG=True` yerel geliştirmeye dönüş içindir.

<a id="render"></a>

## 18. Render'da ücretsiz deneme yayını

> ### Bu bölümün amacı “deploy” kavramını öğrenmek
>
> Artık yerelde çalışan ve GitHub'a gönderilmiş bir uygulamayı internetten erişilebilir hale getireceğiz.
>
> Burada şu zinciri izle:
>
> ```text
> GitHub'daki commit
>       ↓
> Render build
>       ↓
> paket kurulumu
>       ↓
> collectstatic / migrate
>       ↓
> Gunicorn uygulamayı başlatır
>       ↓
> canlı URL
> ```
>
> Render ayarlarını körü körüne kopyalamak yerine build ile start komutunun neden ayrı olduğunu anlamaya çalış.

### 18.1 Önce veritabanı kararını ver

> **Bu uyarı önemlidir.**
> SQLite dosyası yerel öğrenme için çok uygundur; ancak ücretsiz ve geçici dosya sistemine sahip bir cloud serviste kalıcı üretim verisi için güvenilir değildir. Bu rehberdeki Render bölümü bir **öğrenme/demonstrasyon yayınıdır**.
>
> Gerçek, kalıcı kullanıcı verisi gereken uygulamada PostgreSQL gibi kalıcı bir veritabanı mimarisi planlanmalıdır.

Bu bölüm **kişisel deneme yayını** için SQLite kullanır. `db.sqlite3` GitHub'a gitmediğinden yerel hesaplar/tweetler Render'a taşınmaz. Render'ın geçici dosya sisteminde kayıtlar yeniden deploy, yeniden başlatma ve ücretsiz servisin kapanıp yeniden başlaması sırasında kaybolabilir. Bu yüzden bu yol gerçek kullanıcı verilerinin kalıcı tutulacağı bir kurulum değildir. [Render ücretsiz servis sınırları](https://render.com/docs/free).

Kalıcı kullanıma geçerken harici PostgreSQL, bağlantı bilgileri, migration adımı ve yedekleme planı gerekir. Yerel SQLite kayıtlarının taşınması ayrıca veri aktarımıdır; veritabanı adresini değiştirmek kayıtları kendiliğinden kopyalamaz. Ücretsiz web servisine kalıcı disk eklenemez. PostgreSQL kurulumunu bu temel örneğin zorunlu adımı yapmıyoruz; eksik bağlantı bilgisiyle yarım bir yapılandırma eklemiyoruz.

### 18.2 Render formunu doldur

1. Render hesabına gir, **New → Web Service** seç.
2. GitHub hesabını bağla ve **yeni `DjangoTweetPractice` deposunu** seç.
3. Aşağıdaki alanları doldur. Yeni proje için Root Directory, eski eğitim projesinden farklıdır.

| Alan           | Yeni çalışma projesindeki değer                      | Neden?                                                       |
| -------------- | ---------------------------------------------------- | ------------------------------------------------------------ |
| Name           | Uygun bir servis adı, örneğin `djangotweet-practice` | URL için kullanılabilir bir ad gerekir; ad doluysa değiştir. |
| Language       | Python 3                                             | Uygulama Python kullanıyor.                                  |
| Branch         | main                                                 | Gönderdiğin kodun dalı.                                      |
| Region         | Sana/kullanıcılarına uygun bir bölge                 | Veritabanı eklenirse mümkünse aynı bölgeyi seç.              |
| Root Directory | **Boş bırak**                                        | Yeni depoda manage.py doğrudan kökte.                        |
| Compute        | Free                                                 | Bu bölüm deneme amaçlı ücretsiz web servisi içindir.         |

**Eski depo ile yeni depoyu ayır:** Eski `Django-Egitimi` deposunu seçersen Root Directory `DjangoTweet/djangotweet` idi. Bu rehberdeki yeni `DjangoTweetPractice` deposunda o yolu yazarsan klasör bulunamaz.

**Build Command — yalnızca SQLite deneme yolu:**

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput
```

Paketleri kurar → statikleri toplar → boş SQLite dosyasında tabloları oluşturur. `&&`, önceki komut başarısızsa devam etmez. `--noinput`, sunucuda etkileşimli soru beklenmesini önler. Bu SQLite yaklaşımında migration'ı build'e eklemek ilk sayfanın “no such table” hatası vermesini önler; **kalıcı veri sağlamaz**. Kalıcı PostgreSQL'e geçince migration'ın doğru veritabanına kontrollü uygulanacağı ayrı yayın adımını planla. Ücretli planların pre-deploy komutunu ücretsiz planda varmış gibi varsayma.

**Start Command:**

```bash
gunicorn djangotweet.wsgi:application --bind 0.0.0.0:$PORT
```

`djangotweet.wsgi`, `djangotweet/wsgi.py` modülüdür. `application`, o dosyadaki WSGI nesnesidir. `0.0.0.0`, sunucunun ağ arayüzlerinden gelen istekleri kabul eder. `$PORT`, Render'ın sağladığı port değeridir; kendi kafana göre sabit 8000 yazmıyoruz.

Komut alanlarının solunda Render'ın gösterdiği `klasör/ $` öneki komutun parçası değildir. Komutları `pip` ve `gunicorn` sözcüklerinden başlayarak gir.

### 18.3 Environment Variables

> Ortam değişkenlerini “Render'a yazılan rastgele ayarlar” olarak düşünme. Bunlar kod ile ortama özel bilgiyi ayırır:
>
> ```text
> kaynak kod        → GitHub'da olabilir
> SECRET_KEY vb.    → ortamda tutulur
> ```
>
> Böylece aynı kod yerelde ve sunucuda farklı güvenlik/çalışma değerleriyle çalışabilir.

| Key                        | Value                                     | Kim verir?                                          |
| -------------------------- | ----------------------------------------- | --------------------------------------------------- |
| `SECRET_KEY`               | Yeni üretilmiş gizli anahtar              | Sen eklersin; örnek geliştirme anahtarını kullanma. |
| `DEBUG`                    | `False`                                   | Sen eklersin.                                       |
| `PYTHON_VERSION`           | `3.12.14`                                 | Sen eklersin; bu rehberin doğrulandığı sürüm.       |
| `ALLOWED_HOSTS`            | Özel domain varsa virgülle ayrılmış adlar | İsteğe bağlı.                                       |
| `RENDER_EXTERNAL_HOSTNAME` | Servisin Render host adı                  | Render sağlar, elle yazman gerekmez.                |
| `RENDER` / `PORT`          | Render ortamı / port                      | Render sağlar.                                      |

Render'da Python sürümü ortam değişkeniyle belirlenirken tam `major.minor.patch` değeri kullanılır. [Render Python sürümü](https://render.com/docs/python-version). Daha sonraki tarihte çalışıyorsan mevcut Python 3.12 güvenlik yamasını kontrol edip hem yerelde hem sunucuda doğrula; sürüm değiştirip test etmeden yayınlama.

### 18.4 Yayından önce son kontrol

- [ ] Yeni depoda kod, `requirements.txt` ve migration dosyaları var.
- [ ] `python manage.py check` ve testler başarılı.
- [ ] GitHub'daki son commit doğru; sadece yerel dosyayı değiştirmekle kalmadın.
- [ ] Root Directory yeni depo düzenine uygun.
- [ ] Build/Start komutları ve Environment değerleri yazıldı.
- [ ] SQLite kayıtlarının geçici olduğunu kabul ediyorsun.

Artık **Deploy web service** düğmesine bas. Build loglarında paket kurulumu, collectstatic ve migration sonuçlarını izle. Durum `Live` olunca Render'ın verdiği URL'yi aç; URL'yi örnek servis adına bakarak tahmin etme.

### 18.5 Canlı kontrol

Yeni bir kullanıcı oluştur, giriş yap, tweet ekle, düzenle ve sil. Başka kullanıcıyla yetki kontrolünü dene. CSS ve admin giriş sayfası da açılmalı. Bu yeni veritabanında yereldeki superuser yoktur; normal kayıt formuyla açılan hesap admin değildir.

Ücretsiz serviste Shell/SSH gibi olanakların bulunacağını varsayma; bu deneme için otomatik superuser veya kodda sabit admin parolası eklemiyoruz. İleride kalıcı veritabanı ve yönetim erişimi planlanır.

İlk istek bir süre bekletebilir; ücretsiz servis hareketsizken durabilir. Loglarda `/favicon.ico` için 404 görmek, ana sayfanın bozuk olduğu anlamına gelmez; bu örnek özel sekme ikonu sağlamaz. Ana sayfa için 200, yönlendirme için 302, eksik sayfa için 404 normal olabilir; 500 uygulama hatasıdır.

Yeni kod gönderdiğinde otomatik deploy açıksa `git push` yayını tetikler. **Kodun değişmesi, tarayıcının yenilenmesi ve sunucunun yeniden deploy edilmesi farklı şeylerdir.**

<a id="durdurma"></a>

## 19. Yayını durdurmak ve yeniden açmak

> ### Suspend ile Delete aynı şey değildir
>
> Suspend çalışan servisi durdurur; kodu veya GitHub deposunu silmez. Delete ise servis yapılandırmasını kaldırır. Sadece deneme yayınını geçici olarak kapatmak istiyorsan “silmek” yerine askıya alma mantığını kullan.

Render'da ilgili web servisini aç → **Settings → Delete or suspend → Suspend Web Service** → onayı tamamla. Durumun askıya alındığını panelden doğrula. Menü adları zamanla değişirse Settings altındaki askıya alma seçeneğini bul.

`Suspend`, servisi askıya alır; `Delete`, servis yapılandırmasını kaldırma işlemidir. Sadece yayını durdurmak için silme seçeneğini kullanma. GitHub'daki kodun ve bilgisayarındaki çalışma klasörün askıya almadan etkilenmez.

Yeniden açmak için servisin **Resume** seçeneğini kullan. Bu SQLite düzeninde yeniden açınca önceki deneme verilerinin kalacağını varsayma. Sadece tarayıcı sekmesini veya bilgisayarı kapatmak Render yayınını durdurmaz. Sadece Auto-Deploy'u kapatmak da çalışan siteyi kapatmaz; yeni commit'lerden otomatik yayın yapılmasını engeller.

<a id="devam"></a>

## 20. Ertesi gün devam etmek

> ### En sık yapılan başlangıç hatası
>
> Yeni terminal açınca projeyi yeniden oluşturmuyorsun. `startproject`, `startapp` ve `venv` oluşturma işlemleri ilk kurulum içindir.
>
> Sonraki gün normal akış:
>
> ```text
> proje klasörüne git
>       ↓
> .venv'i aktive et
>       ↓
> gerekli ortam değişkenini ayarla
>       ↓
> check / runserver
> ```

Yeni terminal açtığında **tekrar startproject, startapp veya venv oluşturma**. Var olan çalışmana dön:

```bash
cd "/Users/omerfarukiris/Desktop/Yazılım/Projeler/DjangoTweetPractice"
source .venv/bin/activate
export DEBUG=True
python manage.py check
python manage.py runserver
```

Yeni bilgisayara geçersen depoyu klonla, Python 3.12 ile yeni `.venv` oluştur, etkinleştir, `python -m pip install -r requirements.txt`, `export DEBUG=True` ve `python manage.py migrate` çalıştır. Kaynak kod gelir; Git dışında bıraktığımız eski SQLite kayıtları gelmez.

| Değişiklik         | Gerekli işlem                                                                                          |
| ------------------ | ------------------------------------------------------------------------------------------------------ |
| HTML/CSS           | Yerelde sayfayı yenile; yayında commit/push ve yeni build.                                             |
| Model alanı        | `makemigrations`, `migrate`, test; migration dosyasını da commit et.                                   |
| Yeni Python paketi | Temiz proje ortamına kur, `pip freeze > requirements.txt`, test et, dosyayı commit et.                 |
| Ortam değişkeni    | Yerelde terminalde, Render'da Environment alanında değiştir; sunucunun yeni değerle başlaması gerekir. |
| Tweet verisi       | Uygulamanın veritabanına yazılır; Git commit değildir.                                                 |

Frontend öğrenirken önce bir değişiklik yap: örneğin `--primary` rengini değiştir. Gözlemle, sonra bir sonraki değişikliğe geç. On dosyayı birden değiştirip hatanın kaynağını kaybetme.

<a id="hatalar"></a>

## 21. Hata çözme tablosu

> ### Hata çözme yaklaşımı
>
> Hata görünce tüm dosyayı değiştirmek yerine şu sırayı kullan:
>
> ```text
> hata türünü oku
>      ↓
> traceback'te kendi dosyanı bul
>      ↓
> ilgili satırı incele
>      ↓
> son yaptığın değişikliği düşün
>      ↓
> tek düzeltme yap
>      ↓
> tekrar dene
> ```
>
> Hata mesajı çoğu zaman problemin kendisini veya en azından hangi katmanda olduğunu söyler.

| Belirti                                | Olası sebep                                                    | Kontrol / çözüm                                                                             |
| -------------------------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `python3.12: command not found`        | Python kurulu değil veya PATH'te değil.                        | Python kurulumunu doğrula; bu makinede `/opt/homebrew/bin/python3.12 --version` dene.       |
| `No module named django`               | Yanlış yorumlayıcı/sanal ortam.                                | `source .venv/bin/activate`, `python -m pip --version`, paket kurulumu.                     |
| Django 5.2 Python 3.9 ile kurulmuyor   | Eski eğitim ortamındasın.                                      | Yeni `.venv` oluştururken `python3.12` kullandığından emin ol.                              |
| `can't open file manage.py`            | Yanlış klasör.                                                 | `pwd` ve `ls`; bu rehberde manage.py proje kökünde.                                         |
| `SECRET_KEY ortam değişkenini tanımla` | DEBUG varsayılan False ve anahtar yok.                         | Yerelde `export DEBUG=True`; Render'da gerçek SECRET_KEY ekle.                              |
| `no such table`                        | Migration uygulanmamış veya yanlış DB.                         | `python manage.py showmigrations`, sonra `migrate`; Render demo Build Command'i kontrol et. |
| `No changes detected`                  | Yeni model farkı yok.                                          | Hata değildir; mevcut migration'ı `migrate` ile uygula.                                     |
| Model değişti ama kolon yok            | `makemigrations` ile `migrate` karıştırılmış.                  | İkisini sırayla çalıştır, doğru veritabanında olduğunu kontrol et.                          |
| `TemplateDoesNotExist`                 | Dosya yolu/TEMPLATES yanlış.                                   | Bu rehberin dosya haritasıyla karşılaştır; dosyayı kaydet.                                  |
| `NoReverseMatch`                       | URL adı, namespace veya pk eksik.                              | `tweetapp:edittweet` ve `pk=tweet.pk` eşleşmesini kontrol et.                               |
| CSS yok                                | Kaynak yolu yanlış veya build eksik.                           | `python manage.py findstatic tweetapp/app.css`; DEBUG=False ise collectstatic.              |
| `Missing staticfiles manifest entry`   | Manifest yok veya dosya adı yanlış.                            | Kaynak dosyanın varlığını doğrula, `collectstatic --noinput` çalıştır.                      |
| `DisallowedHost` / 400                 | Host listede yok.                                              | localhost veya Render hostunun ayarlara eklendiğini doğrula; `*` ile geçiştirme.            |
| Form POST'unda 403                     | CSRF token/origin/cookie sorunu.                               | Formda csrf_token var mı, aynı domain ve protokol mü? HTTPS proxy ayarını kontrol et.       |
| Logout adresinde 405                   | GET ile çıkış istenmiş.                                        | Base şablonundaki CSRF'li POST formunu kullan.                                              |
| Silme adresinde 405                    | GET isteğiyle gerçek silme çağrılmış.                          | Bu beklenen korumadır; onay sayfasındaki POST düğmesini kullan.                             |
| Başkasının tweetinde 404               | Sahiplik filtresi.                                             | Beklenen davranış; kendi tweetinle dene.                                                    |
| `View didn't return an HttpResponse`   | Bir koşulda return yok.                                        | Her GET/POST/geçersiz form yolunun yanıt döndürdüğünü incele.                               |
| Formda yazdıklarım kayboluyor          | Geçersiz POST sonrası boş form kuruluyor.                      | Bağlı formu aynı render'a geri gönder.                                                      |
| `MultiValueDictKeyError` / `KeyError`  | Form alan adıyla okunan anahtar farklı.                        | `name`, form alanı ve cleaned_data anahtarını karşılaştır.                                  |
| `Unknown field(s)`                     | Form Meta.fields içinde olmayan model alanı veya sonda boşluk. | `message` ile `message ` farklıdır; bu projede yalnızca message formda.                     |
| Port kullanımda                        | Önceki sunucu açık.                                            | Kendi sunucunu Ctrl+C ile durdur veya `runserver 8001` kullan.                              |
| `git push`: Everything up-to-date      | Yeni commit yok.                                               | `git status`; değişiklik varsa önce add ve commit.                                          |
| `src refspec main does not match any`  | Henüz commit yok veya dal adı farklı.                          | `git log -1`, `git branch`; ilk commit'i ve main dalını kontrol et.                         |
| `remote origin already exists`         | Uzak depo daha önce tanımlanmış.                               | `git remote -v`; doğruysa yeniden ekleme, yanlışsa URL'yi bilinçli düzelt.                  |
| Push rejected                          | Uzakta sende olmayan commit var.                               | Uzak değişiklikleri incele; force push yaparak silme.                                       |
| GitHub değişti ama site değişmedi      | Yanlış dal/depo veya deploy yapılmamış.                        | Render Source ve son commit kimliğini karşılaştır.                                          |
| Render klasörü bulamıyor               | Eski Root Directory yeni projeye yazılmış.                     | Yeni bağımsız depoda boş; eski eğitim deposunda DjangoTweet/djangotweet.                    |
| Render 500                             | Uygulama istisnası.                                            | Logs içindeki ilk ilgili traceback ve son hata satırını oku. DEBUG'u yayında açma.          |
| Canlı sitede hesaplar kayboldu         | Geçici SQLite dosyası yeniden oluştu.                          | Demo sınırlaması; kalıcı kullanımda veritabanı mimarisini değiştir.                         |

**Log okuma yöntemi:** Zamanı ve ilgili isteği bul → traceback'in son satırındaki hata türünü oku → kendi dosyanın yolunu ve satırını bul → son yaptığın değişiklikle ilişkilendir → tek düzeltme yap → aynı isteği yeniden dene. Python dosyasındaki kırmızı çizgi ile gerçek çalışma zamanı hatası aynı şey olmayabilir; editörün doğru `.venv` yorumlayıcısını seçtiğini kontrol et.

<a id="alistirmalar"></a>

## 22. Kendi başına alıştırmalar ve cevaplar

> ### Amaç kod ezberini ölçmek değil
>
> Buradaki alıştırmaları README'ye bakmadan çözmeye çalış. Takıldığında geri dön. Bir özelliği değiştirirken hangi dosyaların etkilendiğini söyleyebilmek, Django mimarisini anladığının iyi bir göstergesidir.

### Önce bakmadan yap

1. Başlığı, ana rengi ve boş liste mesajını değiştir. Model/migration dosyasına dokunman gerekiyor mu?
2. Sayfa başına tweet sayısını 10'dan 5'e indir. İlgili testi nasıl güncellersin?
3. Mesaj sınırını 100'den 140'a çıkar. Model, form mesajı, sayaç, şablon metni ve testlerde hangi noktalar değişir? Migration oluşturmayı unutma.
4. Kullanıcının kendi tweetlerini göreceği `/my-tweets/` sayfasını ekle. Sadece menüde gizlemekle yetinme; view giriş istesin.
5. `?q=django` ile mesajda arama ekle. `request.GET.get`, `filter(message__icontains=...)` ve sayfalamada sorguyu korumayı düşün.
6. JavaScript'i kapatıp tweet oluştur. Backend neden hâlâ çalışıyor?
7. İkinci bir kullanıcıyla başkasının düzenleme URL'sini aç. Koruma hangi dosyada?
8. Bir tasarım değişikliğini anlamlı commit olarak kaydet. Push ile deploy arasındaki farkı kendi cümlenle yaz.

### Kavrama soruları

- `save(commit=False)` neden ekleme akışında var, düzenlemede neden gerekmiyor?
- `SECRET_KEY` neden kullanıcı parolası değil?
- `DEBUG=False` olunca hata ortadan kalkmış olur mu?
- `git push` neden kaydedilmemiş dosyayı göndermez?
- `collectstatic` neden veritabanı oluşturmaz?
- `makemigrations` neden tek başına tabloyu değiştirmez?
- POST kullanmak neden sahiplik kontrolünün yerine geçmez?
- GitHub'dan klonladığında eski kullanıcıların neden gelmez?

<details>
<summary>Cevap anahtarını aç — önce kendin açıklamayı dene</summary>

1. Tasarım değişikliği veritabanı yapısını değiştirmez; migration gerekmez.
2. Paginator'ın sayfa boyutu değişir. Testte ilk/ikinci sayfada beklenen kayıt sayıları buna göre değişmelidir.
3. Model max_length, form hata metni, JavaScript sayaç metni, form/list sayfasındaki açıklamalar ve sınır testleri değişir. Model değiştiği için migration gerekir.
4. `@login_required` ile korunan view, `Tweet.objects.filter(author=request.user)` kullanır. Aynı liste şablonu kullanılabilir; başlıkları uyarlamak gerekir.
5. View sorguya göre filtreler; sayfa bağlantıları `q` değerini URL kodlamasıyla korumazsa ikinci sayfada arama kaybolur.
6. JavaScript yalnızca sayaçtır. Asıl doğrulama ve kayıt Django'dadır.
7. View'daki `get_object_or_404(..., author=request.user)` sahipliği kontrol eder. Template yalnızca düğmeyi gizler.
8. Commit yerel sürüm kaydı, push uzaktaki depoya gönderim, deploy sunucuda o sürümü çalıştırmadır.

Eklemede henüz yazar atanmamıştır; commit=False yazarı eklemeden DB'ye kaydetmeyi önler. Düzenlemede mevcut ve sahipliği kontrol edilmiş instance'ın yazarı korunur. SECRET_KEY uygulamanın imzalama anahtarıdır, kullanıcı kimlik bilgisi değildir. DEBUG=False teknik ayrıntıyı gizler; hatayı çözmez. Push commit gönderir, çalışma klasöründeki her dosyayı kopyalamaz. Collectstatic dosya toplar, migration tablo yapısını değiştirir. Makemigrations tarif oluşturur, migrate uygular. POST istek yöntemi, sahiplik ise yetki kuralıdır. SQLite Git dışında tutulduğu için klonla kullanıcı verisi gelmez.

</details>

### Kendi başına tamamladım ölçütü

Hazır kodu kapatıp boş bir klasörde model → form → view → URL → template sırasını tarif edebiliyorsan; iki kullanıcıyla yetkiyi test edebiliyorsan; bir hatayı logdan takip edip düzeltebiliyorsan; git add/commit/push ve build/start ayrımını anlatabiliyorsan bu çalışmanın temel hedefini tamamladın. Sonraki projede aynı adımları farklı bir fikir için kullan: kişisel notlar, kitap listesi veya görev takip uygulaması.

<a id="eski-proje"></a>

## 23. Mevcut projeyle farklar

> ### Neden bu karşılaştırma var?
>
> Eski eğitim projesi ile bu yeni çalışma aynı klasör yapısını, Django sürümünü ve bazı model/form kararlarını kullanmıyor. İki projeden parçaları rastgele birleştirirsen hata çıkabilir.
>
> Bu bölüm “eski kod yanlış” demek için değil; **hangi örneğin hangi projeye ait olduğunu karıştırmaman** için var.

Bu bölüm eski eğitim dosyalarını okurken yeni rehberle karıştırmaman içindir. **README'deki örneklerin mevcut projeye uygulanmış olduğunu varsayma.**

| Eski eğitim projesi                                        | Bu rehberdeki yeni çalışma                             |
| ---------------------------------------------------------- | ------------------------------------------------------ |
| Django 4.2.30, mevcut ortak sanal ortam                    | Ayrı Python 3.12 ortamında Django 5.2 serisi.          |
| Depoda DjangoTweet/djangotweet/manage.py                   | Ayrı depoda kökte manage.py.                           |
| Tweet.username kullanıcı ilişkisi                          | Tweet.author kullanıcı ilişkisi; ad daha açık.         |
| message alanı 100 karakter                                 | Aynı sınır; form ve testlerle doğrulanıyor.            |
| Eski Form örneği nickname anahtarlarına başvuruyor         | Tek ModelForm akışı; yazar oturumdan atanıyor.         |
| ModelForm'da username kullanıcıya açık                     | Yazar alanı formda bulunmuyor.                         |
| Silme GET bağlantısıyla gerçekleşebiliyor                  | GET yalnızca onay gösterir, silme POST ister.          |
| Sahip olmayan kullanıcı için view yanıtı eksik kalabiliyor | Sahiplik filtresiyle 404; tüm yollar yanıt döndürüyor. |
| Logout bağlantısı kullanılıyor                             | Django 5.2 ile uyumlu POST logout.                     |
| Bootstrap CDN kullanılıyor                                 | Tam yerel HTML/CSS; harici frontend bağımlılığı yok.   |
| Düzenleme ve tarih alanı yok                               | Düzenleme, created_at ve sayfalama var.                |
| Özel otomatik testler yok                                  | Temel akış ve yetki kuralları için testler var.        |

Eski veritabanını yeni projeye kopyalayıp çalıştırma; model yapıları farklıdır. Yeni proje kendi ilk migration'ını üretir. Bu, eğitimi baştan bağımsız yapman içindir.

**Eski projeyi yalnızca yeniden açmak istersen**, onun klasörünü ve ortamını kullan:

```bash
cd "/Users/omerfarukiris/Desktop/Yazılım/Python/Django/DjangoTweet/djangotweet"
source "/Users/omerfarukiris/Desktop/Yazılım/.venv/bin/activate"
DEBUG=True python manage.py runserver
```

Eski projede de ana liste `/` adresindedir. Önceki README'de bulunan `/tweetapp/` yolu ve nickname alanı, daha eski öğrenme aşamasına aitti. Bu rehber o eski tariflerin yerine geçer.

<a id="kaynaklar"></a>

## 24. Resmî kaynaklar ve sözlük

> ### Bu bölüm ne zaman kullanılmalı?
>
> README'deki adımları tamamlamak için her bağlantıyı şimdi okumak zorunda değilsin. Bir kavramı daha derin öğrenmek veya davranışın resmî tanımını görmek istediğinde ilgili kaynağa dön.
>
> Özellikle Django belgelerinde sürüm seçiminin **5.2** olduğuna dikkat et; farklı sürümlerde davranış veya örnek kod değişebilir.

Bu bağlantılar konuyu derinleştirmek içindir. Temel çalışma için gereken dosyalar yukarıda tam verilmiştir. Belgelerde başka sürümlere ait örnekler görürsen sürüm seçicisini **5.2** olarak kontrol et.

| Kaynak                                                                                                                                   | Hangi soruya yardımcı olur?                                                                    |
| ---------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| [Python venv](https://docs.python.org/3.12/library/venv.html)                                                                            | Sanal ortam neden var, nasıl çalışıyor?                                                        |
| [Django başlangıç rehberi](https://docs.djangoproject.com/en/5.2/intro/tutorial01/)                                                      | Proje, app, view ve URL ilişkisi.                                                              |
| [Django modeller](https://docs.djangoproject.com/en/5.2/topics/db/models/)                                                               | Alanlar ve ForeignKey ilişkileri.                                                              |
| [Django migration](https://docs.djangoproject.com/en/5.2/topics/migrations/)                                                             | Şema değişikliklerinin yönetimi.                                                               |
| [Django ModelForm](https://docs.djangoproject.com/en/5.2/topics/forms/modelforms/)                                                       | fields, instance, doğrulama ve commit=False.                                                   |
| [Django kimlik doğrulama](https://docs.djangoproject.com/en/5.2/topics/auth/default/)                                                    | LoginView, LogoutView, UserCreationForm ve oturumlar.                                          |
| [Django şablon dili](https://docs.djangoproject.com/en/5.2/ref/templates/language/)                                                      | extends, include, değişkenler, filtreler ve otomatik kaçış.                                    |
| [Django CSRF](https://docs.djangoproject.com/en/5.2/howto/csrf/)                                                                         | POST formlarında CSRF belirteci ve AJAX farkları.                                              |
| [Django test araçları](https://docs.djangoproject.com/en/5.2/topics/testing/tools/)                                                      | TestCase, test istemcisi ve yanıt kontrolleri.                                                 |
| [Django yayın kontrolü](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)                                               | DEBUG, gizli anahtar, host ve HTTPS ayarları.                                                  |
| [Django desteklenen sürümler](https://www.djangoproject.com/download/#supported-versions)                                                | Hangi sürüm güvenlik güncellemesi alıyor?                                                      |
| [MDN HTML](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content)                                      | Semantik HTML ve sayfa yapısı.                                                                 |
| [MDN CSS](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics)                                            | Seçiciler, kutu modeli ve stiller.                                                             |
| [Git başlangıç](https://git-scm.com/docs/gittutorial)                                                                                    | add, commit, diff ve depo kavramları.                                                          |
| [GitHub kimlik doğrulama](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github) | HTTPS/SSH ile güvenli Git erişimi.                                                             |
| [WhiteNoise Django](https://whitenoise.readthedocs.io/en/stable/django.html)                                                             | Statik dosyalar, middleware sırası ve manifest.                                                |
| [Render Django](https://render.com/docs/deploy-django)                                                                                   | Platformun Django yayın yaklaşımı; oradaki PostgreSQL adımları bu SQLite demosundan farklıdır. |
| [Render ücretsiz plan](https://render.com/docs/free)                                                                                     | Uyku, dosya kalıcılığı ve ücretsiz servis sınırları.                                           |
| [Render diskler](https://render.com/docs/disks)                                                                                          | Geçici dosya sistemi ile kalıcı depolama farkı.                                                |
| [Render Python](https://render.com/docs/python-version)                                                                                  | Python sürümünü sabitlemek.                                                                    |

## Kısa sözlük: **repository/depo** kod geçmişinin tutulduğu yer; **branch/dal** ayrı geliştirme hattı; **commit** sürüm kaydı; **deploy/yayın** kodu sunucuda çalışır hale getirme; **host** isteğin geldiği alan adı; **port** uygulamanın dinlediği numaralı bağlantı noktası; **environment variable/ortam değişkeni** kod dışından sağlanan ayar; **traceback** hataya giden Python çağrı zinciri; **manifest** statik dosyaların ad eşleme kaydı; **CRUD** oluşturma, okuma, güncelleme ve silme işlemleri.

# Ek: Bu README ile çalışırken önerilen tekrar yöntemi

Projeyi ilk kez kurarken kodlara bakman normal. Fakat öğrenme için ikinci turda şu yöntemi kullan:

```text
1. README'yi kapat.
2. Boş kağıda/nota dosya akışını yaz:
   Model → Form → View → URL → Template
3. Her dosyanın görevini bir cümleyle açıkla.
4. Tweet ekleme akışını baştan sona kendi cümlenle anlat.
5. Sonra kodu açıp eksiklerini karşılaştır.
```

Bir kod satırını hatırlamaman problem değildir. Gerçek hedef şudur:

> “Bu özelliği yapmak için hangi katmanlara dokunmam gerektiğini ve nedenini biliyorum.”

Örneğin mesaj sınırını 100'den 140'a çıkarmak istediğinde yalnızca bir sayı değiştirmek yerine düşün:

```text
Model kuralı değişiyor mu?        → Evet
Migration gerekir mi?             → Evet
Form hata mesajı etkileniyor mu?  → Evet
Sayaç/metin etkileniyor mu?       → Evet
Testler etkileniyor mu?           → Evet
```

Bu şekilde çalıştığında Django'yu kod ezberleyerek değil, sistem mantığını anlayarak öğrenmiş olursun.
