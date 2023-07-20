import subprocess
import requests
from datetime import datetime

import re
import json
from bs4 import BeautifulSoup
from unidecode import unidecode

url = 'https://www.recope.go.cr/productos/precios-nacionales/tabla-precios/'


class Recope():
    def __init__(self):
        try:
            # Use subprocess to execute the curl command and download the webpage
            process = subprocess.Popen(['curl', url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            # Check if the curl command executed successfully
            if process.returncode == 0:
                # Print the HTML content (you can process it further as needed)
                self.text = stdout.decode('utf-8')
                self.text = self.text.replace('<br>', ' ')
            else:
                print(f"Failed to download the URL. Error: {stderr.decode('utf-8')}")

            self.text = unidecode(self.text) # Accents remove
            self.text=self.text.lower()

            self.process_estaciones_table()
            self.process_terminales_table()

        except Exception as e:
            print(e)

    def _process_row(self, table, header, row):
        if row[0] == 'producto':
            header = [re.sub(r'\s+', '_', el.replace('/', '')) for el in row]
            return table, header

        result = dict()
        for index, el in enumerate(header):
            if not index:
                continue

            result[el] = float(row[index])

        table[re.sub(r'\s+', '_', row[0]).replace('-','_')] = result
        return table, header

    def update(self):
        self.__init__()

    def process_estaciones_table (self):
        # Crear un objeto BeautifulSoup para analizar el contenido HTML
        soup = BeautifulSoup(self.text, 'html.parser')

        tablas_recope = soup.find_all(class_='tabla')
        tabla_recope = tablas_recope[0] # TODO

        # Encontrar todos los elementos div en el HTML
        elements = tabla_recope.find_all('tr')

        # Crear una lista con el contenido de los elementos div
        content_list = [tr for tr in elements]

        table = dict()
        header = list()
        for tr in content_list:
            if tr:
                row = [el for el in tr.get_text().split('\n') if el]

                if len(row) > 1:
                    table, header = self._process_row(table, header, row)

        self.table_estaciones = table

    def process_terminales_table (self):
        # Crear un objeto BeautifulSoup para analizar el contenido HTML
        soup = BeautifulSoup(self.text, 'html.parser')

        tablas_recope = soup.find_all(class_='tabla')
        tabla_recope = tablas_recope[1] # TODO

        # Encontrar todos los elementos div en el HTML
        elements = tabla_recope.find_all('tr')

        # Crear una lista con el contenido de los elementos div
        content_list = [tr for tr in elements]

        table = dict()
        header = list()
        for tr in content_list:
            if tr:
                row = [el for el in tr.get_text().split('\n') if el]

                if len(row) > 1:
                    table, header = self._process_row(table, header, row)

        self.table_terminales = table

    def print_data (self):
        # Convert the dictionary back to a sorted JSON string
        sorted_json = json.dumps(self.table_terminales, indent=2, sort_keys=True)
        print(sorted_json)

        sorted_json = json.dumps(self.table_estaciones, indent=2, sort_keys=True)
        print(sorted_json)

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
                'https://gee.bccr.fi.cr/indicadoreseconomicos/cuadros/frmvercatcuadro.aspx?idioma=2&codcuadro=%20400',
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
