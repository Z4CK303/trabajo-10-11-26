from sqlmodel import Field, Session, SQLModel, create_engine


class columna_canciones(SQLModel):
    titulo: str
    artista: str
    genero: str | None = Field(default=None, index=True)
    duracion: int = Field(index=True)

class canciones(columna_canciones, table=True):
    __tablename__ = "canciones"
    id: int | None = Field(default=None, primary_key=True)



nombre_archivo_sqlite = "base de datos.db"
URL_sqlite = f"sqlite:///{nombre_archivo_sqlite}"
engine = create_engine(URL_sqlite, echo=True)

def crear_db_y_tablas():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session