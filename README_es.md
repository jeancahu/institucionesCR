# InstitucionesCR Scraper

Scraper en Python para recuperar algunos datos importantes publicados por las instituciones.
Instituciones soportadas:

- BCCR, Banco Central de Costa Rica (precio del dólar)
- RECOPE (Precios de combustibles en estaciones y terminales)

Los valores actualizados diariamente son de utilidad en procesos automáticos,
lamentablemente muchas veces no es de interés de las instituciones el habilitar
APIs para consultar dichos valores fácilmente por parte de programas, por esta
razón he creado este pequeño proyecto para tomar estos datos desde las interfaces
previamente creadas para personas.

## Install

    pip install instcr

## Usage

### Obtener información de precios de combustible desde RECOPE

```python
from instcr.recope import Recope

recope = Recope()

recope.print_data()

print(f"\nPrecio del diesel: {recope.table_estaciones['diesel_50']['precio_litro_total']}")

## Mucho tiempo después:

recope.update()

## Precio del diesel en estasiones
recope.table_estaciones['diesel_50']['precio_litro_total']

## Precio del diesel en terminales
recope.table_terminales['diesel_50']['precio_litro_total']

# recope.table_estaciones.keys() Muestra todos los combustibles disponibles en estaciones
```

### Tipo de cambio desde el Banco Central de Costa Rica

```python
from instcr.bccr import Bccr

bccr = Bccr()

## Mostrar las dos tablas de venta y compra
bccr.print_data()

## Imprimir la información de hoy, (date= datetime para especificar una fecha diferente)
print(f"\n Today sell dollar price: {bccr.dollar('sell')}")
print(f"\n Today buy dollar price: {bccr.dollar('buy')}")
```
