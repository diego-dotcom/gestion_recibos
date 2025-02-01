import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from db_manager import DBManager
from datetime import datetime
from emite_pdf import emitir_pdf  

class ClienteApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Clientes")
        self.geometry("550x650")

        self.db = DBManager()

        # --- Crear Tabview para manejar las solapas ---
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)

        # --- Solapa de Gestión de Clientes ---
        self.tab_clientes = self.tabview.add("Clientes")
        self.cliente_frame = ClienteFrame(self.tab_clientes, self.db)
        self.cliente_frame.pack(fill="both", expand=True)

        # --- Solapa de Emisión de Recibos ---
        self.tab_recibos = self.tabview.add("Recibos")
        self.recibo_frame = ReciboFrame(self.tab_recibos, self.db)
        self.recibo_frame.pack(fill="both", expand=True)

class ClienteFrame(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db

        # Formulario de Cliente

        # --- Formulario ---
        self.frame_formulario = ctk.CTkFrame(self)
        self.frame_formulario.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(self.frame_formulario, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nombre = ctk.CTkEntry(self.frame_formulario, width=200)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(self.frame_formulario, text="CUIT:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_cuit = ctk.CTkEntry(self.frame_formulario, width=200)
        self.entry_cuit.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(self.frame_formulario, text="Dirección:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_direccion = ctk.CTkEntry(self.frame_formulario, width=200)
        self.entry_direccion.grid(row=2, column=1, padx=5, pady=5)

        # --- Botones ---
        self.btn_agregar = ctk.CTkButton(self.frame_formulario, text="Agregar Cliente", command=self.agregar_cliente)
        self.btn_agregar.grid(row=3, column=0, columnspan=2, pady=5)

        self.btn_editar = ctk.CTkButton(self.frame_formulario, text="Actualizar Cliente", command=self.actualizar_cliente, state="disabled")
        self.btn_editar.grid(row=4, column=0, columnspan=2, pady=5)

        self.btn_eliminar = ctk.CTkButton(self.frame_formulario, text="Eliminar Cliente", command=self.eliminar_cliente, state="disabled")
        self.btn_eliminar.grid(row=5, column=0, columnspan=2, pady=5)

        # --- Treeview para mostrar clientes ---
        self.tree = ttk.Treeview(self, columns=("ID", "Nombre", "CUIT", "Dirección"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("CUIT", text="CUIT")
        self.tree.heading("Dirección", text="Dirección")

        self.tree.column("ID", width=30, anchor="center")
        self.tree.column("Nombre", width=150)
        self.tree.column("CUIT", width=120, anchor="center")
        self.tree.column("Dirección", width=200)

        self.tree.pack(pady=10, fill="both", expand=True)
        self.tree.bind("<Double-1>", self.seleccionar_cliente)

        self.mostrar_clientes()

    def agregar_cliente(self):
        """Agrega un nuevo cliente a la base de datos."""
        nombre = self.entry_nombre.get()
        cuit = self.entry_cuit.get()
        direccion = self.entry_direccion.get()

        if not nombre or not cuit or not direccion:
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return

        if self.db.agregar_cliente(nombre, cuit, direccion):
            messagebox.showinfo("Éxito", "Cliente agregado correctamente")
            self.mostrar_clientes()
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", "El CUIT ya está registrado")

    def mostrar_clientes(self):
        """Carga los clientes en el Treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        clientes = self.db.obtener_clientes()
        for cliente in clientes:
            self.tree.insert("", "end", values=cliente)

    def seleccionar_cliente(self, event):
        """Carga los datos del cliente seleccionado en los campos y deshabilita 'Agregar Cliente'."""
        selected_item = self.tree.focus()
        if not selected_item:
            return

        values = self.tree.item(selected_item, "values")
        if values:
            self.entry_nombre.delete(0, "end")
            self.entry_cuit.delete(0, "end")
            self.entry_direccion.delete(0, "end")

            self.entry_nombre.insert(0, values[1])
            self.entry_cuit.insert(0, values[2])
            self.entry_direccion.insert(0, values[3])

            self.btn_editar.configure(state="normal")
            self.btn_eliminar.configure(state="normal")
            self.btn_agregar.configure(state="disabled")  # 🚨 Deshabilita 'Agregar Cliente'

            self.selected_id = values[0]

    def actualizar_cliente(self):
        """Actualiza los datos de un cliente existente."""
        if not hasattr(self, 'selected_id'):
            return

        nombre = self.entry_nombre.get()
        cuit = self.entry_cuit.get()
        direccion = self.entry_direccion.get()

        if not nombre or not cuit or not direccion:
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return

        self.db.actualizar_cliente(self.selected_id, nombre, cuit, direccion)
        messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
        self.mostrar_clientes()
        self.limpiar_campos()

    def eliminar_cliente(self):
        """Elimina un cliente de la base de datos."""
        if not hasattr(self, 'selected_id'):
            return

        if messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar este cliente?"):
            self.db.eliminar_cliente(self.selected_id)
            messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
            self.mostrar_clientes()
            self.limpiar_campos()

    def limpiar_campos(self):
        """Limpia los campos y re-habilita 'Agregar Cliente'."""
        self.entry_nombre.delete(0, "end")
        self.entry_cuit.delete(0, "end")
        self.entry_direccion.delete(0, "end")

        self.btn_editar.configure(state="disabled")
        self.btn_eliminar.configure(state="disabled")
        self.btn_agregar.configure(state="normal")  # ✅ Se vuelve a habilitar 'Agregar Cliente'

        self.selected_id = None

class ReciboFrame(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.conceptos = []

        # Selección de Cliente
        ctk.CTkLabel(self, text="Seleccionar Cliente:").grid(row=0, column=0, padx=5, pady=5)
        self.combo_clientes = ctk.CTkComboBox(self, values=self.obtener_clientes(), width=250)
        self.combo_clientes.grid(row=0, column=1, padx=5, pady=5)

        # Tabla de conceptos
        self.tree = ttk.Treeview(self, columns=("Concepto", "Valor"), show="headings")
        self.tree.heading("Concepto", text="Concepto")
        self.tree.heading("Valor", text="Valor")
        self.tree.column("Concepto", width=200)
        self.tree.column("Valor", width=100, anchor="center")
        self.tree.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Formulario para agregar conceptos
        ctk.CTkLabel(self, text="Concepto:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_concepto = ctk.CTkEntry(self, width=200)
        self.entry_concepto.grid(row=2, column=1, padx=5, pady=5)

        ctk.CTkLabel(self, text="Valor:").grid(row=3, column=0, padx=5, pady=5)
        self.entry_valor = ctk.CTkEntry(self, width=200)
        self.entry_valor.grid(row=3, column=1, padx=5, pady=5)

        # Botón para agregar concepto
        self.btn_agregar_concepto = ctk.CTkButton(self, text="Agregar Concepto", command=self.agregar_concepto)
        self.btn_agregar_concepto.grid(row=4, column=0, columnspan=2, pady=5)

        # Mostrar Total
        self.label_total = ctk.CTkLabel(self, text="Total: $0.00", font=("Arial", 14, "bold"))
        self.label_total.grid(row=5, column=0, columnspan=2, pady=10)

        # Botón para emitir el recibo
        self.btn_emitir = ctk.CTkButton(self, text="Emitir", command=self.emitir_recibo)
        self.btn_emitir.grid(row=6, column=0, columnspan=2, pady=10)

    def obtener_clientes(self):
        """Obtiene la lista de clientes de la base de datos."""
        clientes = self.db.obtener_clientes()
        return [f"{c[0]} - {c[1]}" for c in clientes]

    def agregar_concepto(self):
        """Agrega un concepto con su valor a la tabla y actualiza el total."""
        concepto = self.entry_concepto.get()
        valor = self.entry_valor.get()

        if not concepto or not valor:
            messagebox.showwarning("Error", "Debe ingresar un concepto y su valor.")
            return

        try:
            valor = float(valor)
        except ValueError:
            messagebox.showwarning("Error", "El valor debe ser un número válido.")
            return

        self.tree.insert("", "end", values=(concepto, f"${valor:.2f}"))
        self.conceptos.append((concepto, valor))
        self.actualizar_total()

        # Limpiar entradas
        self.entry_concepto.delete(0, "end")
        self.entry_valor.delete(0, "end")

    def actualizar_total(self):
        """Calcula y actualiza el total de los valores ingresados."""
        total = sum(valor for _, valor in self.conceptos)
        self.label_total.configure(text=f"Total: ${total:.2f}")

    def limpiar_formulario(self):
        """Limpia la tabla de conceptos y reinicia el total."""
        self.tree.delete(*self.tree.get_children())  # Borra todos los elementos de la tabla
        self.conceptos.clear()  # Borra la lista de conceptos
        self.label_total.configure(text="Total: $0.00")  # Reinicia el total


    def emitir_recibo(self):
        """Prepara los datos y emite el recibo en PDF."""
        cliente_seleccionado = self.combo_clientes.get()

        if not cliente_seleccionado:
            messagebox.showwarning("Error", "Debe seleccionar un cliente.")
            return
        
        if not self.conceptos:
            messagebox.showwarning("Error", "Debe agregar al menos un concepto.")
            return

        cliente_id, cliente_nombre = cliente_seleccionado.split(" - ", 1)
        cliente_info = self.db.obtener_cliente_por_id(cliente_id)

        if not cliente_info:
            messagebox.showwarning("Error", "Cliente no encontrado en la base de datos.")
            return

        direccion, cuit = cliente_info[1], cliente_info[0]  # Dirección y CUIT en la DB

        fecha = datetime.now().strftime("%d/%m/%Y")
        numero = "00001"  # Aquí podrías agregar una lógica para numeración automática

        # Llamar a la función que genera el PDF
        emitir_pdf(fecha, numero, cliente_nombre, direccion, cuit, self.conceptos)

        messagebox.showinfo("Éxito", "Recibo emitido correctamente.")

        # Limpiar el formulario después de emitir el recibo
        self.limpiar_formulario()


