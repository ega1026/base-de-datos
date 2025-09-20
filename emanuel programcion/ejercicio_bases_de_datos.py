import sqlite3

# -------------------------------
# Conexión y creación de base de datos
# -------------------------------
conn = sqlite3.connect("tienda.db")
cursor = conn.cursor()

# -------------------------------
# Creación de tablas
# -------------------------------
cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo_documento VARCHAR(50),
        documento VARCHAR(50) UNIQUE,
        nombre VARCHAR(40),
        apellidos VARCHAR(40),
        telefono VARCHAR(10),
        email VARCHAR(40) UNIQUE,
        direccion VARCHAR(80),
        municipio VARCHAR(40),
        departamento VARCHAR(40),
        pais VARCHAR(40)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo INTEGER UNIQUE,
        nombre VARCHAR(50) UNIQUE,
        categoria VARCHAR(50),
        precio REAL,
        stock INTEGER,
        iva REAL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS unidades (
        codigo TEXT PRIMARY KEY,
        nombre TEXT NOT NULL UNIQUE,
        cantidad REAL NOT NULL
    )
''')

# -------------------------------
# Funciones de CLIENTES
# -------------------------------
def agregar_cliente():
    while True:
        tipo_documento = input("Tipo de documento: ").capitalize()

        while True:
            documento = input("Número de documento: ")
            cursor.execute("SELECT * FROM clientes WHERE documento = ?", (documento,))
            if cursor.fetchone():
                print(f"El documento '{documento}' ya existe. Intente con otro.")
            else:
                break

        nombre = input("Nombre: ").capitalize()
        apellidos = input("Apellidos: ").capitalize()
        telefono = input("Teléfono: ")

        while True:
            email = input("Email: ")
            cursor.execute("SELECT * FROM clientes WHERE email = ?", (email,))
            if cursor.fetchone():
                print(f"El email '{email}' ya está registrado. Intente con otro.")
            else:
                break

        direccion = input("Dirección: ").capitalize()
        municipio = input("Municipio: ").capitalize()
        departamento = input("Departamento: ").capitalize()
        pais = input("País: ").capitalize()

        cursor.execute('''INSERT INTO clientes
                           (tipo_documento, documento, nombre, apellidos, telefono, email, direccion, municipio, departamento, pais)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                         (tipo_documento, documento, nombre, apellidos, telefono, email, direccion, municipio, departamento, pais))
        conn.commit()
        print("Cliente agregado con éxito.")

        salir = input("¿Desea agregar otro cliente? (s/n): ").lower()
        if salir != 's':
            break

def ver_clientes():
    print("\nClientes registrados:")
    cursor.execute("SELECT tipo_documento, documento, nombre, apellidos, telefono, email, direccion, municipio, departamento, pais FROM clientes")
    clientes = cursor.fetchall()

    if not clientes:
        print("No hay clientes registrados.")
        return

    headers = ['Tipo Doc.', 'Documento', 'Nombre', 'Apellidos', 'Teléfono', 'Email', 'Dirección', 'Municipio', 'Departamento', 'País']
    
    # Calcular el ancho máximo para cada columna
    column_widths = [len(header) for header in headers]
    for cliente in clientes:
        for i, item in enumerate(cliente):
            if len(str(item)) > column_widths[i]:
                column_widths[i] = len(str(item))

    # Construir la cadena de formato
    format_string = ""
    for width in column_widths:
        format_string += f"{{:<{width+3}}}" # Añade un pequeño espacio extra

    # Imprimir encabezados
    print(format_string.format(*headers))
    print("-" * (sum(column_widths) + len(column_widths) * 3))

    # Imprimir filas
    for cliente in clientes:
        print(format_string.format(*cliente))

# -------------------------------
# Funciones de PRODUCTOS
# -------------------------------
def agregar_producto():
    while True:
        while True:
            try:
                codigo = int(input("Código del producto: "))
            except ValueError:
                print("Código inválido, debe ser un número.")
                continue
            cursor.execute("SELECT * FROM productos WHERE codigo = ?", (codigo,))
            if cursor.fetchone():
                print(f"El código '{codigo}' ya existe. Intente con otro.")
            else:
                break

        while True:
            nombre = input("Nombre del producto: ").capitalize()
            cursor.execute("SELECT * FROM productos WHERE nombre = ?", (nombre,))
            if cursor.fetchone():
                print(f"El producto '{nombre}' ya existe. Intente con otro.")
            else:
                break

        categoria = input("Categoría: ").capitalize()

        try:
            precio = float(input("Precio unitario: "))
            stock = int(input("Cantidad en stock: "))
            iva = float(input("IVA (%) del producto (ejemplo: 19): "))
        except ValueError:
            print("Datos numéricos inválidos.")
            continue

        cursor.execute('''INSERT INTO productos
            (codigo, nombre, categoria, precio, stock, iva)
            VALUES (?, ?, ?, ?, ?, ?)''',
            (codigo, nombre, categoria, precio, stock, iva))
        conn.commit()
        print(f"Producto '{nombre}' agregado.")

        salir = input("¿Desea agregar otro producto? (s/n): ").lower()
        if salir != 's':
            break

def ver_productos():
    print("\nProductos registrados:")
    cursor.execute("SELECT codigo, nombre, categoria, stock, precio, iva FROM productos")
    productos = cursor.fetchall()
    if productos:
        print(f"{'Código':<8} {'Nombre':<15} {'Categoría':<15} {'Stock':<8} {'Precio':<10} {'IVA':<5}")
        print("-" * 65)
        for p in productos:
            print(f"{p[0]:<8} {p[1]:<15} {p[2]:<15} {p[3]:<8} ${p[4]:<10.2f} {p[5]:<5.2f}%")
    else:
        print("No hay productos registrados.")

# -------------------------------
# Funciones de UNIDADES
# -------------------------------
def agregar_unidad():
    while True:
        while True:
            codigo = input("Código de la unidad (ej: KG, LT, UND): ").upper()
            cursor.execute("SELECT * FROM unidades WHERE codigo = ?", (codigo,))
            if cursor.fetchone():
                print(f"El código '{codigo}' ya existe. Intente con otro.")
            else:
                break

        while True:
            nombre = input("Nombre de la unidad: ").capitalize()
            cursor.execute("SELECT * FROM unidades WHERE nombre = ?", (nombre,))
            if cursor.fetchone():
                print(f"La unidad '{nombre}' ya existe. Intente con otra.")
            else:
                break

        try:
            cantidad = float(input("Cantidad que representa la unidad: "))
        except ValueError:
            print("La cantidad debe ser un número.")
            continue

        cursor.execute("INSERT INTO unidades (codigo, nombre, cantidad) VALUES (?, ?, ?)",
                         (codigo, nombre, cantidad))
        conn.commit()
        print(f"Unidad '{nombre}' con código '{codigo}' agregada con éxito.")

        salir = input("¿Desea agregar otra unidad? (s/n): ").lower()
        if salir != 's':
            break

def ver_unidades():
    print("\nUnidades registradas:")
    cursor.execute("SELECT codigo, nombre, cantidad FROM unidades")
    unidades = cursor.fetchall()
    if unidades:
        print(f"{'Código':<10} {'Nombre':<20} {'Cantidad':<10}")
        print("-" * 40)
        for u in unidades:
            print(f"{u[0]:<10} {u[1]:<20} {u[2]:<10}")
    else:
        print("No hay unidades registradas.")

# -------------------------------
# Submenús
# -------------------------------
def gestion_clientes():
    while True:
        print("\nGESTIÓN DE CLIENTES")
        print("1. Agregar cliente")
        print("2. Ver clientes")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            agregar_cliente()
        elif opcion == "2":
            ver_clientes()
        elif opcion == "3":
            break
        else:
            print("Opción no válida.")

def gestion_productos():
    while True:
        print("\nGESTIÓN DE PRODUCTOS")
        print("1. Agregar producto")
        print("2. Ver productos")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            agregar_producto()
        elif opcion == "2":
            ver_productos()
        elif opcion == "3":
            break
        else:
            print("Opción no válida.")

def gestion_unidades():
    while True:
        print("\nGESTIÓN DE UNIDADES")
        print("1. Agregar unidad")
        print("2. Ver unidades")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            agregar_unidad()
        elif opcion == "2":
            ver_unidades()
        elif opcion == "3":
            break
        else:
            print("Opción no válida.")

# -------------------------------
# Vista general
# -------------------------------
def vista_general():
    print("\n--- Vista General ---")
    ver_clientes()
    print("\n" + "="*150 + "\n")  # Separador
    ver_productos()
    print("\n" + "="*150 + "\n")  # Separador
    ver_unidades()

# -------------------------------
# Menú principal
# -------------------------------
def menu():
    while True:
        print("\nMENÚ PRINCIPAL")
        print("1. Gestión de clientes")
        print("2. Gestión de productos")
        print("3. Gestión de unidades")
        print("4. Vista general")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            gestion_clientes()
        elif opcion == "2":
            gestion_productos()
        elif opcion == "3":
            gestion_unidades()
        elif opcion == "4":
            vista_general()
        elif opcion == "5":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida, intente de nuevo.")

# -------------------------------
# Ejecutar programa
# -------------------------------
menu()
conn.close()