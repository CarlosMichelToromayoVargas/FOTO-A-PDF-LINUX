import tkinter as tk
from tkinter import messagebox
from PIL import Image
from datetime import datetime
import os
import time
import subprocess

class ToromayoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Toromayo")
        
        # --- DISEÑO ULTRA COMPACTO ---
        VENTANA_ANCHO = 180
        VENTANA_ALTO = 250
        
        pantalla_ancho = self.root.winfo_screenwidth()
        pantalla_alto = self.root.winfo_screenheight()
        pos_x = int(pantalla_ancho - (VENTANA_ANCHO + 40))
        pos_y = int((pantalla_alto / 2) - (VENTANA_ALTO / 2))
        self.root.geometry(f"{VENTANA_ANCHO}x{VENTANA_ALTO}+{pos_x}+{pos_y}")
        self.root.resizable(False, False)
        self.root.configure(bg="#070707")
        
        self.lista_capturas = []

        # 1. TÍTULO DE LA EMPRESA
        self.lbl_title = tk.Label(root, text="👑 𝐓𝐎𝐑𝐎𝐌𝐀𝐘𝐎 𝐒𝐑𝐋 👑", font=("Arial", 10, "bold"), bg="#030303", fg="white")
        self.lbl_title.pack(pady=10)
        
        # 2. BOTÓN: CAPTURAR IMAGEN
        self.btn_capture = tk.Button(
            root, text="𝐂𝐀𝐏𝐓𝐔𝐑𝐀𝐑 𝐂𝐔𝐀𝐃𝐑𝐎", font=("Arial", 9, "bold"),
            bg="#1410FF", fg="white", activebackground="#11E3FF", activeforeground="white",
            bd=2, relief="raised", command=self.captura_interactiva_linux
        )
        self.btn_capture.pack(fill="x", padx=15, pady=4)
        
        # 3. BOTÓN: BORRAR ÚLTIMA
        self.btn_clear = tk.Button(
            root, text="𝐁𝐎𝐑𝐑𝐀𝐑", font=("Arial", 12, "bold"),
            bg="#FF1900", fg="white", activebackground="#BD1300", activeforeground="white",
            bd=2, relief="raised", command=self.borrar_ultima_captura
        )
        self.btn_clear.pack(fill="x", padx=15, pady=4)
        
        # 4. RECUADRO NUMÉRICO (CONTADOR)
        self.display_frame = tk.Frame(root, bg="white", bd=2, relief="sunken")
        self.display_frame.pack(fill="both", expand=True, padx=15, pady=8)
        
        self.lbl_number = tk.Label(self.display_frame, text="0", font=("Arial", 34, "bold"), bg="white", fg="#050505")
        self.lbl_number.pack(expand=True)
        
        # 5. BOTÓN ÚNICO: GUARDAR PDF
        self.btn_pdf = tk.Button(
            root, text="GUARDAR PDF", font=("Arial", 12, "bold"),
            bg="#F11FE0", fg="white", activebackground="#9C0D7D", activeforeground="white",
            bd=2, relief="raised", command=self.generar_pdf
        )
        self.btn_pdf.pack(fill="x", padx=15, pady=(4, 15))

    # --- LÓGICA DE CAPTURA INTERACTIVA ---
    def captura_interactiva_linux(self):
        self.root.withdraw()
        self.root.update()
        time.sleep(0.4)
        
        nombre_archivo = f"captura_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        try:
            # MEJORA: Se añade -q 100 para capturar el pixel puro de la pantalla sin compresión inicial
            comando = f"scrot -s -q 100 {nombre_archivo}"
            subprocess.run(comando, shell=True)
            
            if os.path.exists(nombre_archivo):
                self.lista_capturas.append(nombre_archivo)
                self.lbl_number.config(text=str(len(self.lista_capturas)))
            
        except Exception as e:
            messagebox.showerror("Error de Sistema", f"No se pudo capturar: {e}")
            
        self.root.deiconify()

    def borrar_ultima_captura(self):
        if self.lista_capturas:
            archivo_a_borrar = self.lista_capturas.pop()
            if os.path.exists(archivo_a_borrar):
                os.remove(archivo_a_borrar)
            self.lbl_number.config(text=str(len(self.lista_capturas)))
        else:
            messagebox.showwarning("Toromayo", "No hay capturas en el historial.")

    # --- FUNCIÓN PDF DE ALTA DENSIDAD ULTRA ---
    def generar_pdf(self):
        if not self.lista_capturas:
            messagebox.showwarning("Toromayo", "No tienes capturas para armar el documento.")
            return
        try:
            imagenes_pil = []
            for f in self.lista_capturas:
                img = Image.open(f).convert("RGB")
                
                # Súper escalado a 4X: Multiplica masivamente la densidad de pixeles
                nuevo_ancho = img.width * 4
                nuevo_alto = img.height * 4
                
                # Filtro Lanczos de Pillow + remuestreo de bordes limpios
                img_alta_res = img.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
                imagenes_pil.append(img_alta_res)
            
            nombre_pdf = f"Reporte_Toromayo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            # Forzamos compresión lossless interna en el contenedor PDF
            opciones_guardado = {
                "dpi": (600, 600),       # Resolución Ultra-HD de impresión física 
                "quality": 100,          # Calidad al máximo absoluto sin degradar color
                "subsampling": 0         # Desactiva submuestreo de croma (mantiene textos hiper-nítidos)
            }
            
            if len(imagenes_pil) == 1:
                imagenes_pil[0].save(nombre_pdf, **opciones_guardado)
            else:
                imagenes_pil[0].save(nombre_pdf, save_all=True, append_images=imagenes_pil[1:], **opciones_guardado)
            
            # Limpieza limpia de temporales
            for f in self.lista_capturas:
                if os.path.exists(f):
                    os.remove(f)
            
            messagebox.showinfo("Éxito", f"¡PDF Generado en Ultra-HD!\nNombre: {nombre_pdf}")
            
            self.lista_capturas.clear()
            self.lbl_number.config(text="0")
        except Exception as e:
            messagebox.showerror("Error PDF", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ToromayoApp(root)
    root.mainloop()
