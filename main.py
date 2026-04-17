
from personaje import Personaje, CLASES
from enemigo import Enemigo
from batalla import Batalla


def seleccionar_clase():
    opciones = list(CLASES.keys())

    # Construimos las líneas dinámicamente
    lineas = []

    for i, clave in enumerate(opciones, 1):
        datos = CLASES[clave]

        lineas.append(f"[{i}] {clave.upper()} - {datos['descripcion']}")
        lineas.append(
            f"    ATK:{datos['ataque']}  DEF:{datos['defensa']}  HP:{datos['vida_maxima']}"
        )
        lineas.append(f"    Hechizo: {datos['hechizo_nombre']}")

    # Calculamos ancho máximo
    ancho = max(len(linea) for linea in lineas) + 4

    # Dibujar caja
    print("\n" + "╔" + "═" * ancho + "╗")
    titulo = "ELEGÍ TU CLASE DE PERSONAJE"
    print("║" + titulo.center(ancho) + "║")
    print("╠" + "═" * ancho + "╣")

    for i, linea in enumerate(lineas):
        print("║ " + linea.ljust(ancho - 1) + "║")

        # separador entre clases (cada 3 líneas)
        if (i + 1) % 3 == 0 and i < len(lineas) - 1:
            print("║" + "─" * ancho + "║")

    print("╚" + "═" * ancho + "╝")

    # input
    while True:
        eleccion = input("\n> Ingresá el número de tu clase: ").strip()
        if eleccion.isdigit() and 1 <= int(eleccion) <= len(opciones):
            return opciones[int(eleccion) - 1]
        print("⚠️  Opción inválida. Intentá de nuevo.")

def main():
    print("\n" + "=" * 44)
    print("       ⚔️  JUEGO DE BATALLA RPG  ⚔️")
    print("=" * 44)

    nombre = input("\n¿Cuál es el nombre de tu personaje? ").strip() or "Héroe"
    clase = seleccionar_clase()

    jugador = Personaje(nombre, clase)
    datos_clase = CLASES[clase]

    print(f"\n✅ ¡{nombre} el {clase.capitalize()} está listo!")
    print(f"   Hechizo disponible: {datos_clase['hechizo_nombre']} "
          f"({datos_clase['hechizo_usos']} usos)")
    print(f"   {datos_clase['hechizo_desc']}\n")

    # Creación del enemigo (podés ajustar según dificultad deseada)
    rival = Enemigo(nombre="Dragón Oscuro", nivel=5, ataque=18, defensa=8, vida_maxima=120)

    combate = Batalla(jugador, rival)
    combate.ejecutar()

    ver_historial = input("¿Querés ver el historial de la batalla? (s/n): ").strip().lower()
    if ver_historial == "s":
        combate.mostrar_historial()


if __name__ == "__main__":
    main()