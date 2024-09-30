import bcrypt
from sqlalchemy.orm import Session, sessionmaker
from database import Usuario, motor

# Función para registrar un nuevo usuario


def registrar_usuario(nombre_usuario: str, correo_electronico: str, telefono: str, contrasenya: str, db: Session):
    # usamos bcrypt para encriptar la contraseña
    hash_contrasenya = bcrypt.hashpw(
        contrasenya.encode('utf-8'), bcrypt.gensalt())

    # Crear una nueva instancia de Usuario
    nuevo_usuario = Usuario(
        nombre_usuario=nombre_usuario,
        correo_electronico=correo_electronico,
        telefono=telefono,
        hash_contrasenya=hash_contrasenya.decode(
            'utf-8')  # Almacenar como string
    )

    # Agregar a la sesión y guardar en la base de datos
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

# Función para autenticar un usuario


def autenticar_usuario(nombre_usuario: str, contrasenya: str, db: Session):
    usuario = db.query(Usuario).filter(
        Usuario.nombre_usuario == nombre_usuario).first()

    if usuario and bcrypt.checkpw(contrasenya.encode('utf-8'), usuario.hash_contrasenya.encode('utf-8')):
        return usuario  # Autenticación ok
    return None  # Autenticación ko

# Crear una sesión de base de datos


def obtener_sesion():
    SessionLocal = sessionmaker(bind=motor)
    return SessionLocal()
