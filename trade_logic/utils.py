import pandas as pd
from signal_prophet.ml.model_classes.prophet_model import ProphetModel
from datetime import datetime, timezone


def dongu_kontrol_decorator(func):
    def inner1(*args, **kwargs):
        if not args[0].dondu_4h:
            return
        print(f'#################### {args[0].bitis_gunu} icin basladi! ###################')
        returned_value = func(*args, **kwargs)

        return returned_value

    return inner1


def bitis_gunu_truncate_hour_precision(_now, arttir):
    bitis_gunu = _now.replace(minute=0, second=0, microsecond=0)
    _h = bitis_gunu.hour - (bitis_gunu.hour % arttir)
    bitis_gunu = bitis_gunu.replace(hour=_h)
    return bitis_gunu.replace(tzinfo=None)


# TODO:: bu iki fonksiyonu birlestir video bile cekilir
def bitis_gunu_truncate_min_precision(arttir):
    bitis_gunu = datetime.utcnow().replace(second=0, microsecond=0)
    _m = bitis_gunu.minute - (bitis_gunu.minute % arttir)
    bitis_gunu = bitis_gunu.replace(minute=_m)
    return bitis_gunu.replace(tzinfo=timezone.utc)


def tahmin_doldur(tahmin, wallet, prophet):
    tahmin["alis"] = float("nan")
    tahmin["satis"] = float("nan")
    tahmin["cikis"] = float("nan")

    tahmin["high"] = prophet.high
    tahmin["low"] = prophet.low
    tahmin["open"] = prophet.open

    tahmin["eth"] = wallet["ETH"]
    tahmin["usdt"] = wallet["USDT"]

    return tahmin


def okunur_date_yap(unix_ts):
    return datetime.utcfromtimestamp(unix_ts/1000).strftime("%Y-%m-%d %H:%M:%S")


def integer_date_yap(date_str):
    return int(datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=None).timestamp())


def model_egit_tahmin_et(train, pencere):
    model = ProphetModel(
        train=train,
        horizon=1,
        freq=pencere

    )
    model.fit()
    return model.predict()


def train_kirp_yeniden_adlandir(df, cesit):
    # df = df.iloc[:, :2]
    train = df.rename(columns={"open_ts_str": "ds"})
    train = train.rename(columns={cesit: "y"})
    return train


def tahmin_onceden_hesaplanmis_mi(baslangic_gunu, _config, tahminler_cache):
    if pd.Timestamp(baslangic_gunu) in tahminler_cache['ds_str'].values:
        return True
    return False


def print_islem_detay(trader):
    islem = trader.tahmin
    print(f"islem detaylar ==> ds: {islem.get('ds')} ")
    if islem.get('alis') > 0:
        print(f"\t\t\t\t ==> alis: {islem.get('alis')}")
    if islem.get('satis') > 0:
        print(f"\t\t\t\t ==> satis: {islem.get('satis')}")
    if islem.get('cikis') > 0:
        print(f"\t\t\t\t ==> cikis: {islem.get('cikis')}")
    print(f"\t\t\t\t ==> islem_miktari: {trader.islem_miktari} islem_fiyati: {trader.islem_fiyati}")


if __name__ == '__main__':
    bugun = '2021-12-06'
