from .domain.builders import OrdenBuilder
from django.db import transaction
from .models import Libro, Inventario, Orden


class CompraRapidaService:
    """Servicio para la lógica de compra."""

    def __init__(self, procesador_pago):
        self.procesador_pago = procesador_pago
        self.builder = OrdenBuilder()

    # --- Flujo simple: compra de un solo libro (Tutorial 1) ---

    def obtener_detalle_producto(self, libro_id):
        from .models import Libro
        libro = Libro.objects.get(id=libro_id)
        total = float(libro.precio) * 1.19
        return {'libro': libro, 'total': total}

    def procesar(self, libro_id, cantidad=1):
        from .models import Libro, Inventario
        libro = Libro.objects.get(id=libro_id)
        inv = Inventario.objects.get(libro=libro)

        if inv.cantidad < cantidad:
            raise ValueError("No hay existencias.")

        total = float(libro.precio) * 1.19

        if self.procesador_pago.pagar(total):
            inv.cantidad -= cantidad
            inv.save()
            return total
        raise ValueError("El pago no pudo procesarse.")

    # --- Flujo con Builder: orden con usuario, múltiples productos y dirección (Tutorial 2) ---

    def ejecutar_proceso_compra(self, usuario, lista_productos, direccion):
        # Uso del Builder: semántica clara y validación interna
        orden = (self.builder
            .con_usuario(usuario)
            .con_productos(lista_productos)
            .para_envio(direccion)
            .build())

        # Uso del Factory (inyectado): cambio de comportamiento sin cambio de código
        if self.procesador_pago.pagar(orden.total):
            return f"Orden {orden.id} procesada exitosamente."

        orden.delete()
        raise Exception("Error en la pasarela de pagos.")


        # --- Flujo para la API (Tutorial 3) ---

    def ejecutar_compra(self, libro_id, direccion, usuario=None):

        with transaction.atomic():
            libro = Libro.objects.get(id=libro_id)
            inv = Inventario.objects.select_for_update().get(libro=libro)

            if inv.cantidad < 1:
                raise ValueError("No hay existencias.")

            total = round(float(libro.precio) * 1.19, 2)

            if not self.procesador_pago.pagar(total):   # escribe en el log
                raise ValueError("El pago no pudo procesarse.")

            inv.cantidad -= 1
            inv.save()

            Orden.objects.create(
                usuario=usuario,
                libro=libro,
                total=total,
                direccion_envio=direccion,
            )
        return total