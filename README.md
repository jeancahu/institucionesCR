# InstitucionesCR Scraper

[Spanish README/ README en español](https://github.com/jeancahu/institucionesCR/blob/main/README_es.md)

Python Scraper to retrieve important data published by institutions.
Supported institutions:

- BCCR, Central Bank of Costa Rica (dollar exchange rate)
- RECOPE (Fuel prices at stations and terminals)

The daily updated values are useful in automated processes; unfortunately,
many times institutions do not prioritize enabling APIs for easy value retrieval
by programs. For this reason, I have created this small project to fetch
these data from the interfaces previously designed for humans.

## Install

    pip install instcr

## Usage

### Get fuel price information from RECOPE

```python
from instcr import Recope

recope = Recope()

recope.print_data()

print(f"\nPrecio del diesel: {recope.table_estaciones['diesel_50']['precio_litro_total']}")

## ## Much later:

recope.update()

## Diesel price at stations
recope.table_estaciones['diesel_50']['precio_litro_total']

## Diesel price at terminals
recope.table_terminales['diesel_50']['precio_litro_total']

# recope.table_estaciones.keys() Shows all available fuels at stations
```

### Exchange rate from the Central Bank of Costa Rica

```python
from instcr import Bccr

bccr = Bccr()

## Show both buy and sell tables
bccr.print_data()

## Print today's information (date= datetime to specify a different date)
print(f"\n Today sell dollar price: {bccr.dollar('sell')}")
print(f"\n Today buy dollar price: {bccr.dollar('buy')}")
```
