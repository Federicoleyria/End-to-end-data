#Este archivo analisis lo cre
import pandas as pd

# Cargar el archivo CSV con el delimitador correcto
df = pd.read_csv('hoteles_booking.csv', delimiter=';', skipinitialspace=True)

# Verificar las primeras filas del DataFrame
print("Antes de eliminar columnas:")
print(df.head())

# Eliminar las últimas 8 columnas
df = df.iloc[:, :-11]

# Limpiar caracteres no numéricos en la columna 'price'
df['price'] = df['price'].str.replace(r'[^\d,]', '', regex=True).str.replace(',', '')

# Convertir las columnas al tipo adecuado
df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0).astype(int) # Convertir precios a enteros
df['puntuacion'] = pd.to_numeric(df['puntuacion'].str.replace(',', '.'), errors='coerce')  # Convertir puntuaciones a numéricos
df['distancia_centro'] = pd.to_numeric(df['distancia_centro'].str.replace(r'[^\d.]', '', regex=True), errors='coerce')  # Convertir distancias a numéricos

# Verificar los tipos de datos después de la conversión
print("Tipos de datos después de la conversión:")
print(df.dtypes)

# Verificar las primeras filas después de la conversión de tipos
print("Primeras filas después de la conversión:")
print(df.head())

# Guardar el DataFrame limpio en un nuevo archivo CSV
df.to_csv('hoteles_booking_clean.csv', index=False, encoding='utf-8-sig')
