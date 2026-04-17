import random

# 10 enemigos, uno por nivel. Stats crecen progresivamente.
ENEMIGOS_POR_NIVEL = {
    1:  {"nombre": "Goblin Ladronzuelo",  "emoji": "👺", "ataque": 10, "defensa": 4,  "vida_maxima": 60,  "exp": 50},
    2:  {"nombre": "Lobo Salvaje",        "emoji": "🐺", "ataque": 13, "defensa": 5,  "vida_maxima": 75,  "exp": 70},
    3:  {"nombre": "Esqueleto Guerrero",  "emoji": "💀", "ataque": 16, "defensa": 7,  "vida_maxima": 90,  "exp": 95},
    4:  {"nombre": "Ogro del Pantano",    "emoji": "👹", "ataque": 19, "defensa": 9,  "vida_maxima": 110, "exp": 120},
    5:  {"nombre": "Mago Oscuro",         "emoji": "🧙", "ataque": 22, "defensa": 6,  "vida_maxima": 100, "exp": 150},
    6:  {"nombre": "Caballero Maldito",   "emoji": "⚫", "ataque": 24, "defensa": 14, "vida_maxima": 130, "exp": 185},
    7:  {"nombre": "Quimera Rabiosa",     "emoji": "🐉", "ataque": 27, "defensa": 11, "vida_maxima": 145, "exp": 220},
    8:  {"nombre": "Liche Ancestral",     "emoji": "☠️",  "ataque": 30, "defensa": 13, "vida_maxima": 160, "exp": 260},
    9:  {"nombre": "Demonio Abismal",     "emoji": "😈", "ataque": 34, "defensa": 15, "vida_maxima": 180, "exp": 310},
    10: {"nombre": "Dragón Oscuro",       "emoji": "🔥", "ataque": 40, "defensa": 18, "vida_maxima": 220, "exp": 400},
}


def crear_enemigo(nivel_batalla):
    """Crea y devuelve el Enemigo correspondiente al nivel indicado (1-10)."""
    nivel = max(1, min(10, nivel_batalla))
    datos = ENEMIGOS_POR_NIVEL[nivel]
    return Enemigo(
        nombre=f"{datos['emoji']} {datos['nombre']}",
        nivel=nivel,
        ataque=datos["ataque"],
        defensa=datos["defensa"],
        vida_maxima=datos["vida_maxima"],
        exp_recompensa=datos["exp"],
    )


class Enemigo:
    def __init__(self, nombre, nivel, ataque, defensa, vida_maxima, exp_recompensa=50):
        self.nombre = nombre
        self.nivel = nivel
        self.ataque = ataque
        self.defensa = defensa
        self.vida_maxima = vida_maxima
        self.vida = vida_maxima
        self.exp_recompensa = exp_recompensa

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
            print(f"  {self.nombre} ataca a {personaje.nombre} por {dano_final} de daño.")
        print(f"     (ATK variable: {variacion_ataque} | DEF de {personaje.nombre}: {variacion_defensa})")