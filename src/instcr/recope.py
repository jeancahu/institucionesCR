import subprocess

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
