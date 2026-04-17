import random


class Enemigo:
    def __init__(self, nombre, nivel, ataque, defensa, vida_maxima=100):
        self.nombre = nombre
        self.nivel = nivel
        self.ataque = ataque
        self.defensa = defensa
        self.vida_maxima = vida_maxima
        self.vida = vida_maxima

    def atacar(self, personaje):
        variacion_ataque = random.randint(int(self.ataque * 0.8), int(self.ataque * 1.2))
        variacion_defensa = random.randint(int(personaje.defensa * 0.8), int(personaje.defensa * 1.2))
        es_critico = random.randint(1, 100) <= 30
        if es_critico:
            variacion_ataque = int(variacion_ataque * 1.5)
        dano_final = max(1, variacion_ataque - variacion_defensa * 2)
        personaje.vida -= dano_final

        if es_critico:
            print(f"  ⚡ ¡CRÍTICO! {self.nombre} golpea a {personaje.nombre} por {dano_final} de daño.")
        else:
            print(f"  🐲 {self.nombre} ataca a {personaje.nombre} por {dano_final} de daño.")
        print(f"     (Ataque: {variacion_ataque} | Defensa de {personaje.nombre}: {variacion_defensa})")