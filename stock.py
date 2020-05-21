from datetime import date

import requests


def do_request(stock_id: str = None,
               engine: str = "stock",
               market: str = "shares",
               board: str = "TQBR",
               request_parameters: dict = None) -> dict:
    # create url by template

    url = f"https://iss.moex.com/iss"

    if engine:
        url += f"/engines/{engine}"

    if market:
        url += f"/markets/{market}"

    if board:
        url += f"/boards/{board}"

    url += "/securities"

    # add stock id if needed
    if stock_id is not None:
        url += f"/{stock_id}.json"

    response = requests.get(url, params=request_parameters)
    json_data = response.json()

    json_parameter = "marketdata"
    if "iss.only" in request_parameters:
        json_parameter = request_parameters["iss.only"]

    market_data = json_data[json_parameter]

    # zip column names and values into one dictionary
    data_dict = dict(zip(market_data["columns"], market_data["data"][0]))

    return data_dict


class Stock:
    def __init__(self, stock_id: str):
        self.stock_id = stock_id
        self.full_stock_name = None

        self.request_parameters = {
            "iss.json": "extended",
            "marketdata.columns": "SECID,SECNAME,LAST",
        }

    def get_id(self) -> str:
        return self.stock_id

    def get_price(self) -> float:
        response_dict = do_request(
            stock_id=self.stock_id,
            request_parameters={
                "iss.meta": "off",
                "iss.only": "marketdata",
                "securities.columns": "SECID,LAST",
            }
        )

        return float(response_dict["LAST"])

    def get_full_name(self) -> str:
        if self.full_stock_name:
            return self.full_stock_name

        response_dict = do_request(
            stock_id=self.stock_id,
            request_parameters={
                "iss.meta": "off",
                "iss.only": "securities",
                "securities.columns": "SECID,SECNAME",
            }
        )

        return response_dict["SECNAME"]

    def get_dividends(self, date_from: str, date_till: str = str(date.today())) -> list:
        """
        Requests dividend list from a specific date.
        Every dividend is a dictionary with such keys: ['secid', 'isin', 'registryclosedate', 'value', 'currencyid']

        Request exmample:
            http://iss.moex.com/iss/securities/TATN/dividends.json?iss.meta=off&from=2015-07-15&till=2016-06-24&start=0&dividends.columns=registryclosedate

        :param date_from: starting date in format: YYYY-MM-DD
        :param date_till: optional date where default value is today (same format as date_from)

        :return: dividends list
        """

        url = f"http://iss.moex.com/iss/securities/TATN/dividends.json"
        request_parameters = {
            "iss.meta": "off",
            "from": date_from,
            "till": date_till,
        }
        response = requests.get(url, params=request_parameters)
        json_data = response.json()

        # unwrap dividents layer
        json_data = json_data["dividends"]

        # FIXME: find how to filter data in request
        # strings are compared lexicographically
        all_dividends_list = [dict(zip(json_data["columns"], dividend))
                              for dividend in json_data["data"]]

        filtered_dividends_list = [dividend for dividend in all_dividends_list
                                   if date_from <= dividend["registryclosedate"] <= date_till]

        return filtered_dividends_list

    def __str__(self) -> str:
        return f"{self.get_id()} - {self.get_full_name()}: {self.get_price()}"
