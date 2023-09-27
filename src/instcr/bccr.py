import subprocess
import requests
from datetime import datetime

import re
from bs4 import BeautifulSoup
from unidecode import unidecode

url = 'https://gee.bccr.fi.cr/indicadoreseconomicos/cuadros/frmvercatcuadro.aspx?idioma=2&codcuadro=%20400'

class Bccr():
    def __init__(self):
        self._dollar = dict()
        self.update()

    def _process_row(self, table, header, row):
        pass

    def process_dollar_table(self):
        # Crear un objeto BeautifulSoup para analizar el contenido HTML
        soup = BeautifulSoup(self.text, 'html.parser')

        tablas_bccr = soup.find_all('table')

        table_html = ''
        for table in tablas_bccr:
            columns = table.find_all(class_='celda400')
            for col in columns:
                table_html += str(col)

        soup2 = BeautifulSoup(table_html, 'html.parser')
        rows = [re.sub(r'[\s\n\r]+', '', el.get_text()) for el in soup2.find_all('td')]

        dates = list()
        values = list()
        for row in rows:
            # Define el formato que coincide con la cadena de fecha proporcionada
            formato = "%d%b%Y"

            try:
                # Intenta parsear la cadena en un objeto datetime
                dates.append(datetime.strptime(row, formato))
            except ValueError as e:
                values.append(float(row))

        buy_dict = dict()
        sell_dict= dict()
        for index, (date, value) in enumerate(zip(dates*2, values)):
            if index < len(dates):
                sell_dict[date.strftime("%Y-%m-%d")] = value
            else:
                buy_dict[date.strftime("%Y-%m-%d")] = value

        self._dollar['sell'] = sell_dict
        self._dollar['buy'] = buy_dict

    def update(self):
        try:
            resp = requests.get(
                url,
                verify=True)

            if resp.status_code == 200:
                self.text = resp.text
                self.text = unidecode(self.text) # Accents remove
                self.text=self.text.lower()
                self.process_dollar_table()

            else:
                self.text = ''
                print(f"Failed to fetch the URL. Status code: {resp.status_code}")

        except Exception as e:
            print(e)

    def dollar(self, table, date=datetime.now()):
        date = date.strftime("%Y-%m-%d")
        #try:
        return self._dollar[table][date]
        #except TODO

    def print_data (self):
        print("Sell")
        for key, value in zip(self._dollar['sell'].keys(), self._dollar['sell'].values()):
            print(f'{key}: {value}')

        print("Buy")
        for key, value in zip(self._dollar['buy'].keys(), self._dollar['buy'].values()):
            print(f'{key}: {value}')
