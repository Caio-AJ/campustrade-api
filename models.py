from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
from datetime import datetime


class Produto(Base):
    """
    Model SQLAlchemy — representa a tabela 'produtos' no banco.
    Cada instância desta classe = uma linha na tabela.
    """
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)
    descricao = Column(String(500), nullable=False)
    preco = Column(Float, nullable=False)
    categoria = Column(String(50), nullable=False)
    vendedor = Column(String(50), nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)
