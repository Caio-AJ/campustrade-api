from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ProdutoCreate(BaseModel):
    """Schema para CRIAR produto (POST)."""
    titulo: str = Field(..., min_length=3, max_length=100)
    descricao: str = Field(..., min_length=10, max_length=500)
    preco: float = Field(..., gt=0, le=50000)
    categoria_id: Optional[int] = Field(None)
    vendedor: str = Field(..., min_length=2, max_length=50)

class CategoriaCreate(BaseModel):
    """Schema para CRIAR categoria (POST)."""
    nome: str = Field(..., min_length=3, max_length=50)
    descricao: Optional[str] = Field(None, max_length=200)


class ProdutoUpdate(BaseModel):
    """
    Schema para ATUALIZAR produto (PUT).
    Todos os campos são opcionais — só atualiza o que for enviado.
    """
    titulo: Optional[str] = Field(None, min_length=3, max_length=100)
    descricao: Optional[str] = Field(None, min_length=10, max_length=500)
    preco: Optional[float] = Field(None, gt=0, le=50000)
    categoria_id: Optional[int] = Field(None)
    vendedor: Optional[str] = Field(None, min_length=2, max_length=50)

class CategoriaResponse(BaseModel):
    id: int
    nome: str
    descricao: Optional[str] = None

    class Config:
        from_attributes = True

class ProdutoResponse(BaseModel):
    """Schema de RESPOSTA — o que a API retorna."""
    id: int
    titulo: str
    descricao: str
    preco: float
    categoria_id: Optional[int]
    categoria_rel: Optional[CategoriaResponse] = None
    vendedor: str
    criado_em: datetime


    class Config:
        from_attributes = True  # Permite converter objetos SQLAlchemy → Pydantic
