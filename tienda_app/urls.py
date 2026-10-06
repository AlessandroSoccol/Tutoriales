from django.urls import path
from tienda_app import views
from tienda_app.api.views import CompraAPIView   # <-- faltaba

urlpatterns = [
    path('', views.home, name='home'),
    path('compra/<int:libro_id>/', views.CompraView.as_view(), name='finalizar_compra'),
    path('api/v1/comprar/', CompraAPIView.as_view(), name='api_comprar'),
]