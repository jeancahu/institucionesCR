from instcr import Recope, Bccr

recope = Recope()

recope.print_data()

print(f"\nPrecio del diesel: {recope.table_estaciones['diesel_50']['precio_litro_total']}")

bccr = Bccr()

## Mostrar las dos tablas de venta y compra
bccr.print_data()

## Imprimir la información de hoy, (date= datetime para especificar una fecha diferente)
print(f"\n Today sell dollar: {bccr.dollar('sell')}")
print(f"\n Today buy dollar: {bccr.dollar('buy')}")
