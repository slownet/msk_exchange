import requests


def do_request(stock_id=None, engine="stock", market="shares", board="TQBR", request_parameters=None):
    # create url by template

    url = f"https://iss.moex.com/iss/engines/{engine}/markets/{market}/boards/{board}/securities"

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
    def __init__(self, stock_id):
        self.stock_id = stock_id
        self.full_stock_name = None

        self.request_parameters = {
            "iss.json": "extended",
            "marketdata.columns": "SECID,SECNAME,LAST",
        }

    def get_id(self):
        return self.stock_id

    def get_price(self):
        response_dict = do_request(
            stock_id=self.stock_id,
            request_parameters={
                "iss.meta": "off",
                "iss.only": "marketdata",
                "securities.columns": "SECID,LAST",
            }
        )

        return response_dict["LAST"]

    def get_full_name(self):
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

    def __str__(self):
        return f"{self.get_id()} - {self.get_full_name()}: {self.get_price()}"


if __name__ == "__main__":
    yandex_stock = Stock("YNDX")
    sber_stock = Stock("SBER")

    print(yandex_stock)
    print(sber_stock)
