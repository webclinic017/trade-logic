from signal_atr.atr import ATR


class SuperTrendStrategy:
    def __init__(self, conf):
        self.config = conf
        self.atr = None
        self.atr_value = None
        self.suanki_fiyat = 0
        self.tp = 0
        self.onceki_tp = 0

    def atr_hesapla(self, trader):
        series_4h = trader.series.sort_values(by='open_ts_int', ascending=True)
        self.atr_4h_15 = ATR(series_4h, 15).average_true_range
        self.atr_value_4h_15 = float(self.atr_4h_15[0])

    def update_tp(self, trader):
        # pozisyon 0 iken bu fonksiyon aslinda calismiyor
        if trader.pozisyon.value * self.onceki_tp < trader.pozisyon.value * self.tp:
            self.onceki_tp = self.tp

    def calculate_tp(self, pozisyon):
        return self.suanki_fiyat + (-1 * pozisyon.value * self.config.get("supertrend_mult") * self.atr_value_4h_15)

    def tp_hesapla(self, pozisyon):
        if pozisyon.value != 0:
            self.tp = self.calculate_tp(pozisyon)
        if self.onceki_tp == 0:
            self.onceki_tp = self.tp

    def reset_super_trend(self):
        self.onceki_tp = 0
        self.tp = 0
