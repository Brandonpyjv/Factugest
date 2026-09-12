from fastapi.templating import Jinja2Templates

from services import monograma

templates = Jinja2Templates(directory="templates")

# El monograma de una empresa se dibuja igual en la pantalla y en el PDF, y de una
# sola definición: si la pantalla calculara sus propias iniciales, el día que
# cambien las reglas el panel y la factura mostrarían distintivos distintos.
templates.env.globals["iniciales"] = monograma.iniciales
templates.env.globals["color_monograma"] = monograma.color
