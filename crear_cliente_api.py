"""
Alta de un cliente de la API desde la consola.

    python crear_cliente_api.py --nombre "Siste Soluciones" --empresa 3
    python crear_cliente_api.py --listar
    python crear_cliente_api.py --rotar 1
    python crear_cliente_api.py --estado 1 SUSPENDIDO

Es provisional: cuando exista el módulo «Clientes API» del panel (tarea 5.2) esto
se hace desde la web. Mientras tanto, es lo que permite entregarle una llave al
punto de venta para que se integre.

La llave completa se muestra **una sola vez**, aquí. De ella solo queda el hash.
"""
import argparse
import sys

from database import get_one
from services.api_key_service import (ESTADOS, PLANES, cambiar_estado, crear_cliente_api,
                                      get_all_clientes_api, rotar_llave)


def listar():
    clientes = get_all_clientes_api()
    if not clientes:
        print("No hay clientes API registrados.")
        return
    print(f"{'ID':>3}  {'NOMBRE':28} {'PREFIJO':20} {'PLAN':10} {'ESTADO':11} EMISOR")
    for c in clientes:
        print(f"{c['cod_cliente_api']:>3}  {(c['nombre'] or '')[:28]:28} "
              f"{c['api_key_prefijo']:20} {c['plan']:10} {c['estado']:11} "
              f"{c['empresa_nombre'] or '-'}")


def crear(nombre, cod_empresa, cod_cliente, plan, limite):
    if not get_one("SELECT cod_empresa FROM empresas WHERE cod_empresa = %s", (cod_empresa,)):
        sys.exit(f"No existe la empresa {cod_empresa}. Revisa /branches.")
    if cod_cliente and not get_one("SELECT customer_id FROM customers WHERE customer_id = %s",
                                   (cod_cliente,)):
        sys.exit(f"No existe el cliente {cod_cliente}.")
    if plan not in PLANES:
        sys.exit(f"Plan inválido. Opciones: {', '.join(PLANES)}")

    cod, llave = crear_cliente_api(nombre, cod_empresa, cod_cliente, plan, limite)
    print(f"\nCliente API #{cod} creado: {nombre}")
    print("\n  Llave (se muestra una sola vez, guárdala ahora):\n")
    print(f"    {llave}\n")
    print("  Uso:")
    print(f"    curl -H \"X-API-Key: {llave}\" http://127.0.0.1:8000/api/v1/ping\n")


def main():
    p = argparse.ArgumentParser(description="Clientes de la API de FactuGest")
    p.add_argument("--listar", action="store_true", help="Lista los clientes registrados")
    p.add_argument("--nombre", help="Nombre del negocio o sistema integrado")
    p.add_argument("--empresa", type=int, help="cod_empresa con el que va a emitir")
    p.add_argument("--cliente", type=int, default=None,
                   help="customer_id al que le facturamos el plan (opcional)")
    p.add_argument("--plan", default="BASICO", help=f"Uno de: {', '.join(PLANES)}")
    p.add_argument("--limite", type=int, default=None,
                   help="Documentos por mes; omitir para sin límite")
    p.add_argument("--rotar", type=int, metavar="ID", help="Genera una llave nueva")
    p.add_argument("--estado", nargs=2, metavar=("ID", "ESTADO"),
                   help=f"Cambia el estado. Uno de: {', '.join(ESTADOS)}")
    args = p.parse_args()

    if args.listar:
        return listar()

    if args.rotar:
        print(f"\n  Llave nueva del cliente #{args.rotar} (la anterior ya no sirve):\n")
        print(f"    {rotar_llave(args.rotar)}\n")
        return

    if args.estado:
        cod, estado = args.estado
        if estado not in ESTADOS:
            sys.exit(f"Estado inválido. Opciones: {', '.join(ESTADOS)}")
        cambiar_estado(int(cod), estado)
        print(f"Cliente #{cod} ahora está {estado}.")
        return

    if not args.nombre or not args.empresa:
        p.error("Para crear un cliente hacen falta --nombre y --empresa "
                "(o usa --listar).")
    crear(args.nombre, args.empresa, args.cliente, args.plan, args.limite)


if __name__ == "__main__":
    main()
