# Threefold Repetition

- Bu projede, bir satranç oyununa ait notasyon üzerinden konum tekrarları kontrol edilmektedir. Mevcut satranç programlarının bu konudaki eksiklikleri de dikkate alınmıştır.

***

- Notasyonun İngilizce olması gerekmektedir. Notasyon, satranç platformlarından kopyalanabilir.

- Konum tekrarları, FEN kodları karşılaştırılarak kontrol edilmektedir. FEN kodlarında "rok" ve "en passant" kontrolü zaten mevcuttur.

- FIDE kuralları 9.2.3 uyarınca, konum tekrarlarının kontrolünde "hamlede olan" oyuncu, "rok" ve "en passant" durumları ayrı ayrı değerlendirilmektedir.

- Ayrıca, "50 hamle" kontrolü de yapılmaktadır.