from collections import defaultdict
from typing import Dict, List, TypedDict

class Tarea(TypedDict):
    titulo: str
    descripcion: str

_MEM_TAREAS: Dict[str, List[Tarea]] = defaultdict(list)

def user_key_from_request(request) -> str:
    if request.user.is_authenticated:
        return f"user_{request.user.id}"
    if not request.session.session_key:
        request.session.create()
    return f"session_{request.session.session_key}"

def get_tareas(request) -> List[Tarea]:
    return _MEM_TAREAS[user_key_from_request(request)]

def add_tarea(request, titulo: str, descripcion: str) -> None:
    _MEM_TAREAS[user_key_from_request(request)].append(
        {"titulo": titulo, "descripcion": descripcion}
    )

def get_tarea(request, indice: int) -> Tarea | None:
    tareas = get_tareas(request)
    if 0 <= indice < len(tareas):
        return tareas[indice]
    return None

def delete_tarea(request, indice: int) -> bool:
    tareas = get_tareas(request)
    if 0 <= indice < len(tareas):
        del tareas[indice]
        return True
    return False

def migrate_session_to_user(request) -> None:
    """
    Mueve tareas de la clave de sesión anónima a la clave user:<id>
    (si el usuario está autenticado). Evita duplicar en caso que ya existan.
    """
    if not request.user.is_authenticated:
        return
    # claves
    if not request.session.session_key:
        return
    session_key = f"session:{request.session.session_key}"
    user_key = f"user:{request.user.id}"
    if session_key == user_key:
        return
    session_tasks = _MEM_TAREAS.get(session_key, [])
    if session_tasks and not _MEM_TAREAS.get(user_key):
        _MEM_TAREAS[user_key].extend(session_tasks)
    if session_key in _MEM_TAREAS:
        del _MEM_TAREAS[session_key]

def update_tarea(request, indice: int, titulo: str, descripcion: str) -> bool:
    """
    Actualiza una tarea por índice. Devuelve True si se pudo actualizar.
    """
    tareas = get_tareas(request)
    if 0 <= indice < len(tareas):
        tareas[indice] = {"titulo": titulo, "descripcion": descripcion}
        return True
    return False