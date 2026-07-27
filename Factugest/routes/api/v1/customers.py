from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from services.customer_service import (
    get_all_customers,
    get_customer_by_id,
    create_customer,
    update_customer,
    delete_customer,
)
from routes.api.v1.auth import get_current_user

router = APIRouter(prefix="/api/v1/customers", tags=["customers (mobile)"])


class CustomerBase(BaseModel):
    full_name: str
    document_type: str
    document_number: str
    phone: str | None = ""
    email: str | None = ""
    address: str | None = ""
    cod_municipio: str | None = None
    pais: str = "Colombia"
    tipo_persona: str = "NATURAL"
    regimen_tributario: str = "NO_RESPONSABLE_IVA"


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    pass


class CustomerOut(BaseModel):
    customer_id: int
    full_name: str
    document_type: str | None = None
    document_number: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None
    ciudad: str | None = None
    departamento: str | None = None
    pais: str | None = None
    tipo_persona: str | None = None
    regimen_tributario: str | None = None
    cod_municipio: str | None = None
    activo: int | None = 1
    municipio_nombre: str | None = None
    departamento_nombre: str | None = None
    cod_departamento: str | None = None


def _get_active_or_404(customer_id: int) -> dict:
    c = get_customer_by_id(customer_id)
    if not c or not c.get("activo", 1):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado",
        )
    return c


@router.get("", response_model=list[CustomerOut])
def list_customers(user: dict = Depends(get_current_user)):
    return get_all_customers()


@router.get("/{customer_id}", response_model=CustomerOut)
def get_customer(customer_id: int, user: dict = Depends(get_current_user)):
    return _get_active_or_404(customer_id)


@router.post("", response_model=CustomerOut, status_code=status.HTTP_201_CREATED)
def create_customer_endpoint(
    payload: CustomerCreate,
    user: dict = Depends(get_current_user),
):
    customer_id = create_customer(
        full_name=payload.full_name,
        document_type=payload.document_type,
        document_number=payload.document_number,
        phone=payload.phone or "",
        email=payload.email or "",
        address=payload.address or "",
        cod_municipio=payload.cod_municipio,
        pais=payload.pais,
        tipo_persona=payload.tipo_persona,
        regimen_tributario=payload.regimen_tributario,
    )
    return get_customer_by_id(customer_id)


@router.put("/{customer_id}", response_model=CustomerOut)
def update_customer_endpoint(
    customer_id: int,
    payload: CustomerUpdate,
    user: dict = Depends(get_current_user),
):
    _get_active_or_404(customer_id)
    update_customer(
        customer_id,
        full_name=payload.full_name,
        document_type=payload.document_type,
        document_number=payload.document_number,
        phone=payload.phone or "",
        email=payload.email or "",
        address=payload.address or "",
        cod_municipio=payload.cod_municipio,
        pais=payload.pais,
        tipo_persona=payload.tipo_persona,
        regimen_tributario=payload.regimen_tributario,
    )
    return get_customer_by_id(customer_id)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer_endpoint(
    customer_id: int,
    user: dict = Depends(get_current_user),
):
    _get_active_or_404(customer_id)
    delete_customer(customer_id)
    return None
