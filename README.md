# Recope Scraper

## Install

    pip install -r requierements.txt

## Usage

```python
from recope import Recope

recope = Recope()

recope.print_data()

print(f"\nPrecio del diesel: {recope.table_estaciones['diesel_50']['precio_litro_total']}")

## Mucho tiempo después:

recope.update()

## Precio del diesel en estasiones
recope.table_estaciones['diesel_50']['precio_litro_total']

## Precio del diesel en terminales
recope.table_terminales['diesel_50']['precio_litro_total']
```
