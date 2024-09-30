from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Configuración de la base de datos SQLite
URL_BASE_DATOS = "sqlite:///bjjfit.db"

# Crear un motor y una base
motor = create_engine(URL_BASE_DATOS)
Base = declarative_base()

# Definir los modelos


class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String, unique=True, index=True)
    correo_electronico = Column(String, unique=True, index=True)
    telefono = Column(String)
    # Para almacenar la contraseña de forma segura
    hash_contrasenya = Column(String)


class Clase(Base):
    __tablename__ = 'clases'

    id = Column(Integer, primary_key=True, index=True)
    tipo_clase = Column(String)  # Bjj, MMA, Grappling, etc
    horario = Column(DateTime)
    descripcion = Column(String)


class Reserva(Base):
    __tablename__ = 'reservas'

    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'))
    id_clase = Column(Integer, ForeignKey('clases.id'))

    usuario = relationship("Usuario", back_populates="reservas")
    clase = relationship("Clase", back_populates="reservas")


class Ubicacion(Base):
    __tablename__ = 'ubicaciones'

    id = Column(Integer, primary_key=True, index=True)
    direccion = Column(String, nullable=False)
    ciudad = Column(String, nullable=False)
    estado = Column(String, nullable=False)
    codigo_postal = Column(String, nullable=False)
    telefono_contacto = Column(String, nullable=False)
    correo_contacto = Column(String, nullable=False)


Usuario.reservas = relationship("Reserva", back_populates="usuario")
Clase.reservas = relationship("Reserva", back_populates="clase")

# Crear las tablas en la base de datos


def crear_base_datos():
    Base.metadata.create_all(bind=motor)


if __name__ == "__main__":
    crear_base_datos()
