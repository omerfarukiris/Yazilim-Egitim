# import numpy as np

#  Burada numpy kütüphanesini kullanarak iki listeyi çarpıyoruz. Önce geleneksel yöntemle bir for döngüsü kullanarak çarpma işlemi yapıyoruz, ardından numpy array'leri kullanarak aynı işlemi daha kısa ve verimli bir şekilde gerçekleştiriyoruz.

# geleneksel yöntemle çarpma işlemi
# a = [1, 2, 3, 4, 5]
# b = [6, 7, 8, 9, 10]

# ab = []

# for i in range(0, len(a)):
#     ab.append(a[i] * b[i])
#     print(ab[i])

# numpy array'leri kullanarak çarpma işlemi:

# neden numpy kullanıyoruz? Çünkü numpy array'leri, geleneksel listelere göre daha hızlı ve daha verimli bir şekilde matematiksel işlemler yapmamıza olanak tanır. Ayrıca, numpy array'leri ile yapılan işlemler daha kısa ve okunabilir kodlar yazmamızı sağlar.

# a = np.array([1, 2, 3, 4, 5])
# b = np.array([6, 7, 8, 9, 10])

# print(a * b)

# Numpy array'leri oluşturmak için farklı yöntemler de vardır. Örneğin, np.zeros(), np.ones(), np.full(), np.arange() ve np.linspace() gibi fonksiyonlar kullanarak farklı boyutlarda ve değerlerde array'ler oluşturabiliriz.

# np.zeros(10, dtype=int)  # 10 tane 0 oluşturur ve veri tipini integer olarak ayarlar. np.zeros(başlangıç boyutu, dtype=veri tipi) şeklinde kullanılır.

# np.ones((3, 5), dtype=int)  #3 e 5 lik bir matris oluşturur ve tüm elemanları 1 olarak ayarlar. np.ones((satır sayısı, sütun sayısı), dtype=veri tipi) şeklinde kullanılır.

# np.full((3, 5), 7, dtype=int)  # 3 e 5 lik bir matris oluşturur ve tüm elemanları 7 olarak ayarlar. np.full((satır sayısı, sütun sayısı), değer, dtype=veri tipi) şeklinde kullanılır.

# np.arrange(0, 10, 2)  # 0 dan 10 a kadar olan sayıları 2 şer 2 şer artırarak bir array oluşturur. np.arrange(başlangıç, bitiş, adımlar) şeklinde kullanılır.

# np.linspace(0, 1, 5)  # 0 dan 1 e kadar olan sayıları eşit aralıklarla böler ve bir array oluşturur. np.linspace(başlangıç, bitiş, nokta sayısı) şeklinde kullanılır.

# np.random.normal(10,4,(3,4))  # 10 ortalama ve 4 standart sapma ile 3 e 4 lük bir matris oluşturur. np.random.normal(ortalama,standart sapma, bu 3 e 4 lük matris boyutu) şeklinde kullanılır.

# np.random.randint(0, 10, (3, 4))  # 0 ile 10 arasında rastgele sayılarla 3 e 4 lük bir matris oluşturur. np.random.randint(başlangıç, bitiş, boyut) şeklinde kullanılır.

# ndim  = boyut sayısını verir.
# shape = boyutları verir.
# size = toplam eleman sayısını verir.
# dtype = veri tipini verir.
# itemsize = her bir elemanın byte cinsinden boyutunu verir.


# a = np.arange(1, 10).reshape(
#     (3, 3)
# )  # 0 dan 10 a kadar olan sayıları 2 şer 2 şer artırarak bir array oluşturur. np.arange(başlangıç, bitiş, adımlar) şeklinde kullanılır.
# #.resphape((satır sayısı, sütun sayısı)) şeklinde kullanılır. Bu örnekte 1 den 10 a kadar olan sayıları 3 e 3 lük bir matris haline getiriyoruz.
# print(a)

# x = np.array([[1, 2, 3]])
# y = np.array([[4, 5, 6]])
# z = np.concatenate(
#     (x, y), axis=0
# )  # iki array'i birleştirir. axis=0 satır bazında birleştirir. axis=1 sütun bazında birleştirir.
