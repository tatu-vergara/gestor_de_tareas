from django.shortcuts import render, redirect
from django.http import Http404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import TareaForm
from .memstore import (
    get_tareas, get_tarea, add_tarea, delete_tarea, migrate_session_to_user, update_tarea
)

@login_required
def lista_tareas(request):
    migrate_session_to_user(request)
    tareas = get_tareas(request)
    return render(request, "tareas/lista.html", {"tareas": tareas})

@login_required
def detalle_tarea(request, indice: int):
    tarea = get_tarea(request, indice)
    if tarea is None:
        raise Http404("Tarea no encontrada")
    return render(request, "tareas/detalle.html", {"tarea": tarea, "indice": indice})

@login_required
def agregar_tarea(request):
    if request.method == "POST":
        form = TareaForm(request.POST)
        if form.is_valid():
            add_tarea(request, form.cleaned_data["titulo"], form.cleaned_data["descripcion"])
            return redirect(reverse("tareas:lista"))
    else:
        form = TareaForm()
    return render(request, "tareas/agregar.html", {"form": form})


@login_required
def eliminar_tarea(request, indice: int):
    if request.method == "POST":
        ok = delete_tarea(request, indice)
        if not ok:
            raise Http404("Tarea no encontrada")
        return redirect(reverse("tareas:lista"))

    tarea = get_tarea(request, indice)
    if tarea is None:
        raise Http404("Tarea no encontrada")
    return render(request, "tareas/eliminar.html", {"tarea": tarea, "indice": indice})

def registro(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Auto-login tras registrarse (mejor UX)
            login(request, user)
            # migrar tareas de sesión anónima a la cuenta
            migrate_session_to_user(request)
            messages.success(request, "¡Cuenta creada! Bienvenide ✨")
            return redirect("tareas:lista")
    else:
        form = UserCreationForm()
    return render(request, "tareas/registro.html", {"form": form})

@login_required
def editar_tarea(request, indice: int):
    tarea = get_tarea(request, indice)
    if tarea is None:
        raise Http404("Tarea no encontrada")

    if request.method == "POST":
        form = TareaForm(request.POST)
        if form.is_valid():
            ok = update_tarea(request, indice, form.cleaned_data["titulo"], form.cleaned_data["descripcion"])
            if not ok:
                raise Http404("Tarea no encontrada")
            messages.success(request, "Tarea actualizada.")
            return redirect("tareas:detalle", indice=indice)
    else:
        # Precarga con los datos existentes
        form = TareaForm(initial={"titulo": tarea["titulo"], "descripcion": tarea["descripcion"]})

    return render(request, "tareas/editar.html", {"form": form, "indice": indice})