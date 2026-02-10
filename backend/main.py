from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from datetime import date

from .database import SessionLocal, engine
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Viveiro de Mudas")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/especies/")
def criar_especie(nome_popular: str, nome_cientifico: str, db: Session = Depends(get_db)):
    especie = models.Especie(
        nome_popular=nome_popular,
        nome_cientifico=nome_cientifico
    )
    db.add(especie)
    db.commit()
    db.refresh(especie)
    return especie

@app.get("/especies/")
def listar_especies(db: Session = Depends(get_db)):
    return db.query(models.Especie).all()

@app.post("/lotes/")
def criar_lote(
    especie_id: int,
    quantidade: int,
    estagio: str,
    local: str,
    db: Session = Depends(get_db)
):
    lote = models.Lote(
        especie_id=especie_id,
        data_semeadura=date.today(),
        quantidade_inicial=quantidade,
        quantidade_atual=quantidade,
        estagio=estagio,
        local=local
    )
    db.add(lote)
    db.commit()
    db.refresh(lote)
    return lote

@app.post("/qualidade/")
def registrar_qualidade(
    lote_id: int,
    altura_media: float,
    diametro_coleto: float,
    sanidade: str,
    uniformidade: str,
    nota_qualidade: float,
    observacoes: str,
    db: Session = Depends(get_db)
):
    qualidade = models.Qualidade(
        lote_id=lote_id,
        data_avaliacao=date.today(),
        altura_media=altura_media,
        diametro_coleto=diametro_coleto,
        sanidade=sanidade,
        uniformidade=uniformidade,
        nota_qualidade=nota_qualidade,
        observacoes=observacoes
    )
    db.add(qualidade)
    db.commit()
    db.refresh(qualidade)
    return qualidade
