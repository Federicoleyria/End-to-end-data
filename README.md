# Proyecto end to end desde Web Scrapping en Python hasta el análisis en Power BI
# Hoteles de Córdoba Capital, Argentina en Booking.com

![](https://github.com/Federicoleyria/End-to-end-data/blob/main/Flujo%20de%20trabajo.PNG)
## Descripción
Este proyecto realiza scraping de datos de Booking.com para extraer información sobre hoteles en Córdoba, Argentina, para el mes de julio de 2024. La información incluye nombres de hoteles, precios, puntuaciones, distancias al centro de la ciudad y descripciones. Los datos se limpian y procesan en un archivo CSV que luego se utiliza para crear un dashboard en Power BI.

Este proyecto se ha desarrollado exclusivamente con el propósito de practicar y mejorar mis habilidades en ingeniería de datos y análisis de datos. En ningún momento se ha utilizado para recopilar datos personales ni se ha tenido la intención de utilizar la información de manera indebida.

Es importante destacar que, aunque este proyecto abarca una pequeña cantidad de datos inicialmente, ha sido diseñado con todas las fases necesarias para obtener información valiosa de manera ética. Además, está concebido como un proyecto escalable, lo que permite la recopilación de datos de tanto meses,semanas o dias disponibles en la página booking.com.
## Requisitos
Python 3.x
Librerías de Python: pandas, playwright
Power BI
Instalación
Clona el repositorio:
bash
Copiar código
git clone https://github.com/tu-usuario/tu-proyecto.git
Navega al directorio del proyecto:
bash
Copiar código
cd tu-proyecto
Instala las dependencias necesarias:
bash
Copiar código
pip install pandas playwright
playwright install
Uso
Ejecución del Script de Scraping
Ejecuta el script de scraping:
bash
Copiar código
python scraping_hoteles.py
Este script realizará el scraping de los datos de Booking.com y los guardará en un archivo hoteles_booking.csv.

## Limpieza de Datos
Ejecuta el script de etl:
bash
Copiar código
python limpieza_datos.py
Este script limpiará y procesará los datos, y guardará el resultado en un archivo hoteles_booking_clean.csv.

 ## Visualización en Power BI
Importa el archivo hoteles_booking_clean.csv en Power BI para crear visualizaciones y análisis de los datos.

## Codigo
En el codigo encontrara comentarios de lo que realiza cada linea explicando el funcionamiento.

## Power BI
Aqui se realizo un análisis simple destancando los hoteles mas caros, precio de hoteles mas cercanos al centro de Córdoba, o el menor precio de un hotel.

![](https://github.com/Federicoleyria/End-to-end-data/blob/main/Power%20BI%20An%C3%A1lisis%20Booking.com%20C%C3%B3rdoba.PNG)
