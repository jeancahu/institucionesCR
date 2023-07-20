# Recope Scraper

## Install

    pip install -r requierements.txt

## Usage

### Obtener información de precios de combustible desde RECOPE

```python
from instcr import Recope

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

### Tipo de cambio desde el Banco Central de Costa Rica

```python
from instcr import Bccr

bccr = Bccr()

## Mostrar las dos tablas de venta y compra
bccr.print_data()

## Imprimir la información de hoy, (date= datetime para especificar una fecha diferente)
print(f"\n Today sell dollar price: {bccr.dollar('sell')}")
print(f"\n Today buy dollar price: {bccr.dollar('buy')}")
```
