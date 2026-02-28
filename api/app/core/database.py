from app.core.bootstrap.db import Base, engine, SessionLocal
from app.modules.contas import Conta

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def inserir_conta(dados):    
    db = SessionLocal()

    try:
        nova_conta = Conta(
            residencia=dados.get("residencia"),
            tipo=dados.get("tipo"),
            favorecido=dados.get("favorecido"),
            referencia=dados.get("referencia"),
            valor=float(dados.get("valor", "0").replace(",", ".")) if dados.get("valor") else None,
            vencimento=dados.get("vencimento"),
            codigo_barras=dados.get("codigo_pagamento"),
            pix_payload=dados.get("pix_payload"),
            descricao=dados.get("descricao"),
        )

        db.add(nova_conta)
        db.commit()
        db.refresh(nova_conta)

        return nova_conta

    finally:
        db.close()

def listar_contas():
    db = SessionLocal()

    try:
        contas = db.query(Conta).order_by(Conta.vencimento).all()

        return [
            {
                "id": c.id,
                "residencia": c.residencia,
                "tipo": c.tipo,
                "favorecido": c.favorecido,
                "referencia": c.referencia,
                "valor": c.valor,
                "vencimento": c.vencimento,
                "codigo_barras": c.codigo_barras,
                "pix_payload": c.pix_payload,
                "descricao": c.descricao,
                "status": c.status,
                "criado_em": c.criado_em,
            }
            for c in contas
        ]

    finally:
        db.close()

def pagar_conta(conta_id: int):
    db = SessionLocal()

    try:
        conta = db.query(Conta).filter(Conta.id == conta_id).first()

        if conta:
            conta.status = "pago"
            db.commit()

        return conta

    finally:
        db.close()