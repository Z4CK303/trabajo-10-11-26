from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI
from sqlmodel import Session, select

from database import canciones,crear_db_y_tablas, get_session, engine,columna_canciones

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Al iniciar la aplicación, crear la base de datos y las tablas
    crear_db_y_tablas()
    yield
    # Al finalizar la aplicación, se puede realizar limpieza si es necesario (opcional)


app = FastAPI(lifespan=lifespan)

session_dependency = Annotated[Session, Depends(get_session)]

# Rutas de la API


# Endpoint para crear un héroe
@app.post("/playlists", response_model=canciones)
def create_playlist(playlist: columna_canciones, session: session_dependency):
    new_song = canciones.model_validate(playlist)
    session.add(new_song)
    session.commit()
    session.refresh(new_song)
    return new_song


# Endpoint para obtener todos los héroes
@app.get("/playlists", response_model=list[canciones])
def ver_playlists(session: session_dependency):
    consulta = select(canciones)
    return session.exec(consulta).all()


# Endpoint para borrar un héroe por su ID
@app.delete("/playlists/{playlist_id}", response_model=canciones)
def delete_playlist(playlist_id: int, session: session_dependency):
    playlist = session.get(canciones, playlist_id)
    if playlist is None:
        return {"error": "Playlist no encontrada"}
    data = canciones.model_validate(playlist)
    session.delete(playlist)
    session.commit()
    return data


# Endpoint para actualizar un héroe por su ID
@app.put("/playlists/{playlist_id}", response_model=canciones)
def update_playlist(playlist_id: int, updated_playlist: columna_canciones, session: session_dependency):
    playlist = session.get(columna_canciones, playlist_id)
    if playlist is None:
        return {"error": "Playlist no encontrada"}

    playlist.titulo = updated_playlist.titulo
    playlist.artista = updated_playlist.artista
    playlist.genero = updated_playlist.genero
    playlist.duracion = updated_playlist.duracion
    playlist.favorito = updated_playlist.favorito

    session.add(playlist)
    session.commit()
    session.refresh(playlist)

    return playlist

@app.get("/playlists/{playlist_id}", response_model=canciones)
def get_playlist(playlist_id: int, session: session_dependency):
    playlist = session.get(canciones, playlist_id)
    if playlist is None:
        return {"error": "Playlist no encontrada"}
    return playlist