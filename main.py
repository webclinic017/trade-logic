import os
from trade_logic.trader import Trader
from trade_logic.utils import bitis_gunu_truncate_hour_precision, print_islem_detay
from datetime import datetime, timezone


def trader_calis(trader):
    trader.init()
    trader.heikinashi_kontrol_4h()
    trader.rsi_ema_karar_hesapla()
    trader.karar_calis()
    trader.cikis_kontrol()
    trader.pozisyon_al()


def app_calis():
    # bitis_gunu = datetime.strptime('2022-04-03 00:00:00', '%Y-%m-%d %H:%M:%S')
    # bitis_gunu = bitis_gunu.replace(tzinfo=timezone.utc)
    bitis_gunu = datetime.utcnow()
    bitis_gunu = bitis_gunu_truncate_hour_precision(bitis_gunu, 4)


    trader = Trader(bitis_gunu)
    trader.sqlite_service.trader_eski_verileri_temizle(bitis_gunu)
    trader.init_prod()
    trader_calis(trader)
    if os.getenv("PYTHON_ENV") != "TEST":
        trader.borsada_islemleri_hallet()
    print_islem_detay(trader)
    if trader.karar.value == 3:
        trader.reset_trader()
    trader.sqlite_service.trader_durumu_kaydet(trader)


if __name__ == '__main__':
    app_calis()
    # TODO:: piyasanin durumunu atr'den cikararak rsi ayarlari degistirmek en mantikli yaklasim olabilir
    # TODO:: once alttaki maddeyi ekle sonra stateleri daha duzgun tutup strteji yaz bastan 1-rsi ve emasi, 2-ema_trend, normal ema ile cikis
    # TODO:: daha sik calistirip su anki fiyattan erken cikis dene, basktest icin bunu yari handle etmen lazim
    # TODO:: onceki karar ve karar verilerine pozisyonu kapatmayi dene, karar 0 iken pozisyon olsa kapatmayi dusunuebiliriz
    # TODO:: check rsi kesisme arrayin son verilerini alip en son veri yukari kesmis mi gibi bir kontrol, uzun suren
    #  asiri satis ve alislarda karini arttirmasi icin
    # TODO:: pazari 2'ye bol trending ve ranging diye ema veya rsi degerlerinden
    # TODO:: basarili islem oranini da islemler tablosundan hesapla
    # TODO:: decorator videosu yap
    # TODO:: thread videosu yap
    # TODO:: islem acikken wallet'da usdt gozukuyor, acik islem bilgisini cekip state'i ona gore ezmek lazim
    # TODO:: binance servis exception alirsa uygulamayi bastan baslat
    # TODO:: yeni versiyon cikmadan once calistirabilcegin testler yaz
    #        mesela alis yapiyor mu belli bir case'de, tp dogru takip ediyor mu, cikis yapiyor mu tp de,
    #        binance baglanti hatasi alirsa tekrar program basliyor mu gibi

    # TODO:: uygulama patlarsa hatayi e-posta ile gonder
