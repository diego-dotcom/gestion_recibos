import sqlite3

DB_NAME = "clientes.db"

class DBManager:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()
        self.crear_tabla()

    def crear_tabla(self):
        """Crea la tabla de clientes si no existe."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                cuit TEXT NOT NULL UNIQUE,
                direccion TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def agregar_cliente(self, nombre, cuit, direccion):
        """Agrega un nuevo cliente."""
        try:
            self.cursor.execute("INSERT INTO clientes (nombre, cuit, direccion) VALUES (?, ?, ?)", (nombre, cuit, direccion))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def obtener_clientes(self):
        """Devuelve todos los clientes."""
        self.cursor.execute("SELECT * FROM clientes")
        return self.cursor.fetchall()
    
    def obtener_cliente_por_id(self, cliente_id):
        """Obtiene la dirección y el CUIT de un cliente por su ID."""
        self.cursor.execute("SELECT cuit, direccion FROM clientes WHERE id = ?", (cliente_id,))
        return self.cursor.fetchone()  # Retorna (cuit, direccion) o None si no existe

    def actualizar_cliente(self, cliente_id, nombre, cuit, direccion):
        """Actualiza un cliente."""
        self.cursor.execute("UPDATE clientes SET nombre=?, cuit=?, direccion=? WHERE id=?", (nombre, cuit, direccion, cliente_id))
        self.conn.commit()

    def eliminar_cliente(self, cliente_id):
        """Elimina un cliente."""
        self.cursor.execute("DELETE FROM clientes WHERE id=?", (cliente_id,))
        self.conn.commit()
