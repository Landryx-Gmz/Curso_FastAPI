#After: Corre despued de las validaciones/transformaciones de pydantic
#Before: Corre antes de las validaciones/transformaciones de pydantic
#Plain: similar a before termina al retornar el valor
#Before: Flexible antes o despues de las validaciones de pydantic


from typing import Annotated
from pydantic import AfterValidator, BaseModel,field_validator

# ==============================ANNOTATED==================================

# Función para validar un campo
def es_par(value: int) -> int:
    if value % 2 == 1:
        raise ValueError(f"{value} no es numero par")
    return value

#validacion = Annotated[tipehim, AfterValidator(funcion)]

NumeroPar = Annotated[int, AfterValidator(es_par)]

class Model1(BaseModel):
    my_number: NumeroPar
#ejemplo: Model1 = Model1(my_number=3)

class Model2(BaseModel):
    other_number: Annotated[NumeroPar, AfterValidator(lambda v: v+2)]
# ejemplo2: Model2 = Model2(other_number=4)
# print(ejemplo2)

class Model3(BaseModel):
    lista_pares: list[NumeroPar]
# ejemplo3: Model3 = Model3(lista_pares=[2,5,10])
# print(ejemplo3)

# =======================DECORATOR==========================
class Item(BaseModel):
    item_id: int
    price: float
    @field_validator("item_id", "price")# despues de decir las variables que queremos validar podemos poner mediante mode="after,before,etc"
    def check_positive(cls, value:int | float):
        if value < 0 :
            raise ValueError("Item ID debe ser positivo")
banana: Item = Item(item_id=2, price=-2.7)