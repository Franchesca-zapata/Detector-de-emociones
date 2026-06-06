import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
import cv2
import requests
import os

# ==========================
# CONFIGURACIÓN
# ==========================

TEMP_DIR = "temp"

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

face_cascade = cv2.CascadeClassifier(
    "haarcascade_frontalface_default.xml"
)

# ==========================
# VENTANA
# ==========================

ventana = tk.Tk()
ventana.title("Detector de Emociones V3 - Dataset en la Nube")
ventana.geometry("850x700")

titulo = tk.Label(
    ventana,
    text="Detector de Emociones Faciales (Cloud)",
    font=("Arial",18,"bold")
)

titulo.pack(pady=15)

imagen_label = tk.Label(ventana)
imagen_label.pack()

resultado = tk.Label(
    ventana,
    text="Presione el botón para ingresar una URL",
    font=("Arial",14)
)

resultado.pack(pady=15)

# ==========================
# MOSTRAR IMAGEN
# ==========================

def mostrar_imagen(ruta):

    img = Image.open(ruta)

    img.thumbnail((500,500))

    foto = ImageTk.PhotoImage(img)

    imagen_label.config(image=foto)

    imagen_label.image = foto

# ==========================
# DESCARGAR IMAGEN
# ==========================

def descargar_imagen(url):

    archivo = os.path.join(
        TEMP_DIR,
        "imagen_cloud.jpg"
    )

    respuesta = requests.get(url)

    with open(archivo, "wb") as f:
        f.write(respuesta.content)

    return archivo

# ==========================
# ANALIZAR IMAGEN
# ==========================

def analizar():

    url = simpledialog.askstring(
        "URL",
        "Ingrese la URL de la imagen:"
    )

    if not url:
        return

    try:

        ruta = descargar_imagen(url)

        imagen = cv2.imread(ruta)

        gris = cv2.cvtColor(
            imagen,
            cv2.COLOR_BGR2GRAY
        )

        rostros = face_cascade.detectMultiScale(
            gris,
            scaleFactor=1.3,
            minNeighbors=5
        )

        if len(rostros) == 0:

            resultado.config(
                text="No se detectó ningún rostro"
            )

            mostrar_imagen(ruta)

            return

        for (x, y, w, h) in rostros:

            rostro = gris[y:y+h, x:x+w]

            brillo = rostro.mean()

            # Simulación de emociones

            if brillo > 170:
                emocion = "Sorprendido "

            elif brillo > 130:
                emocion = "Feliz "

            elif brillo > 90:
                emocion = "Triste "

            else:
                emocion = "Enojado "

            cv2.rectangle(
                imagen,
                (x, y),
                (x+w, y+h),
                (0, 255, 0),
                2
            )

            cv2.putText(
                imagen,
                emocion,
                (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            resultado.config(
                text=f"Emoción detectada: {emocion}"
            )

        salida = os.path.join(
            TEMP_DIR,
            "resultado.jpg"
        )

        cv2.imwrite(
            salida,
            imagen
        )

        mostrar_imagen(salida)

    except Exception as e:

        resultado.config(
            text=f"Error: {e}"
        )

# ==========================
# BOTÓN
# ==========================

boton = tk.Button(
    ventana,
    text="Analizar Imagen desde URL",
    command=analizar,
    width=25,
    height=2
)

boton.pack(pady=20)

ventana.mainloop()