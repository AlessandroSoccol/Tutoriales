import datetime
from ..domain.interfaces import ProcesadorPago

class BancoNacionalProcesador(ProcesadorPago):
    def pagar(self, monto: float) -> bool:
        # SUSTITUYA "SU_NOMBRE" por su nombre y apellido real
        archivo_log = "pagos_locales_ALESSANDRO_SOCCOL.log"

        with open(archivo_log, "a") as f:
            f.write(
                f"[{datetime.datetime.now()}] Transaccion exitosa por: ${monto}\n"
            )
        return True