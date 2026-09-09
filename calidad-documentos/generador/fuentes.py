"""
Las fuentes del informe, en un solo sitio.

Mismo reparto que el documento de grado. Los capítulos citan por clave y el cierre
construye la lista bibliográfica a partir de esta misma estructura, porque escribir
la lista aparte termina siempre igual, o con una fuente citada que no aparece en la
lista o con una lista que incluye fuentes que nadie citó.

Todas se citan por parafraseo salvo las tres que el texto entrecomilla, que llevan
su página. Las normas ISO se citan por el organismo y el año de la versión.
"""

# clave: (cita en el texto, referencia completa en APA 7)
FUENTES = {
    "sena": ("SENA, s.f.",
             "Servicio Nacional de Aprendizaje. (s.f.). Modelos y estándares de calidad "
             "del software [Material de formación]. Formación en Ambientes Virtuales de "
             "Aprendizaje, SENA."),
    "pressman": ("Pressman, 2010",
                 "Pressman, R. S. (2010). Ingeniería del software: un enfoque práctico "
                 "(7.ª ed.). McGraw-Hill."),
    "vega": ("Vega et al., 2008",
             "Vega, V., Rivera, L., y García, R. (2008). Mejores prácticas para el "
             "establecimiento y aseguramiento de la calidad de software. Universidad "
             "Cristóbal Colón."),
    "scalone": ("Scalone, 2006",
                "Scalone, F. (2006). Estudio comparativo de los modelos y estándares de "
                "calidad del software [Tesis de maestría, Universidad Tecnológica "
                "Nacional]."),
    "estayno": ("Estayno et al., 2009",
                "Estayno, M., Dapozo, G., Cuenca Pletsch, L., y Greiner, C. (2009). "
                "Modelos y métricas para evaluar la calidad del software. XI Workshop de "
                "Investigadores en Ciencias de la Computación, 382-386."),
    "fillottrani": ("Fillottrani, 2007",
                    "Fillottrani, P. (2007). Calidad en el desarrollo de software: "
                    "modelos de calidad de software. Universidad Nacional del Sur."),
    "gomez": ("Gómez, 2009",
              "Gómez, D. (2009). ¿Qué significa calidad de software? Dos Ideas."),
    "rae": ("Real Academia Española, 2023",
            "Real Academia Española. (2023). Diccionario de la lengua española "
            "(23.ª ed.)."),
    "ieee": ("IEEE, 1990",
             "Institute of Electrical and Electronics Engineers. (1990). IEEE Standard "
             "Glossary of Software Engineering Terminology (IEEE Std 610.12-1990). IEEE."),
    "iso9126": ("ISO/IEC, 2001",
                "International Organization for Standardization. (2001). ISO/IEC "
                "9126-1:2001. Software engineering. Product quality. Part 1, Quality "
                "model. ISO."),
    "iso25000": ("ISO/IEC, 2005",
                 "International Organization for Standardization. (2005). ISO/IEC "
                 "25000:2005. Software engineering. Software product Quality Requirements "
                 "and Evaluation (SQuaRE). Guide to SQuaRE. ISO."),
    "iso25010": ("ISO/IEC, 2011",
                 "International Organization for Standardization. (2011). ISO/IEC "
                 "25010:2011. Systems and software engineering. Systems and software "
                 "Quality Requirements and Evaluation (SQuaRE). System and software "
                 "quality models. ISO."),
    "iso15504": ("ISO/IEC, 2004",
                 "International Organization for Standardization. (2004). ISO/IEC "
                 "15504-1:2004. Information technology. Process assessment. Part 1, "
                 "Concepts and vocabulary. ISO."),
    "iso12207": ("ISO/IEC, 2008",
                 "International Organization for Standardization. (2008). ISO/IEC "
                 "12207:2008. Systems and software engineering. Software life cycle "
                 "processes. ISO."),
    "iso9001": ("ISO, 2015",
                "International Organization for Standardization. (2015). ISO 9001:2015. "
                "Quality management systems. Requirements. ISO."),
    "cmmi": ("CMMI Product Team, 2010",
             "CMMI Product Team. (2010). CMMI for Development, Version 1.3 "
             "(CMU/SEI-2010-TR-033). Software Engineering Institute, Carnegie Mellon "
             "University."),
    "portal25000": ("ISO 25000, 2018",
                    "Portal ISO 25000. (2018). La familia de normas ISO/IEC 25000."),
    "polillo": ("Polillo, 2011",
                "Polillo, R. (2011). Quality models for web [2.0] sites: a methodological "
                "approach and a proposal. Lecture Notes in Computer Science, 6757, "
                "251-265."),
    "alfonzo": ("Alfonzo y Mariño, 2013",
                "Alfonzo, P., y Mariño, S. (2013). Propuesta metodológica para la "
                "evaluación de la calidad de productos de software. Universidad Nacional "
                "del Nordeste."),
    "dian42": ("DIAN, 2020",
               "Dirección de Impuestos y Aduanas Nacionales. (2020). Resolución 000042 de "
               "2020, por la cual se desarrollan los sistemas de facturación, los "
               "proveedores tecnológicos y se expide el anexo técnico de factura "
               "electrónica de venta. DIAN."),
    "istqb": ("ISTQB, 2018",
              "International Software Testing Qualifications Board. (2018). Certified "
              "Tester Foundation Level Syllabus, Version 2018. ISTQB."),
    "ieee829": ("IEEE, 2008",
                "Institute of Electrical and Electronics Engineers. (2008). IEEE Standard "
                "for Software and System Test Documentation (IEEE Std 829-2008). IEEE."),
    "iso29119": ("ISO/IEC/IEEE, 2013",
                 "International Organization for Standardization. (2013). "
                 "ISO/IEC/IEEE 29119-1:2013. Software and systems engineering. Software "
                 "testing. Part 1, Concepts and definitions. ISO."),
    "beck": ("Beck, 2003",
             "Beck, K. (2003). Test-driven development: by example. Addison-Wesley."),
    "myers": ("Myers et al., 2011",
              "Myers, G. J., Sandler, C., y Badgett, T. (2011). The art of software "
              "testing (3.ª ed.). John Wiley and Sons."),
}


def cita(clave):
    """La forma corta, para meter entre paréntesis en el cuerpo."""
    return FUENTES[clave][0]


def narrativa(clave):
    """La forma para cuando el autor es sujeto de la oración, con el año aparte.

    APA distingue las dos formas. Entre paréntesis va «(Scalone, 2006)», pero cuando
    el autor entra en la frase se escribe «Scalone (2006) sostiene», y usar la
    primera dentro del texto produce el error corriente de escribir «según Scalone,
    2006 la calidad».
    """
    autor, anio = FUENTES[clave][0].rsplit(", ", 1)
    return f"{autor} ({anio})"


def usadas(claves):
    """Las referencias completas de las claves citadas, en orden alfabético.

    Se ordena por la referencia y no por la clave porque APA ordena la lista por el
    apellido del autor, que es con lo que empieza la referencia.
    """
    return sorted({FUENTES[c][1] for c in claves})
