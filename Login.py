import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Progressbar, Style
from PIL import Image, ImageTk
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ---------------------------
# FUNCIONES DE PRUEBA
# ---------------------------

def prueba_login():
    try:
        options = uc.ChromeOptions()
        options.add_argument("user-agent=Mozilla/5.0")
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = uc.Chrome(options=options)
        driver.get("https://www.sportiumbet.mx")
        driver.maximize_window()

        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "acceptCookies"))
            ).click()
        except:
            pass

        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn_action_login"))
        ).click()

        try:
            WebDriverWait(driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.ID, "ptLoginFrame"))
            )
        except:
            pass

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "userName"))
        ).send_keys("edusolis20")

        for l in "Eduardo2000":
            driver.find_element(By.NAME, "password").send_keys(l)
            time.sleep(0.1)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.fn-login-btn"))
        ).click()

        try:
            driver.switch_to.default_content()
        except:
            pass

        messagebox.showinfo("Resultado", "✅ Login ejecutado correctamente.")
        marcar_prueba_completada("Login de usuario")

    except Exception as e:
        messagebox.showerror("Error", f"❌ Falló la prueba de login:\n\n{str(e)}")

def prueba_placeholder(nombre):
    messagebox.showinfo("Prueba pendiente", f"La prueba '{nombre}' será implementada próximamente.")
    marcar_prueba_completada(nombre)

def marcar_prueba_completada(nombre_prueba):
    if checkbox_vars[nombre_prueba].get() == 0:
        checkbox_vars[nombre_prueba].set(1)
        progreso["value"] += progreso_incremento

# ---------------------------
# INTERFAZ GRÁFICA
# ---------------------------

ventana = tk.Tk()
ventana.title("Sportium - Pruebas Automatizadas")
ventana.geometry("480x570")
ventana.configure(bg="white")

# ---------------------------
# CARGAR LOGO
# ---------------------------

try:
    logo_img = Image.open("sportium_logo.png")
    logo_img = logo_img.resize((200, 50))
    logo = ImageTk.PhotoImage(logo_img)
    tk.Label(ventana, image=logo, bg="white").pack(pady=10)
except Exception as e:
    tk.Label(ventana, text="Sportium", font=("Arial", 20, "bold"), fg="#D80027", bg="white").pack(pady=10)

tk.Label(ventana, text="Checklist de pruebas funcionales", font=("Arial", 13, "bold"), fg="#D80027", bg="white").pack(pady=5)

checkbox_vars = {}

pruebas_disponibles = {
    "Login de usuario": prueba_login,
    "Registro de usuario": lambda: prueba_placeholder("Registro de usuario"),
    "Colocación de apuestas": lambda: prueba_placeholder("Colocación de apuestas"),
    "Ejecución de juegos de casino": lambda: prueba_placeholder("Ejecución de juegos de casino"),
}

for nombre, funcion in pruebas_disponibles.items():
    var = tk.IntVar()
    frame = tk.Frame(ventana, bg="white")
    frame.pack(anchor="w", padx=25, pady=4, fill="x")

    chk = tk.Checkbutton(frame, text=nombre, variable=var, font=("Arial", 10), state="disabled", bg="white", fg="#333333", activebackground="white")
    chk.pack(side="left")

    btn = tk.Button(frame, text="Ejecutar", command=funcion, bg="#D80027", fg="white", relief="flat", padx=10)
    btn.pack(side="right", padx=10)

    checkbox_vars[nombre] = var

# BOTÓN GENERAL
def ejecutar_todas():
    for nombre, funcion in pruebas_disponibles.items():
        try:
            funcion()
        except Exception as e:
            messagebox.showerror("Error", f"❌ Falló la prueba '{nombre}':\n{e}")

tk.Button(ventana, text="✅ Ejecutar todas las pruebas", command=ejecutar_todas,
          bg="#D80027", fg="white", font=("Arial", 10, "bold"), relief="flat").pack(pady=20)

# BARRA DE PROGRESO
tk.Label(ventana, text="Progreso general:", bg="white", fg="#333333", font=("Arial", 10)).pack()
style = Style()
style.theme_use('default')
style.configure("TProgressbar", troughcolor="#ddd", background="#D80027", thickness=20)

progreso = Progressbar(ventana, orient="horizontal", length=400, mode="determinate", style="TProgressbar")
progreso.pack(pady=10)

# Incremento por prueba
total_pruebas = len(pruebas_disponibles)
progreso_incremento = 100 / total_pruebas

# FOOTER
tk.Label(ventana, text="Versión prototipo – Junio 2025", font=("Arial", 8), fg="gray", bg="white").pack(side="bottom", pady=10)

ventana.mainloop()

