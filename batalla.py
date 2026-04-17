from personaje import Personaje
from enemigo import Enemigo


def mostrar_menu(personaje):
    hechizo_info = (
        f"{personaje.hechizo_nombre} "
        f"({personaje.hechizo_usos_restantes}u / {personaje.mana}mp)"
        if personaje.hechizo_usos_restantes > 0 and personaje.mana >= personaje.hechizo_costo_mana
        else f"{personaje.hechizo_nombre} (no disponible)"
    )
    print()
    print("  ┌─────────────────────────────────────────┐")
    print("  │            ¿Qué hacés?                  │")
    print("  ├─────────────────────────────────────────┤")
    print("  │  [1] ⚔️   Atacar                        │")
    print("  │  [2] 💨  Esquivar  (20 % de éxito)      │")
    print(f"  │  [3] ✨  Hechizo: {hechizo_info:<24}│")
    print("  └─────────────────────────────────────────┘")

    while True:
        opcion = input("  > Ingresá 1, 2 o 3: ").strip()
        if opcion in ("1", "2", "3"):
            return int(opcion)
        print("  ⚠️  Opción inválida. Ingresá 1, 2 o 3.")


class Batalla:
    def __init__(self, personaje: Personaje, enemigo: Enemigo):
        self.personaje = personaje
        self.enemigo = enemigo
        self.turno = 0
        self.registro = []
        self.activa = True
        self.ganador = None

    def ejecutar(self):
        print(f"\n{'='*52}")
        print("              ¡BATALLA INICIADA!")
        print(f"  {self.personaje.nombre} (Nv.{self.personaje.nivel} {self.personaje.clase.capitalize()})")
        print(f"  vs  {self.enemigo.nombre} (Nv.{self.enemigo.nivel})")
        print(f"{'='*52}\n")

        while self.activa:
            self.turno += 1
            print(f"── TURNO {self.turno} " + "─" * 40)
            self._mostrar_estado()

            opcion = mostrar_menu(self.personaje)
            print()
            esquivando = False

            if opcion == 1:
                self.personaje.atacar(self.enemigo)
                self._reg(f"{self.personaje.nombre} ataca. "
                          f"{self.enemigo.nombre}: {self.enemigo.vida} HP.")

            elif opcion == 2:
                esquivando = self.personaje.esquivar()
                self._reg(f"{self.personaje.nombre} esquiva "
                          f"({'éxito' if esquivando else 'falla'}).")

            elif opcion == 3:
                ok = self.personaje.lanzar_hechizo(self.enemigo)
                if not ok:
                    print("  (Se realiza un ataque normal en su lugar.)")
                    self.personaje.atacar(self.enemigo)
                self._reg(f"{self.personaje.nombre} usa hechizo. "
                          f"{self.enemigo.nombre}: {self.enemigo.vida} HP.")

            if self.enemigo.vida <= 0:
                self.ganador = "personaje"
                self.activa = False
                break

            print()
            if esquivando:
                print(f"  🛡️  {self.personaje.nombre} esquivó el ataque de {self.enemigo.nombre}.")
                self._reg(f"{self.enemigo.nombre} ataca pero {self.personaje.nombre} esquiva.")
            else:
                self.enemigo.atacar(self.personaje)
                self._reg(f"{self.enemigo.nombre} ataca. "
                          f"{self.personaje.nombre}: {self.personaje.vida} HP.")

            if self.personaje.vida <= 0:
                self.ganador = "enemigo"
                self.activa = False
                break

            print()

        self._mostrar_resultado()

        # Otorgar experiencia si el jugador ganó
        if self.ganador == "personaje":
            self.personaje.ganar_experiencia(self.enemigo.exp_recompensa)

    # ------------------------------------------------------------------
    def _mostrar_estado(self):
        p, e = self.personaje, self.enemigo
        print(f"  {p.nombre:<18} {self._barra(p.vida, p.vida_maxima)}  "
              f"{p.vida}/{p.vida_maxima} HP  💧{p.mana}/{p.mana_maximo}")
        print(f"  {e.nombre:<18} {self._barra(e.vida, e.vida_maxima)}  "
              f"{e.vida}/{e.vida_maxima} HP")

    @staticmethod
    def _barra(vida, maxima, largo=10):
        llenos = int((max(0, vida) / maxima) * largo)
        return "❤️ " + "█" * llenos + "░" * (largo - llenos)

    def _reg(self, evento):
        self.registro.append(f"T{self.turno}: {evento}")

    def _mostrar_resultado(self):
        print(f"\n{'='*52}")
        if self.ganador == "personaje":
            print(f"  🎉 ¡{self.personaje.nombre} GANA LA BATALLA!")
            print(f"  Vida restante: {self.personaje.vida}/{self.personaje.vida_maxima} HP")
            print(f"  Recompensa: {self.enemigo.exp_recompensa} XP")
        else:
            print(f"  💀 ¡{self.personaje.nombre} FUE DERROTADO!")
            print(f"  {self.enemigo.nombre} fue demasiado fuerte...")
        print(f"{'='*52}\n")

    def mostrar_historial(self):
        print("\n--- HISTORIAL ---")
        for evento in self.registro:
            print(" ", evento)
        print("-----------------\n")