import requests
import itertools as IT


class PokeAPI:
    def __init__(self):
        self.api_base_url = 'https://pokeapi.co/api/v2'

    def make_request(self, endpoint):
        """
        Realiza una request a la API y verifica el status code
        :param endpoint:
        :return: request
        """
        r = requests.get(endpoint)
        if r.status_code >= 500:
            print(f'[{r.status_code}] Error de servidor')
            return None
        elif r.status_code == 404:
            print(f'[{r.status_code}] URL no encontrada: [{endpoint}]')
            return None
        elif r.status_code == 400:
            print(f'[{r.status_code}] Bad Request')
            return None
        elif r.status_code >= 300:
            print(f'[{r.status_code}] Error de redirección')
            return None
        elif r.status_code == 200:
            return r.json()
        else:
            print(f'Error: [HTTP {r.status_code}]: Contenido: {r.content}')
        return None

    def poke_name(self) -> int:
        """
        Obtén cuantos pokemones poseen en sus nombres “at” y tienen 2 “a” en su
        nombre, incluyendo la primera del “at”.
        :return: Contador de pokemones
        """
        # definir endpoint
        # encontré que el resultado es más rápido si obtengo todos los pokemon
        # en un solo request, en lugar de hacer muchos request por cada página
        endpoint_path = '/pokemon/?limit=1118'
        endpoint = f"{self.api_base_url}{endpoint_path}"
        # iniciar contador
        counter = IT.count()

        # hacer el request
        r = self.make_request(endpoint)
        # comprobar si el request fue exitoso
        if r is not None:
            results = r['results']
            # en la lista de nombres en los resultados,
            # contar los pokemon que cumplen con condición
            [next(counter) for _, pokemon in enumerate(results)
             if pokemon['name'].count('a') == 2 and 'at' in pokemon['name']]

        else:
            print('Hubo un problema al realizar el request.')
            return None

        return next(counter)

    def poke_raichu(self) -> int:
        """
        ¿Con cuántas especies de pokémon puede procrear raichu?
        (2 Pokémon pueden procrear si están dentro del mismo egg group).
        Tu respuesta debe ser un número. Recuerda eliminar los duplicados.
        :return: Número de especies
        """
        # definir los endpoints para cada egg group
        endpoint_path_ground = '/egg-group/5'
        endpoint_path_fairy = '/egg-group/6'

        # buscar en el egg group: ground
        endpoint_ground = f"{self.api_base_url}{endpoint_path_ground}"
        r = self.make_request(endpoint_ground)

        if r is not None:
            # obtener los nombres de los pokemon species
            especies = [especie['name'] for especie in r['pokemon_species']]

            # buscar en el egg group: fairy
            endpoint_fairy = f"{self.api_base_url}{endpoint_path_fairy}"
            r = self.make_request(endpoint_fairy)

            if r is not None:
                # convertir lista a set para que no haya repetidos
                especies = set(especies)
                # agregar las especies del egg group fairy
                [especies.add(especie['name'])
                 for especie in r['pokemon_species']]
            else:
                print('Hubo un problema al realizar el request.')
                return None
        else:
            print('Hubo un problema al realizar el request.')
            return None

        return len(especies)

    def get_weight(self, endpoint: str) -> int:
        """
        Hace una request y obtiene el peso de cada pokemon
        :param endpoint:
        :return: Peso de cada pokemon
        """
        r = self.make_request(endpoint)
        return r['weight']

    def poke_weight(self) -> list:
        """
        Entrega el máximo y mínimo peso de los pokémon de tipo fighting de
        primera generación (cuyo id sea menor o igual a 151).
        Tu respuesta debe ser una lista con el siguiente formato: [1234, 12],
        en donde 1234 corresponde al máximo peso y 12 al mínimo.
        :return: Lista con peso máximo y peso mínimo
        """
        # definir endpoint
        endpoint_path = '/type/2/'
        endpoint = f"{self.api_base_url}{endpoint_path}"

        # hacer el request
        r = self.make_request(endpoint)
        if r is not None:
            # try por si hay una excepcion de tipo TypeError si algun llamado a
            # self.get_weight devuelve None
            try:
                weights = [self.get_weight(pokemon['pokemon']['url'])
                           for pokemon in r['pokemon']
                           if int(pokemon['pokemon']['url'].split('/')[-2]) <= 151]
            except TypeError:
                return None
        else:
            print('Hubo un problema al realizar el request.')
            return None

        return ([max(weights), min(weights)])
