#After: Corre despued de las validaciones/transformaciones de pydantic
#Before: Corre antes de las validaciones/transformaciones de pydantic
#Plain: similar a before termina al retornar el valor
#Before: Flexible antes o despues de las validaciones de pydantic


from typing import Annotated
from pydantic import AfterValidator, BaseModel

# Función para validar un campo
def es_par(value: int) -> int:
    if value %2 == 1:
        raise ValueError(f"{value} no es numero par")
    return value

#validacion = Annotated[tipehim, AfterValidator(funcion)]

NumeroPar = Annotated[int, AfterValidator(es_par)]

class Model1(BaseModel):
    my_number: NumeroPar



# class Model2(BaseModel):
#     my_number:
# class Model3(BaseModel):

