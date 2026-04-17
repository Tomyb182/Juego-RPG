from personaje import Personaje, CLASES
from enemigo import Enemigo


def mostrar_menu(personaje):
    """Muestra el menú de acciones y devuelve la elección (1-3)."""
    hechizo_info = (
        f"{personaje.hechizo_nombre} ({personaje.hechizo_usos_restantes} uso/s)"
        if personaje.hechizo_usos_restantes > 0
        else f"{personaje.hechizo_nombre} (sin usos)"
    )
    print()
    print("  ┌─────────────────────────────────────┐")
    print("  │           ¿Qué hacés?               │")
    print("  ├─────────────────────────────────────┤")
    print("  │  [1] ⚔️   Atacar                    │")
    print("  │  [2] 💨  Esquivar  (20 % de éxito)  │")
    print(f"  │  [3] ✨  Hechizo: {hechizo_info:<22}│")
    print("  └─────────────────────────────────────┘")

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

    # ------------------------------------------------------------------
    def ejecutar(self):
        print(f"\n{'='*50}")
        print("           ¡BATALLA INICIADA!")
        print(f"  {self.personaje.nombre} ({self.personaje.clase.capitalize()}) "
              f"vs {self.enemigo.nombre} Nv.{self.enemigo.nivel}")
        print(f"{'='*50}\n")

        while self.activa:
            self.turno += 1
            print(f"── TURNO {self.turno} " + "─" * 38)
            self._mostrar_estado()

            # ── TURNO DEL JUGADOR ──────────────────────────────────────
            opcion = mostrar_menu(self.personaje)
            print()

            esquivando = False   # ¿el jugador eligió esquivar?

            if opcion == 1:
                self.personaje.atacar(self.enemigo)
                self._registrar(f"{self.personaje.nombre} ataca. "
                                f"{self.enemigo.nombre} tiene {self.enemigo.vida} HP.")

            elif opcion == 2:
                esquivando = self.personaje.esquivar()
                self._registrar(
                    f"{self.personaje.nombre} intenta esquivar "
                    f"({'éxito' if esquivando else 'falla'})."
                )

            elif opcion == 3:
                resultado = self.personaje.lanzar_hechizo(self.enemigo)
                if not resultado:
                    # Sin usos: fuerza ataque normal
                    print("  (Se realiza un ataque normal en su lugar.)")
                    self.personaje.atacar(self.enemigo)
                self._registrar(f"{self.personaje.nombre} usa hechizo. "
                                f"{self.enemigo.nombre} tiene {self.enemigo.vida} HP.")

            # Verificar si el enemigo cayó
            if self.enemigo.vida <= 0:
                self.ganador = "personaje"
                self.activa = False
                break

            # ── TURNO DEL ENEMIGO ──────────────────────────────────────
            print()
            if esquivando:
                print(f"  🛡️  {self.personaje.nombre} esquivó el ataque de {self.enemigo.nombre}.")
                self._registrar(f"{self.enemigo.nombre} ataca pero {self.personaje.nombre} esquiva.")
            else:
                self.enemigo.atacar(self.personaje)
                self._registrar(f"{self.enemigo.nombre} ataca. "
                                f"{self.personaje.nombre} tiene {self.personaje.vida} HP.")

            # Verificar si el personaje cayó
            if self.personaje.vida <= 0:
                self.ganador = "enemigo"
                self.activa = False
                break

            print()

        self._mostrar_resultado()

    # ------------------------------------------------------------------
    def _mostrar_estado(self):
        p = self.personaje
        e = self.enemigo
        barra_p = self._barra_vida(p.vida, p.vida_maxima)
        barra_e = self._barra_vida(e.vida, e.vida_maxima)
        print(f"  {p.nombre:<16} {barra_p}  {p.vida}/{p.vida_maxima} HP")
        print(f"  {e.nombre:<16} {barra_e}  {e.vida}/{e.vida_maxima} HP")

    @staticmethod
    def _barra_vida(vida, vida_maxima, largo=12):
        llenos = int((vida / vida_maxima) * largo)
        return "❤️ " + "█" * llenos + "░" * (largo - llenos)

    def _registrar(self, evento):
        self.registro.append(f"Turno {self.turno}: {evento}")

    def _mostrar_resultado(self):
        print(f"\n{'='*50}")
        if self.ganador == "personaje":
            print(f"  🎉 ¡{self.personaje.nombre} GANA LA BATALLA!")
            print(f"  Vida restante: {self.personaje.vida}/{self.personaje.vida_maxima}")
        else:
            print(f"  💀 ¡{self.personaje.nombre} FUE DERROTADO!")
            print(f"  {self.enemigo.nombre} fue demasiado fuerte...")
        print(f"{'='*50}\n")

    def mostrar_historial(self):
        print("\n--- HISTORIAL ---")
        for evento in self.registro:
            print(" ", evento)
        print("-----------------\n")