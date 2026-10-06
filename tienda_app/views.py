from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponse

from .infra.factories import PaymentFactory
from .services import CompraRapidaService
from .models import Libro


def home(request):
    return HttpResponse("Bienvenido a la tienda")


class CompraView(View):
    template_name = 'tienda_app/compra.html'

    def setup_service(self):
        gateway = PaymentFactory.get_processor()
        return CompraRapidaService(procesador_pago=gateway)

    def get(self, request, libro_id):
        servicio = self.setup_service()
        contexto = servicio.obtener_detalle_producto(libro_id)
        return render(request, self.template_name, contexto)

    def post(self, request, libro_id):
        servicio = self.setup_service()
        try:
            total = servicio.procesar(libro_id)
            return render(
                request,
                self.template_name,
                {'mensaje_exito': f"¡Gracias por su compra! Total: ${total}", 'total': total},
            )
        except ValueError as e:
            return render(request, self.template_name, {'error': str(e)}, status=400)