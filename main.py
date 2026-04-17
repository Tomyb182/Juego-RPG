from personaje import Personaje, CLASES
from enemigo import crear_enemigo, ENEMIGOS_POR_NIVEL
from batalla import Batalla

MAX_NIVELES = 10


def seleccionar_clase():
    opciones = list(CLASES.keys())
    lineas = []
    for i, clave in enumerate(opciones, 1):
        d = CLASES[clave]
        lineas.append(f"[{i}] {clave.upper()} — {d['descripcion']}")
        lineas.append(f"    ATK:{d['ataque']}  DEF:{d['defensa']}  "
                      f"HP:{d['vida_maxima']}  MANA:{d['mana_maximo']}")
        lineas.append(f"    Hechizo: {d['hechizo_nombre']} "
                      f"(costo: {d['hechizo_costo_mana']} MP, {d['hechizo_usos']} usos)")

    ancho = max(len(l) for l in lineas) + 4
    print("\n╔" + "═" * ancho + "╗")
    print("║" + "ELEGÍ TU CLASE DE PERSONAJE".center(ancho) + "║")
    print("╠" + "═" * ancho + "╣")
    for i, linea in enumerate(lineas):
        print("║ " + linea.ljust(ancho - 1) + "║")
        if (i + 1) % 3 == 0 and i < len(lineas) - 1:
            print("║" + "─" * ancho + "║")
    print("╚" + "═" * ancho + "╝")

    while True:
        eleccion = input("\n> Ingresá el número de tu clase: ").strip()
        if eleccion.isdigit() and 1 <= int(eleccion) <= len(opciones):
            return opciones[int(eleccion) - 1]
        print("⚠️  Opción inválida.")


def mostrar_mapa(nivel_actual):
    """Muestra el progreso en los 10 niveles."""
    print("\n  🗺️  MAPA DE PROGRESO")
    print("  " + "─" * 42)
    partes = []
    for n in range(1, MAX_NIVELES + 1):
        datos = ENEMIGOS_POR_NIVEL[n]
        if n < nivel_actual:
            partes.append(f"✅ Nv{n}")
        elif n == nivel_actual:
            partes.append(f"🔥 Nv{n}")
        else:
            partes.append(f"❓ Nv{n}")
    print("  " + " → ".join(partes))
    print("  " + "─" * 42 + "\n")


def descanso_entre_batallas(jugador, nivel_siguiente):
    """Pequeña curación y resumen antes de la próxima batalla."""
    curacion = int(jugador.vida_maxima * 0.30)
    jugador.vida = min(jugador.vida_maxima, jugador.vida + curacion)
    jugador.mana = jugador.mana_maximo
    jugador.hechizo_usos_restantes = jugador.hechizo_usos

    proximo = ENEMIGOS_POR_NIVEL[nivel_siguiente]
    print(f"\n  🏕️  DESCANSO ANTES DEL NIVEL {nivel_siguiente}")
    print(f"  Recuperás {curacion} HP y maná completo.")
    print(f"  HP actual: {jugador.vida}/{jugador.vida_maxima} | "
          f"Maná: {jugador.mana}/{jugador.mana_maximo}")
    print(f"\n  Próximo rival: {proximo['emoji']} {proximo['nombre']}  "
          f"(ATK:{proximo['ataque']} DEF:{proximo['defensa']} HP:{proximo['vida_maxima']})")
    input("\n  Presioná Enter para continuar...\n")


def main():
    print("\n" + "=" * 48)
    print("        ⚔️   JUEGO DE BATALLA RPG   ⚔️")
    print("        Derrotá los 10 niveles para ganar")
    print("=" * 48)

    nombre = input("\n¿Cuál es el nombre de tu personaje? ").strip() or "Héroe"
    clase = seleccionar_clase()
    jugador = Personaje(nombre, clase)
    datos_clase = CLASES[clase]

    print(f"\n✅ ¡{nombre} el {clase.capitalize()} está listo!")
    print(f"   Hechizo: {datos_clase['hechizo_nombre']} — {datos_clase['hechizo_desc']}")
    print(f"   Costo: {datos_clase['hechizo_costo_mana']} MP por uso, "
          f"{datos_clase['hechizo_usos']} usos por batalla\n")
    input("  Presioná Enter para comenzar la aventura...\n")

    for nivel_batalla in range(1, MAX_NIVELES + 1):
        mostrar_mapa(nivel_batalla)

        rival = crear_enemigo(nivel_batalla)
        combate = Batalla(jugador, rival)
        combate.ejecutar()

        # El jugador perdió
        if combate.ganador == "enemigo":
            print(f"  💀 FIN DEL JUEGO en el nivel {nivel_batalla}.")
            print(f"  {nombre} cayó ante {rival.nombre}.")
            break

        # El jugador ganó todos los niveles
        if nivel_batalla == MAX_NIVELES:
            print("\n" + "🏆" * 26)
            print(f"  ¡¡¡{nombre} COMPLETÓ LOS 10 NIVELES!!!")
            print(f"  ¡El {clase.capitalize()} más poderoso del reino!")
            print("🏆" * 26 + "\n")
            break

        # Descanso entre niveles
        descanso_entre_batallas(jugador, nivel_batalla + 1)

    ver_historial = input("¿Querés ver el resumen final de stats? (s/n): ").strip().lower()
    if ver_historial == "s":
        print(f"\n  📊 STATS FINALES DE {jugador.nombre.upper()}")
        print(f"  Nivel alcanzado : {jugador.nivel}")
        print(f"  Ataque          : {jugador.ataque}")
        print(f"  Defensa         : {jugador.defensa}")
        print(f"  Vida máxima     : {jugador.vida_maxima}")
        print(f"  Maná máximo     : {jugador.mana_maximo}\n")


if __name__ == "__main__":
    main()