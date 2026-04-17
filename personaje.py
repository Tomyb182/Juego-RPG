import random

CLASES = {
    "guerrero": {
        "descripcion": "Tanque resistente con alto ataque físico.",
        "ataque": 22,
        "defensa": 14,
        "vida_maxima": 130,
        "mana_maximo": 20,
        "hechizo_nombre": "Golpe Devastador",
        "hechizo_desc": "Un golpe brutal que ignora la defensa enemiga.",
        "hechizo_costo_mana": 10,
        "hechizo_usos": 2,
    },
    "mago": {
        "descripcion": "Daño masivo con poca defensa.",
        "ataque": 14,
        "defensa": 6,
        "vida_maxima": 90,
        "mana_maximo": 40,
        "hechizo_nombre": "Bola de Fuego",
        "hechizo_desc": "Inflige daño mágico ignorando defensa física.",
        "hechizo_costo_mana": 15,
        "hechizo_usos": 3,
    },
    "asesino": {
        "descripcion": "Alta probabilidad de crítico y esquive.",
        "ataque": 20,
        "defensa": 8,
        "vida_maxima": 95,
        "mana_maximo": 25,
        "hechizo_nombre": "Sombra Mortal",
        "hechizo_desc": "Ataque en la sombra: siempre es golpe crítico.",
        "hechizo_costo_mana": 12,
        "hechizo_usos": 2,
    },
    "sacerdote": {
        "descripcion": "Se cura durante el combate y tiene buena defensa.",
        "ataque": 12,
        "defensa": 12,
        "vida_maxima": 110,
        "mana_maximo": 35,
        "hechizo_nombre": "Luz Sagrada",
        "hechizo_desc": "Te cura entre 20 y 35 puntos de vida.",
        "hechizo_costo_mana": 10,
        "hechizo_usos": 3,
    },
}


class Personaje:
    def __init__(self, nombre, clase):
        if clase not in CLASES:
            raise ValueError(f"Clase inválida. Elegí entre: {list(CLASES.keys())}")

        self.nombre = nombre
        self.clase = clase

        self.nivel = 1
        self.experiencia = 0
        self.exp_para_subir = 100

        datos = CLASES[clase]
        self.ataque = datos["ataque"]
        self.defensa = datos["defensa"]
        self.vida_maxima = datos["vida_maxima"]
        self.vida = self.vida_maxima
        self.mana_maximo = datos["mana_maximo"]
        self.mana = self.mana_maximo

        self.hechizo_nombre = datos["hechizo_nombre"]
        self.hechizo_desc = datos["hechizo_desc"]
        self.hechizo_costo_mana = datos["hechizo_costo_mana"]
        self.hechizo_usos = datos["hechizo_usos"]
        self.hechizo_usos_restantes = datos["hechizo_usos"]

    # ------------------------------------------------------------------
    def ganar_experiencia(self, cantidad):
        self.experiencia += cantidad
        print(f"\n  ✨ {self.nombre} gana {cantidad} XP  "
              f"({self.experiencia}/{self.exp_para_subir})")

        while self.experiencia >= self.exp_para_subir:
            self.experiencia -= self.exp_para_subir
            self._subir_nivel_interactivo()

    def _subir_nivel_interactivo(self):
        self.nivel += 1
        self.exp_para_subir = int(self.exp_para_subir * 1.5)

        # Restaurar usos de hechizo al subir de nivel
        self.hechizo_usos_restantes = self.hechizo_usos
        # Restaurar maná completo
        self.mana = self.mana_maximo

        print(f"\n{'='*50}")
        print(f"  🆙  ¡{self.nombre} SUBIÓ AL NIVEL {self.nivel}!")
        print(f"{'='*50}")
        print(f"  Stats actuales → ATK:{self.ataque}  DEF:{self.defensa}  "
              f"HP:{self.vida}/{self.vida_maxima}  MANA:{self.mana_maximo}")
        print()
        print("  Elegí qué stat mejorar:")
        print("  ┌──────────────────────────────────────┐")
        print("  │  [1] ⚔️   Ataque    (+5)             │")
        print("  │  [2] 🛡️   Defensa   (+4)             │")
        print("  │  [3] ❤️   Vida máx  (+20)            │")
        print("  │  [4] 💧  Maná máx  (+15)            │")
        print("  └──────────────────────────────────────┘")

        while True:
            opcion = input("  > Ingresá 1, 2, 3 o 4: ").strip()
            if opcion in ("1", "2", "3", "4"):
                break
            print("  ⚠️  Opción inválida.")

        if opcion == "1":
            self.ataque += 5
            print(f"\n  ✅ ¡Ataque aumentado! ATK: {self.ataque - 5} → {self.ataque}")
        elif opcion == "2":
            self.defensa += 4
            print(f"\n  ✅ ¡Defensa aumentada! DEF: {self.defensa - 4} → {self.defensa}")
        elif opcion == "3":
            self.vida_maxima += 20
            self.vida = min(self.vida + 20, self.vida_maxima)
            print(f"\n  ✅ ¡Vida máxima aumentada! HP máx: {self.vida_maxima - 20} → {self.vida_maxima}")
        elif opcion == "4":
            self.mana_maximo += 15
            self.mana = self.mana_maximo
            print(f"\n  ✅ ¡Maná máximo aumentado! MANA máx: {self.mana_maximo - 15} → {self.mana_maximo}")

        print(f"  Stats nuevos → ATK:{self.ataque}  DEF:{self.defensa}  "
              f"HP máx:{self.vida_maxima}  MANA máx:{self.mana_maximo}")
        print(f"  (Hechizos y maná restaurados para la próxima batalla)")
        print(f"{'='*50}\n")

    # ------------------------------------------------------------------
    def atacar(self, enemigo):
        variacion_ataque = random.randint(int(self.ataque * 0.8), int(self.ataque * 1.2))
        variacion_defensa = random.randint(int(enemigo.defensa * 0.8), int(enemigo.defensa * 1.2))
        es_critico = random.randint(1, 100) <= 30
        if es_critico:
            variacion_ataque = int(variacion_ataque * 1.5)
        dano_final = max(1, variacion_ataque - variacion_defensa * 2)
        enemigo.vida -= dano_final

        if es_critico:
            print(f"  ⚡ ¡CRÍTICO! {self.nombre} ataca a {enemigo.nombre} por {dano_final} de daño.")
        else:
            print(f"  ⚔️  {self.nombre} ataca a {enemigo.nombre} por {dano_final} de daño.")
        print(f"     (ATK variable: {variacion_ataque} | DEF enemiga: {variacion_defensa})")

    # ------------------------------------------------------------------
    def esquivar(self):
        exito = random.randint(1, 100) <= 20
        if exito:
            print(f"  💨 ¡{self.nombre} esquiva con éxito! No recibirá daño este turno.")
        else:
            print(f"  😬 {self.nombre} intenta esquivar... pero falla.")
        return exito

    # ------------------------------------------------------------------
    def lanzar_hechizo(self, enemigo):
        if self.hechizo_usos_restantes <= 0:
            print(f"  ❌ No quedan usos de '{self.hechizo_nombre}'.")
            return False
        if self.mana < self.hechizo_costo_mana:
            print(f"  ❌ Maná insuficiente. Necesitás {self.hechizo_costo_mana}, tenés {self.mana}.")
            return False

        self.hechizo_usos_restantes -= 1
        self.mana -= self.hechizo_costo_mana

        if self.clase == "guerrero":
            dano = random.randint(int(self.ataque * 1.0), int(self.ataque * 1.8))
            enemigo.vida -= dano
            print(f"  🗡️  ¡{self.nombre} usa {self.hechizo_nombre}! {dano} de daño (ignora DEF).")

        elif self.clase == "mago":
            dano = random.randint(28, 45)
            enemigo.vida -= dano
            print(f"  🔥 ¡{self.nombre} lanza {self.hechizo_nombre}! {dano} de daño mágico.")

        elif self.clase == "asesino":
            dano = int(random.randint(int(self.ataque * 0.8), int(self.ataque * 1.2)) * 1.5)
            dano = max(1, dano - int(enemigo.defensa * 0.5))
            enemigo.vida -= dano
            print(f"  🌑 ¡{self.nombre} ejecuta {self.hechizo_nombre}! {dano} de daño crítico.")

        elif self.clase == "sacerdote":
            curacion = random.randint(20, 35)
            self.vida = min(self.vida_maxima, self.vida + curacion)
            print(f"  ✨ ¡{self.nombre} usa {self.hechizo_nombre}! Recupera {curacion} HP.")

        print(f"     (Usos restantes: {self.hechizo_usos_restantes} | "
              f"Maná: {self.mana}/{self.mana_maximo})")
        return True