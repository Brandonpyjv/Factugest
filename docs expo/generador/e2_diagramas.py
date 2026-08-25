"""
E2 — Diagramas de casos de uso de FactuGest.

Los diagramas se dibujan a partir de `casos_de_uso.py`, que es la misma lista de la
que sale la documentación de E3. Las relaciones de inclusión y extensión se declaran
por código de caso y aquí se traducen a nombres, que es lo que el dibujante rotula.

    python e2_diagramas.py
"""
from pathlib import Path

import casos_de_uso as catalogo
from apa import DocumentoAPA, inicial_minuscula
from uml import Diagrama

BASE = Path(__file__).resolve().parent.parent
SALIDA = BASE / "entregables"
IMAGENES = SALIDA / "diagramas"
ARCHIVO = SALIDA / "FactuGest - Diagramas de Casos de Uso.docx"

ACTORES = [
    ("Administrador", "Persona con acceso completo a la plataforma. Administra los clientes "
     "integrados, los planes, las empresas emisoras, los usuarios y la configuración, y "
     "consulta la totalidad de los reportes."),
    ("Jefe de tienda", "Persona responsable de la operación de su propia empresa. Accede al "
     "tablero y a los reportes de esa empresa, sin consolidar las demás."),
    ("Supervisor", "Persona que consulta la operación y los reportes de su empresa, con "
     "capacidad limitada de modificación."),
    ("Cajero", "Persona que factura. Emite documentos y consulta clientes y servicios; no "
     "accede a cifras financieras ni a los módulos de plataforma."),
    ("Sistema cliente", "Sistema externo, sea punto de venta, ERP o aplicación propia de la "
     "empresa integrada, que consume la API con su llave para emitir y consultar documentos. "
     "Es un actor no humano y es el que origina la mayor parte de la operación."),
    ("Comprador", "Destinatario del documento electrónico. No accede al sistema y recibe el "
     "PDF y el XML en su correo. Se representa como actor porque es quien recibe el "
     "resultado del caso de uso, aunque nunca lo inicie."),
]


def _dibujar_general():
    diagrama = Diagrama(
        sistema="FACTUGEST",
        actores_izq=["Administrador", "Cajero", "Jefe de tienda"],
        actores_der=["Sistema cliente", "Supervisor", "Comprador"],
        casos=catalogo.GENERAL,
    )
    return diagrama.dibujar(IMAGENES / "DCU-00 general.png")


def _dibujar_modulo(modulo):
    codigo, nombre, izq, der, casos, inclusiones, extensiones, _ = modulo
    nombres = {c[0]: c[1] for c in casos}
    diagrama = Diagrama(
        sistema="FACTUGEST",
        modulo=nombre,
        actores_izq=izq,
        actores_der=der,
        casos=catalogo.por_nombre(casos),
        inclusiones=[(nombres[a], nombres[b]) for a, b in inclusiones],
        extensiones=[(nombres[a], nombres[b]) for a, b in extensiones],
    )
    return diagrama.dibujar(IMAGENES / f"{codigo} {nombre}.png")


def construir():
    IMAGENES.mkdir(parents=True, exist_ok=True)
    general = _dibujar_general()
    dibujos = {m[0]: _dibujar_modulo(m) for m in catalogo.MODULOS}

    d = DocumentoAPA()
    d.portada(
        titulo="FACTUGEST",
        subtitulo="Diagramas de casos de uso",
        integrantes=["Brandon Arley Restrepo Gélvez",
                     "Johan Sebastián Acosta Sánchez",
                     "Wilmer Jesús Contreras Rangel"],
        grado="Ficha 3115426\nTecnólogo en Análisis y Desarrollo de Software",
        institucion=["SERVICIO NACIONAL DE APRENDIZAJE (SENA)",
                     "Centro de la Industria, la Empresa y los Servicios (CIES)",
                     "Tecnólogo en Análisis y Desarrollo de Software"],
        ciudad="CÚCUTA, NORTE DE SANTANDER",
        anio=2026,
    )
    d.tabla_contenido()

    _introduccion(d)
    _actores(d)
    _general(d, general)
    _modulos(d, dibujos)
    _matriz(d)

    SALIDA.mkdir(parents=True, exist_ok=True)
    d.guardar(ARCHIVO)
    return d


def _introduccion(d):
    d.titulo("1. Introducción", nivel=1)
    d.parrafo(
        "Este documento reúne los diagramas de casos de uso de FactuGest. Un caso de uso "
        "describe un objetivo que un actor persigue con el sistema y el resultado observable "
        "que obtiene; no describe una pantalla ni una operación sobre la base de datos. Por "
        "esa razón los cincuenta y seis casos que aquí se presentan no coinciden en número "
        "con los ochenta y dos requisitos funcionales especificados, porque un caso como «gestionar "
        "impuestos» cubre el registro, la consulta, la actualización y la eliminación, que "
        "para quien usa el sistema son un mismo propósito."
    )
    d.parrafo(
        "Los diagramas se elaboraron contra el sistema construido, no contra el planteamiento "
        "inicial del proyecto. Entre uno y otro el alcance cambió: FactuGest dejó de ser un "
        "facturador para una sola empresa y pasó a ser un proveedor que emite por cuenta de "
        "terceros mediante una API. Ese cambio introdujo actores que antes no existían, como el "
        "sistema cliente, y módulos completos como el de clientes integrados "
        "y el de consumo y planes."
    )

    d.titulo("1.1 Notación empleada", nivel=2)
    d.tabla(
        "Elementos de la notación UML utilizados",
        ["Elemento", "Representación", "Significado"],
        [
            ["Actor", "Figura de palotes, fuera de la frontera",
             "Quien interactúa con el sistema. Puede ser una persona o un sistema externo."],
            ["Caso de uso", "Elipse, dentro de la frontera",
             "Objetivo que el actor persigue y resultado que obtiene."],
            ["Frontera del sistema", "Rectángulo rotulado",
             "Separa lo que el sistema hace de quienes lo usan."],
            ["Asociación", "Línea continua",
             "Participación de un actor en un caso de uso."],
            ["«include»", "Flecha discontinua",
             "El caso base siempre ejecuta al caso incluido; sin él queda incompleto."],
            ["«extend»", "Flecha discontinua",
             "El caso extensión agrega comportamiento en ciertas condiciones; el caso base se "
             "sostiene sin él."],
        ],
        nota="Elaboración propia con base en la notación UML.",
        anchos=[3.0, 4.6, 8.7],
    )
    d.parrafo(
        "La distinción entre inclusión y extensión no es un detalle de notación. Calcular los "
        "totales de un documento está incluido en emitirlo, porque una factura sin totales no "
        "es una factura; enviar el documento al comprador lo extiende, porque el documento ya "
        "quedó emitido y válido aunque el correo no salga. Modelar la segunda como inclusión "
        "supondría que un servidor de correo caído impide facturar."
    )


def _actores(d):
    d.titulo("2. Actores del sistema", nivel=1, nueva_pagina=True)
    d.parrafo(
        "El sistema reconoce seis actores. Cuatro corresponden a los roles del panel y se "
        "ordenan jerárquicamente; los otros dos no son personas que lo operen, ya que uno es el "
        "sistema externo que consume la API y el otro es quien recibe el documento emitido."
    )
    d.tabla(
        "Actores del sistema y su alcance",
        ["Actor", "Descripción"],
        [[a, desc] for a, desc in ACTORES],
        nota="Elaboración propia.",
        anchos=[3.4, 12.9],
    )


def _general(d, imagen):
    d.titulo("3. Diagrama general de casos de uso", nivel=1, nueva_pagina=True)
    d.parrafo(
        "El diagrama general presenta el sistema completo agrupando los casos por el "
        "propósito que atienden. Cada uno de esos grupos se detalla después en su propio "
        "diagrama. Se presenta de esta forma porque un diagrama con los cincuenta y seis "
        "casos y sus asociaciones resultaría ilegible, y un diagrama que no se lee no cumple "
        "la función de comunicar el alcance del sistema."
    )
    d.figura(
        "Diagrama general de casos de uso de FactuGest",
        imagen,
        nota="Elaboración propia. Cada elipse agrupa los casos de uso de un módulo, "
             "detallados en el capítulo 4.",
    )
    d.parrafo(
        "Dos observaciones sobre lo que el diagrama muestra. La primera es que el sistema "
        "cliente participa en la emisión de documentos igual que un cajero, porque para la "
        "plataforma, una venta registrada por una persona y una enviada por el punto de venta "
        "de un tercero recorren el mismo camino. La segunda es que el comprador aparece "
        "recibiendo un documento sin iniciar ningún caso, lo que corresponde a su situación "
        "real, ya que es el destinatario de la operación y no tiene acceso al sistema."
    )


def _modulos(d, dibujos):
    d.titulo("4. Diagramas por módulo", nivel=1, nueva_pagina=True)
    d.parrafo(
        "Los ocho diagramas siguientes corresponden a los ocho módulos funcionales "
        "especificados en el documento de requisitos. La correspondencia es intencional, porque "
        "cada caso de uso indica los requisitos que cubre, de modo que pueda comprobarse que "
        "ningún requisito quedó sin caso y que ningún caso describe algo que no fue "
        "especificado."
    )

    for indice, modulo in enumerate(catalogo.MODULOS, start=1):
        codigo, nombre, _, _, casos, _, _, explicacion = modulo
        d.titulo(f"4.{indice} {codigo}. {nombre}", nivel=2, nueva_pagina=True)
        d.parrafo(explicacion)
        d.figura(
            f"Diagrama de casos de uso del módulo de {inicial_minuscula(nombre)}",
            dibujos[codigo],
            nota=f"Elaboración propia. Corresponde al módulo {codigo.replace('DCU-0', 'RF ')} "
                 "del documento de requisitos.",
        )
        d.tabla(
            f"Casos de uso del módulo {codigo}",
            ["Código", "Caso de uso", "Actores", "Descripción", "Requisitos"],
            [[c, n, ", ".join(a) if a else "Ninguno", desc, rf] for c, n, a, desc, rf in casos],
            nota="Elaboración propia. Los casos sin actor son casos incluidos y el sistema los "
                 "ejecuta como parte de otro y nadie los inicia por separado.",
            anchos=[1.6, 3.2, 3.0, 5.5, 3.0],
        )


def _matriz(d):
    d.titulo("5. Matriz de casos de uso por actor", nivel=1, nueva_pagina=True)
    d.parrafo(
        "La matriz resume en qué casos participa cada actor. Sirve para comprobar dos cosas, "
        "que ningún actor quedó sin casos, lo que indicaría un rol declarado pero no "
        "utilizado, y que ningún caso quedó sin actor salvo los incluidos, que por definición "
        "los ejecuta el sistema."
    )

    actores = [a for a, _ in ACTORES]
    filas = []
    for codigo, nombre, modulo, suyos, _, _ in catalogo.todos():
        filas.append([codigo, nombre] + ["X" if a in suyos else "" for a in actores])

    d.tabla(
        "Matriz de participación de los actores en los casos de uso",
        ["Código", "Caso de uso", "Admin.", "Jefe", "Superv.", "Cajero", "Sist. cliente",
         "Compr."],
        filas,
        nota="Elaboración propia. «Admin.» corresponde al administrador, «Jefe» al jefe de "
             "tienda, «Superv.» al supervisor, «Sist. cliente» al sistema integrado y "
             "«Compr.» al comprador.",
        anchos=[1.5, 4.6, 1.5, 1.2, 1.5, 1.4, 1.9, 1.4],
    )

    sin_actor = [c for c, _, _, actores_caso, _, _ in catalogo.todos() if not actores_caso]
    d.parrafo(
        f"De los {len(catalogo.todos())} casos de uso, {len(sin_actor)} no tienen actor "
        f"asociado: {', '.join(sin_actor)}. Todos ellos son casos incluidos, que el sistema "
        "ejecuta como parte de otro caso. El resto tiene al menos un actor, y los seis "
        "actores declarados participan en al menos un caso."
    )


if __name__ == "__main__":
    documento = construir()
    print(f"Generado: {ARCHIVO}")
    print(f"Casos de uso: {len(catalogo.todos())} · Diagramas: {len(catalogo.MODULOS) + 1}")
    print(f"Tablas: {documento.n_tabla} · Figuras: {documento.n_figura}")
