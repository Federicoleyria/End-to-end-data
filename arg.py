#Importamos librerias especificas para el scrapping, se vio playwright.sync_api para este caso en Booking.com ya que no me permitia con Beautiful Soup
from playwright.sync_api import sync_playwright
import pandas as pd
import time
#Iniciamos la fucion principal
def main():
    #Usamos la funcion de sync_playwright() este objeto se puede utilizar para iniciar o conectarse a Firefox y devolver instancias de Browser .
    with sync_playwright() as p:
        #En estas variables guardamos las fechas desde y hasta que necesitemos extraer la informacion de los hoteles en la pagina, es muy interesante porque lo podremos usar para cualquier fecha que tenga disponible Booking
        checkin_date = '2024-07-03'
        checkout_date = '2024-07-30'
        #Traemos el url de la pagina, con las variables de las fechas
        page_url = f'https://www.booking.com/searchresults.es-ar.html?ss=C%C3%B3rdoba%2C+Provincia+de+C%C3%B3rdoba%2C+Argentina&ssne=Villa+Carlos+Paz&ssne_untouched=Villa+Carlos+Paz&label=es-ar-booking-desktop-MRRNwpxuLSY8eNXQ7griKwS652829001343%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3Alp1000126%3Ali%3Adec%3Adm&sid=5752bb7464ed2c22c85d619af46a593c&aid=2311236&lang=es-ar&sb=1&src_elem=sb&src=index&dest_id=-983417&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=es&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=898c039daae005a3&ac_meta=GhA4OThjMDM5ZGFhZTAwNWEzIAAoATICZXM6AWNAAEoAUAA%3D&checkin={checkin_date}&checkout={checkout_date}&group_adults=2&no_rooms=1&group_children=0'
        
        #Iniciamos el browser en chrome, yo personalmente utilizo chrome, pero firefox y otros mas
        browser = p.chromium.launch(headless=False)
        #Creamos la nueva pagina identica a la de la web
        page = browser.new_page()
        # Encendemos la nueva pagina con un tiempo de 60 min
        page.goto(page_url, timeout=60000)

        try:
            # Scroll hasta el final de la página para cargar todos los resultados
            last_height = page.evaluate('document.body.scrollHeight')
            while True:
                page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                time.sleep(5)  # Espera a que se carguen más resultados

                new_height = page.evaluate('document.body.scrollHeight')
                if new_height == last_height:
                    break
                last_height = new_height

            time.sleep(5)  # Espera adicional para asegurar que todos los elementos se carguen
            
            # Para aplicar click en el boton "Cargar más resultados" si es que esta
            while True:
                try:
                    show_more_button = page.locator('button:has-text("Cargar más resultados")').first
                    if show_more_button.is_visible():
                        show_more_button.click()
                        time.sleep(5)  # Espera adicional después de hacer clic
                    else:
                        break
                except Exception as e:
                    print(f'Error al hacer clic en "Cargar más resultados": {e}')
                    break

                time.sleep(5)  # Esperar a que se carguen más resultados

        except Exception as e:
            print(f'Error al encontrar el botón "Cargar más resultados": {e}')

        time.sleep(10)  # Espera adicional para asegurar que todos los elementos se carguen

        # Buscamos y extraemos la información de cada hotel con el selector principal
        try:
            page.wait_for_selector('//div[@data-testid="property-card"]', timeout=100000)
        except Exception as e:
            print(f'Error al esperar los elementos de hoteles: {e}')
        
        #Extraemos la cantidad de hoteles que hay en la pagina
        hoteles = page.locator('//div[@data-testid="property-card"]').all()
        print(f'La cantidad de hoteles es {len(hoteles)}.')

        #Iniciamos con la extraccion de los hoteles y sus requerimientos para el negocio, requerimientos en la creacion del dashboard
        #Creamos la lista de hoteles que va a almacenar los diccionarios
        lista_hoteles = []
        for hotel in hoteles:
            #Creamos el diccionario para el hotel y sus atributos
            hotel_dict = {}
            #Lo primero que traemos es el titulo o nombre del hotel
            try:
                hotel_dict['hotel'] = hotel.locator('div[data-testid="title"]').inner_text(timeout=10000)
            except Exception as e:
                print(f'Error obteniendo el nombre del hotel: {e}')
                hotel_dict['hotel'] = 'N/A'
            #Luego el precio
            try:
                hotel_dict['price'] = hotel.locator('span[data-testid="price-and-discounted-price"]').inner_text(timeout=10000)
            except Exception as e:
                print(f'Error obteniendo el precio del hotel: {e}')
                hotel_dict['price'] = 'N/A'
            #Obtener el puntaje, particularmente este fue el punto que mas costo ya que en el mismo div extraiba bastante informacion,se uso de la funcion first 
            try:
                # Obtener el puntaje del hotel
                score_element = hotel.locator('div[data-testid="review-score"] div.f13857cc8c.e008572b71').first
                puntaje_text = score_element.inner_text(timeout=10000).strip()
                # Extraer solo el número del puntaje
                puntaje_numero = puntaje_text.split()[0]
                hotel_dict['puntuacion'] = puntaje_numero
            except Exception as e:
                print(f'Error obteniendo la puntuación del hotel: {e}')
                hotel_dict['puntuacion'] = 'N/A'
            #Extraccion de la distancia al centro de Córdoba
            try:
                distance_element = hotel.locator('span[data-testid="distance"]')
                hotel_dict['distancia_centro'] = distance_element.inner_text(timeout=10000)
            except Exception as e:
                print(f'Error obteniendo la distancia al centro del hotel: {e}')
                hotel_dict['distancia_centro'] = 'N/A'
            #Por ultimo se extrajo la descripcion, que no sirvio mucho en el dashboard pero esta informacion en un futuro podria ser almacenada por una base de datos en caso de que este interesanda en algun hotel
            try:
                description_element = hotel.locator('h4[class="b290e5dfa6 cf1a0708d9"]').first
                hotel_dict['descripcion'] = description_element.inner_text(timeout=10000)
            except Exception as e:
                print(f'Error obteniendo la descripción del hotel: {e}')
                hotel_dict['descripcion'] = 'N/A'
            #Apendiamos los diccionarios a la lista d ehoteles
            lista_hoteles.append(hotel_dict)
        #Esto nos permite crear el datafram, y con estos scrip crear el csv
        df = pd.DataFrame(lista_hoteles)
        df.to_csv('hoteles_booking.csv', index=False, encoding='utf-8-sig')
        #Cerrar el browser(Buena practica)
        browser.close()

if __name__ == '__main__':
    main()
