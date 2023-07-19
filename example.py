from recope import Recope

recope = Recope()

recope.print_data()

print(f"\nPrecio del diesel: {recope.table_estaciones['diesel_50']['precio_litro_total']}")
