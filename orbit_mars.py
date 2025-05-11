import os
import spiceypy as sp
import numpy as np

# --- Ruta absoluta al meta-kernel v533 ---
METAK = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '..', 'kernels', 'mk',
        'em16_plan_v533_20250425_001.tm'
    )
)

def carga_kernels():
    """Carga el meta-kernel situándose en el directorio kernels/mk."""
    meta_dir = os.path.dirname(METAK)
    print("⤷ Cambiando directorio a:", meta_dir)
    os.chdir(meta_dir)
    tm_file = os.path.basename(METAK)
    print("⤷ Cargando meta-kernel:", tm_file)
    sp.furnsh(tm_file)

def obten_estado(fecha_str):
    """
    Devuelve (pos, vel) de Marte visto desde el Sol.
    - fecha_str: cadena, p.ej. '2025-04-27 TDB'
    """
    # convierte fecha UTC/TDB a et (segundos desde J2000)
    et = sp.str2et(fecha_str)
    # spkezr: target, et, frame, correction, observer
    state, _ = sp.spkezr("MARS", et, "J2000", "NONE", "SUN")
    pos = np.array(state[:3])
    vel = np.array(state[3:])
    return pos, vel

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  

def traza_orbita(t0_str, t1_str, pasos=200):
    """
    Traza la órbita de Marte desde t0_str hasta t1_str.
    - t0_str, t1_str: cad. tipo 'YYYY-MM-DD TDB'
    - pasos: número de puntos en el trazado
    """
    # convierte inicio y fin a ET
    et0 = sp.str2et(t0_str)
    et1 = sp.str2et(t1_str)
    ets = np.linspace(et0, et1, pasos)

    # calcula todas las posiciones
    pos = np.empty((pasos, 3))
    for i, et in enumerate(ets):
        state, _ = sp.spkezr("MARS", et, "J2000", "NONE", "SUN")
        pos[i] = state[:3]

    # dibuja en 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(pos[:,0], pos[:,1], pos[:,2], label='Órbita de Marte')
    ax.scatter(0, 0, 0, s=100, label='Sol')  # punto del Sol
    ax.set_xlabel('X (km)')
    ax.set_ylabel('Y (km)')
    ax.set_zlabel('Z (km)')
    ax.set_title(f"Órbita de Marte: {t0_str[:10]} → {t1_str[:10]}")
    ax.legend()
    plt.tight_layout()
    nombre = f"orbita_{t0_str[:10]}_{t1_str[:10]}.png"
    fig.savefig(nombre, dpi=150)
    print(f"✅ Gráfica guardada en {nombre}")

    plt.show()
    plt.show()



def main():
    carga_kernels()

    # Ejemplo: traza la órbita desde el 1 de abril al 1 de mayo de 2025
    traza_orbita("2025-04-01 TDB", "2025-05-01 TDB", pasos=300)

    sp.kclear()

if __name__ == "__main__":
    main()

