from stock import Stock

if __name__ == "__main__":
    yandex_stock = Stock("YNDX")
    sber_stock = Stock("SBER")
    tatn_stock = Stock("TATN")

    print(yandex_stock)
    print(sber_stock)

    print()

    date_from = "2017-05-20"
    date_till = "2018-05-20"  # optional parameter

    print(f"{tatn_stock.get_full_name()} - dividend list from {date_from} till {date_till}")

    for dividend in tatn_stock.get_dividends(date_from, date_till):
        print(f"{dividend['registryclosedate']} - {dividend['value']} ({dividend['currencyid']})")
