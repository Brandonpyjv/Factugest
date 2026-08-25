"""
Lector del esquema de la base de datos.

El diccionario de datos del documento se arma leyendo `base/factugest.sql`, no
transcribiendo las tablas a mano. Un diccionario copiado a mano empieza a
envejecer el día que se escribe, y la forma en que se descubre es siempre la misma,
cuando alguien busca en el sistema una columna que el documento describe y que ya
no existe.

Las descripciones salen del `COMMENT` que las columnas traen en el propio esquema.
Donde no hay comentario, el generador lo reporta para que se escriba.
"""
import re
from pathlib import Path

SQL = Path(__file__).resolve().parents[2] / "base" / "factugest.sql"

TIPOS = {
    "int": "Entero", "bigint": "Entero grande", "tinyint": "Entero pequeño",
    "varchar": "Texto", "text": "Texto largo", "longtext": "Texto largo",
    "decimal": "Decimal", "double": "Decimal", "float": "Decimal",
    "date": "Fecha", "datetime": "Fecha y hora", "timestamp": "Fecha y hora",
    "blob": "Binario", "longblob": "Binario", "mediumblob": "Binario",
    "mediumtext": "Texto largo", "tinytext": "Texto",
    "enum": "Enumerado", "char": "Texto",
}


def _legible(tipo_sql):
    """«varchar(150)» se lee mejor como «Texto (150)» en un documento."""
    base = re.match(r"([a-z]+)(\(([^)]*)\))?", tipo_sql)
    if not base:
        return tipo_sql
    nombre = TIPOS.get(base.group(1), base.group(1))
    return f"{nombre} ({base.group(3)})" if base.group(3) else nombre


def _cuerpo(tabla, sql):
    patron = rf"CREATE TABLE (?:IF NOT EXISTS )?`?{tabla}`?\s*\((.*?)\n\)\s*ENGINE"
    encontrado = re.search(patron, sql, re.S | re.I)
    if not encontrado:
        raise KeyError(f"No se encontró la tabla «{tabla}» en {SQL.name}")
    return encontrado.group(1)


def columnas(tabla, sql=None):
    """Devuelve (nombre, tipo legible, admite nulo, clave, descripción) por columna."""
    sql = sql if sql is not None else SQL.read_text(encoding="utf-8", errors="replace")
    cuerpo = _cuerpo(tabla, sql)

    primaria = re.search(r"PRIMARY KEY \(([^)]+)\)", cuerpo)
    primarias = set(re.findall(r"`([^`]+)`", primaria.group(1))) if primaria else set()
    foraneas = set(re.findall(r"FOREIGN KEY \(`([^`]+)`\)", cuerpo))
    unicas = set()
    for grupo in re.findall(r"UNIQUE KEY `[^`]+` \(([^)]+)\)", cuerpo):
        unicas.update(re.findall(r"`([^`]+)`", grupo))

    salida = []
    for linea in cuerpo.split("\n"):
        linea = linea.strip().rstrip(",")
        campo = re.match(r"`([^`]+)`\s+([a-z]+(?:\([^)]*\))?)(.*)", linea)
        if not campo:
            continue
        nombre, tipo, resto = campo.groups()
        comentario = re.search(r"COMMENT '([^']*)'", resto)
        claves = []
        if nombre in primarias:
            claves.append("PK")
        if nombre in foraneas:
            claves.append("FK")
        if nombre in unicas and nombre not in primarias:
            claves.append("Única")
        salida.append((
            nombre,
            _legible(tipo),
            "No" if "NOT NULL" in resto.upper() else "Sí",
            ", ".join(claves) or "No aplica",
            comentario.group(1) if comentario else "",
        ))
    return salida


def tablas(sql=None):
    sql = sql if sql is not None else SQL.read_text(encoding="utf-8", errors="replace")
    return re.findall(r"CREATE TABLE (?:IF NOT EXISTS )?`([^`]+)`", sql)


if __name__ == "__main__":
    texto = SQL.read_text(encoding="utf-8", errors="replace")
    todas = tablas(texto)
    print(f"{len(todas)} tablas en {SQL.name}")
    sin_comentario = 0
    for t in todas:
        cols = columnas(t, texto)
        faltan = [c[0] for c in cols if not c[4]]
        sin_comentario += len(faltan)
        print(f"  {t:26s} {len(cols):3d} columnas · sin descripción: {len(faltan)}")
    print(f"Total de columnas sin descripción: {sin_comentario}")
