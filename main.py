from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import Produto
from schemas import ProdutoCreate, ProdutoUpdate, ProdutoResponse
from datetime import datetime
from typing import List


# --- Criar tabelas (fallback se não usar migrations) ---
Base.metadata.create_all(bind=engine)

# --- Configuração do App ---
app = FastAPI(
    title="CampusTrade API",
    description="Marketplace universitário — Projeto de Cloud IBMEC",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Endpoints ---

@app.get("/health")
def health_check():
    """Health check — Azure usa para verificar se a app está viva."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/")
def root():
    """Página inicial."""
    return {
        "aplicacao": "CampusTrade API",
        "versao": "2.0.0",
        "documentacao": "/docs"
    }


@app.get("/produtos", response_model=List[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    """
    Lista todos os produtos.
    O Depends(get_db) injeta uma sessão de banco automaticamente.
    """
    return db.query(Produto).all()


@app.post("/produtos", response_model=ProdutoResponse, status_code=201)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    """
    Cria um novo produto no banco.
    1. Pydantic valida os dados (ProdutoCreate)
    2. Criamos o objeto SQLAlchemy (Produto)
    3. Salvamos no banco (add + commit)
    4. Refresh carrega o id e criado_em gerados pelo banco
    """
    novo_produto = Produto(
        titulo=produto.titulo,
        descricao=produto.descricao,
        preco=produto.preco,
        categoria=produto.categoria,
        vendedor=produto.vendedor
    )
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto


@app.get("/produtos/{produto_id}", response_model=ProdutoResponse)
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    """Busca produto por ID."""
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto


@app.put("/produtos/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(
    produto_id: int,
    dados: ProdutoUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza um produto existente.
    Só altera os campos que foram enviados (não-nulos).
    """
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    # Atualiza apenas campos enviados
    dados_dict = dados.model_dump(exclude_unset=True)
    for campo, valor in dados_dict.items():
        setattr(produto, campo, valor)

    db.commit()
    db.refresh(produto)
    return produto


@app.delete("/produtos/{produto_id}")
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    """Remove um produto do banco."""
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    db.delete(produto)
    db.commit()
    return {"message": "Produto removido com sucesso", "id": produto_id}


# --- Ponto de entrada ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
