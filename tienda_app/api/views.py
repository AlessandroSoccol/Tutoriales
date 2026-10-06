from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import OrdenInputSerializer
from tienda_app.services import CompraRapidaService  # REUTILIZACION
from tienda_app.infra.factories import PaymentFactory


class CompraAPIView(APIView):
    """
    Endpoint para procesar compras vía JSON.

    POST /api/comprar/

    Payload:
    {
        "libro_id": 1,
        "direccion_envio": "Calle 123"
    }
    """

    def post(self, request):
        # 1. Validación de datos de entrada (Adapter)
        serializer = OrdenInputSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        datos = serializer.validated_data

        try:
            # 2. Inyección de Dependencias (Factory)
            gateway = PaymentFactory.get_processor()

            # 3. Ejecución de Lógica de Negocio (Service Layer)
            servicio = CompraRapidaService(procesador_pago=gateway)

            # Noten cómo el servicio NO cambia, solo cambia quien lo llama.
            resultado = servicio.ejecutar_compra(
                libro_id=datos['libro_id'],
                direccion=datos['direccion_envio'],
                usuario=request.user if request.user.is_authenticated else None # Asumiendo autenticación básica o sesión
            )

            return Response(
                {
                    "estado": "exito",
                    "mensaje": f"Orden creada. Total: {resultado}"
                },
                status=status.HTTP_201_CREATED
            )

        except ValueError as e:
            # Errores de negocio (ej: Sin stock)
            return Response(
                {"error": str(e)},
                status=status.HTTP_409_CONFLICT
            )

        except Exception as e:
            # Errores inesperados
            return Response(
                {"error": "Error interno"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )