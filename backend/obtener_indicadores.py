import bcchapi
import numpy as np

siete = bcchapi.Siete(file="credenciales.txt")

df = siete.cuadro(
    series=[
        "F073.TCO.PRE.Z.D",     # Dólar observado
        "F066.UF.VRA.Z.D",      # UF
        "G073.IPC.INDEX.2018.M" # IPC
    ],
    nombres=["dolar", "uf", "ipc"],
    desde="2024-06-01",
    hasta="2024-06-28",
    frecuencia="D",  # Para IPC mensual, podrías usar "M"
    observado={
        "dolar": "last",
        "uf": "last",
        "ipc": "last"
    }
)

print(df)
