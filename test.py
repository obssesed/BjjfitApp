from usuarios import registrar_usuario, autenticar_usuario, obtener_sesion


def main():
    # Obtener sesión de la base de datos
    db = obtener_sesion()

    # Probar el registro de usuario
    nuevo_usuario = registrar_usuario(
        nombre_usuario="victor",
        correo_electronico="victor@example.com",
        telefono="123456789",
        contrasenya="contrasena123",
        db=db
    )
    print(f"Usuario registrado: {nuevo_usuario.nombre_usuario}")

    # Probar autenticación
    usuario_autenticado = autenticar_usuario("victor", "contrasena123", db)
    if usuario_autenticado:
        print(f"Usuario autenticado: {usuario_autenticado.nombre_usuario}")
    else:
        print("Autenticación fallida")


if __name__ == "__main__":
    main()
