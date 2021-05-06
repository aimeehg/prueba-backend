from PokeAPI import PokeAPI

def main():
    poke_api = PokeAPI()

    pregunta_1 = poke_api.poke_name()
    if pregunta_1 is not None:
        print(f'Pokemones que poseen en sus nombres “at” y tienen 2 “a” en su nombre: {pregunta_1}')

    pregunta_2 = poke_api.poke_raichu()
    if pregunta_2 is not None:
        print(f'¿Con cuántas especies de pokémon puede procrear raichu?: {pregunta_2}')

    pregunta_3 = poke_api.poke_weight()
    if pregunta_3 is not None:
        print(f'El máximo y mínimo peso de los pokémon de tipo fighting de primera generación: {pregunta_3}')

if __name__ == '__main__':
    main()

