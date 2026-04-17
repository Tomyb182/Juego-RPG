import random

    
CLASES = {
    "guerrero": {
        "descripcion": "Tanque resistente con alto ataque físico.",
        "ataque": 22,
        "defensa": 14,
        "vida_maxima": 130,
        "hechizo_nombre": "Golpe Devastador",
        "hechizo_desc": "Un golpe brutal que ignora la defensa enemiga.",
        "hechizo_costo": 0,   # sin maná, usos limitados
        "hechizo_usos": 2,
    },
    "mago": {
        "descripcion": "Daño masivo con poca defensa.",
        "ataque": 14,
        "defensa": 6,
        "vida_maxima": 90,
        "hechizo_nombre": "Bola de Fuego",
        "hechizo_desc": "Inflige daño mágico ignorando defensa física.",
        "hechizo_costo": 0,
        "hechizo_usos": 3,
    },
    "asesino": {
        "descripcion": "Alta probabilidad de crítico y esquive.",
        "ataque": 20,
        "defensa": 8,
        "vida_maxima": 95,
        "hechizo_nombre": "Sombra Mortal",
        "hechizo_desc": "Ataque en la sombra: siempre es golpe crítico.",
        "hechizo_costo": 0,
        "hechizo_usos": 2,
    },
    "sacerdote": {
        "descripcion": "Se cura durante el combate y tiene buena defensa.",
        "ataque": 12,
        "defensa": 12,
        "vida_maxima": 110,
        "hechizo_nombre": "Luz Sagrada",
        "hechizo_desc": "Te cura entre 20 y 35 puntos de vida.",
        "hechizo_costo": 0,
        "hechizo_usos": 3,
    },
}


class Personaje:
    def __init__(self, nombre, clase):
        if clase not in CLASES:
            raise ValueError(f"Clase inválida. Elegí entre: {list(CLASES.keys())}")

        self.nombre = nombre
        self.clase = clase

        # progresión
        self.nivel = 1
        self.experiencia = 0
        self.exp_para_subir = 100

        datos = CLASES[clase]

        self.ataque = datos["ataque"]
        self.defensa = datos["defensa"]
        self.vida_maxima = datos["vida_maxima"]
        self.vida = self.vida_maxima

        self.hechizo_nombre = datos["hechizo_nombre"]
        self.hechizo_desc = datos["hechizo_desc"]
        self.hechizo_usos = datos["hechizo_usos"]
        self.hechizo_usos_restantes = datos["hechizo_usos"]
    
    def ganar_experiencia(self, cantidad):
        self.experiencia += cantidad
        print(f"\n✨ {self.nombre} gana {cantidad} XP")

        while self.experiencia >= self.exp_para_subir:
            self.experiencia -= self.exp_para_subir
            self.subir_nivel()

    def subir_nivel(self):
        self.nivel += 1
        self.exp_para_subir = int(self.exp_para_subir * 1.5)

        # mejoras de stats
        self.ataque += 3
        self.defensa += 2
        self.vida_maxima += 10
        self.vida = self.vida_maxima

        print(f"\n🆙 ¡{self.nombre} sube a nivel {self.nivel}!")
        print(f"   ATK: {self.ataque} | DEF: {self.defensa} | HP: {self.vida_maxima}")

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
        print(f"     (Ataque: {variacion_ataque} | Defensa enemiga: {variacion_defensa})")

    # ------------------------------------------------------------------
    def esquivar(self):
        """Intenta esquivar el próximo ataque enemigo (20 % de éxito).
        Devuelve True si logra esquivar."""
        exito = random.randint(1, 100) <= 20
        if exito:
            print(f"  💨 ¡{self.nombre} esquiva con éxito! No recibirá daño este turno.")
        else:
            print(f"  😬 {self.nombre} intenta esquivar... pero falla.")
        return exito

    # ------------------------------------------------------------------
    def lanzar_hechizo(self, enemigo):
        """Lanza el hechizo de clase. Devuelve False si no quedan usos."""
        if self.hechizo_usos_restantes <= 0:
            print(f"  ❌ {self.nombre} no tiene usos de '{self.hechizo_nombre}' restantes.")
            return False

        self.hechizo_usos_restantes -= 1
        clase = self.clase

        if clase == "guerrero":
            # Ignora defensa
            dano = random.randint(int(self.ataque * 1.0), int(self.ataque * 1.8))
            enemigo.vida -= dano
            print(f"  🗡️  ¡{self.nombre} usa {self.hechizo_nombre}! {dano} de daño ignorando defensa.")

        elif clase == "mago":
            # Daño mágico fijo alto
            dano = random.randint(28, 45)
            enemigo.vida -= dano
            print(f"  🔥 ¡{self.nombre} lanza {self.hechizo_nombre}! {dano} de daño mágico.")

        elif clase == "asesino":
            # Golpe crítico garantizado
            dano = int(random.randint(int(self.ataque * 0.8), int(self.ataque * 1.2)) * 1.5)
            dano = max(1, dano - int(enemigo.defensa * 0.5))
            enemigo.vida -= dano
            print(f"  🌑 ¡{self.nombre} ejecuta {self.hechizo_nombre}! {dano} de daño crítico garantizado.")

        elif clase == "sacerdote":
            # Curación
            curacion = random.randint(20, 35)
            self.vida = min(self.vida_maxima, self.vida + curacion)
            print(f"  ✨ ¡{self.nombre} usa {self.hechizo_nombre}! Recupera {curacion} puntos de vida.")

        usos_restantes = self.hechizo_usos_restantes
        print(f"     (Usos restantes de {self.hechizo_nombre}: {usos_restantes})")
        return True
