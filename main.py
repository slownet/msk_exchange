import requests

parameters = {
    "iss.meta": "off",
    "iss.only": "securities",
    "securities.columns": "SECID,PREVADMITTEDQUOTE",
}

response = requests.get(
    "https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.xml",
    params=parameters
)

print("a")
