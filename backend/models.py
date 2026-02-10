from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from .database import Base

class Especie(Base):
    __tablename__ = "especies"

    id = Column(Integer, primary_key=True, index=True)
    nome_popular = Column(String, index=True)
    nome_cientifico = Column(String)

class Lote(Base):
    __tablename__ = "lotes"

    id = Column(Integer, primary_key=True, index=True)
    especie_id = Column(Integer, ForeignKey("especies.id"))
    data_semeadura = Column(Date)
    quantidade_inicial = Column(Integer)
    quantidade_atual = Column(Integer)
    estagio = Column(String)
    local = Column(String)

class Qualidade(Base):
    __tablename__ = "qualidade"

    id = Column(Integer, primary_key=True, index=True)
    lote_id = Column(Integer, ForeignKey("lotes.id"))
    data_avaliacao = Column(Date)
    altura_media = Column(Float)
    diametro_coleto = Column(Float)
    sanidade = Column(String)
    uniformidade = Column(String)
    nota_qualidade = Column(Float)
    observacoes = Column(String)
