# tareas/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthFlowTests(TestCase):
    def test_lista_redirige_si_no_autenticado(self):
        resp = self.client.get(reverse("tareas:lista"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/cuentas/login/", resp["Location"])

    def test_registro_crea_usuario_y_loguea(self):
        resp = self.client.post(
            reverse("tareas:registro"),
            data={"username": "tatu", "password1": "ClaveFuerte123", "password2": "ClaveFuerte123"},
            follow=True,
        )
        self.assertEqual(resp.status_code, 200)
        # ya debería poder ver la lista (logueado)
        self.assertContains(resp, "Mis tareas")

class TareasFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("tatu", password="ClaveFuerte123")
        self.client.login(username="tatu", password="ClaveFuerte123")

    def test_agregar_tarea(self):
        resp = self.client.post(reverse("tareas:agregar"), data={"titulo": "Llamar", "descripcion": "a X"}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Llamar")  # aparece en la lista

    def test_eliminar_tarea(self):
        # crear primero
        self.client.post(reverse("tareas:agregar"), data={"titulo": "Temporal", "descripcion": ""}, follow=True)
        # eliminar índice 0
        resp = self.client.post(reverse("tareas:eliminar", args=[0]), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertNotContains(resp, "Temporal")

    def test_aislamiento_por_usuario(self):
        # usuario A crea tarea
        self.client.post(reverse("tareas:agregar"), data={"titulo": "Solo A", "descripcion": ""}, follow=True)

        # usuario B no debe verla
        self.client.logout()
        User.objects.create_user("otra", password="ClaveFuerte123")
        self.client.login(username="otra", password="ClaveFuerte123")

        resp = self.client.get(reverse("tareas:lista"))
        self.assertEqual(resp.status_code, 200)
        self.assertNotContains(resp, "Solo A")

def test_editar_tarea(self):
    # Crear una tarea
    self.client.post(reverse("tareas:agregar"), data={"titulo": "Original", "descripcion": "A"}, follow=True)
    # Editarla
    resp = self.client.post(reverse("tareas:editar", args=[0]),
                            data={"titulo": "Editada", "descripcion": "B"},
                            follow=True)
    self.assertEqual(resp.status_code, 200)
    self.assertContains(resp, "Editada")
    self.assertNotContains(resp, "Original")