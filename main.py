import requests
import json
import time
import logging
import datetime
import sqlite3


valute_list = [
    "AMD",
    "BYN",
    "EUR",
    "CNY",
    "USD",
]


def api_request():
    return requests.get("https://www.cbr-xml-daily.ru/daily_json.js")


def valute_info(request, name: str):
    valute = json.loads(request.text)["Valute"][name]
    logging.info(f"{valute['Nominal']} {valute['Name']} in RUB: {round(valute['Value'], 4)}, change: {round(valute['Value'] - valute['Previous'], 6)}")



if __name__ == "__main__":
    request = api_request()
    next_url = "https://www.cbr-xml-daily.ru/daily_json.js"
    history = []
    inter = 100
    
    x = time.time()
    logging.info(f"Start: {inter} Today: {datetime.datetime.now()}")
    request = requests.get(next_url)
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()


    cur.execute("""CREATE TABLE IF NOT EXISTS "CBRF" (
        "TIMESTAMP"	TEXT NOT NULL,
        "AMD"	    INTEGER NOT NULL,
        "BYN"	    INTEGER NOT NULL,
        "EUR"	    INTEGER NOT NULL,
        "USD"	    INTEGER NOT NULL
    );""")
    conn.commit()

    
    for i in range(0, inter):
        try:
            start = time.time()
            request = requests.get(next_url)
            data = json.loads(request.text)
            next_url = f"https:{data['PreviousURL']}"
            
            info = json.loads(request.text)
            data = (
                info['Timestamp'],
                round(float(info['Valute']['AMD']['Value']) / int(info['Valute']['AMD']['Nominal']), 8),
                round(float(info['Valute']['BYN']['Value']) / int(info['Valute']['BYN']['Nominal']), 4),
                round(float(info['Valute']['EUR']['Value']) / int(info['Valute']['EUR']['Nominal']), 4),
                round(float(info['Valute']['USD']['Value']) / int(info['Valute']['USD']['Nominal']), 4),
            )
            cur.execute("INSERT INTO CBRF VALUES(?, ?, ?, ?, ?);", data)
            conn.commit()
            logging.info(f"{i}/{inter}")
            if time.time() - start < 0.4:
                time.sleep(0.4 - (time.time() - start))
            
            
        except Exception as E:
            logging.info(f"Failed on {len(history)}, error: [{E}]")
            try:
                logging.info(request.text)
            except Exception as E:
                logging.info("Cant provide request.text")

    logging.info(f"End: {len(history)}/{inter}, {time.time() - x}, Today: {datetime.datetime.now()}")
    try:
        logging.info(f"Saved: ")
        with open('history.json', 'w+', encoding='UTF-8') as f:
            f.write(json.dumps(history))
    except Exception as E:
        logging.error(f"ERR:{E}")
        logging.error(f"history:{history}")
