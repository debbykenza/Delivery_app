from datetime import datetime
from sqlalchemy.orm import Session
from uuid import UUID
from app.models.position import Position
from app.schemas.position import PositionCreate, PositionUpdate

class ServicePosition:
    @staticmethod
    def enregistrer_position(db: Session, position_data: PositionCreate) -> Position:
        position = Position(**position_data.dict())
        db.add(position)
        db.commit()
        db.refresh(position)
        return position

    @staticmethod
    def get_derniere_position_livreur(db: Session, livreur_id: UUID) -> Position:
        return db.query(Position).filter_by(livreur_id=livreur_id).order_by(Position.timestamp.desc()).first()

    @staticmethod
    def get_positions_par_livraison(db: Session, livraison_id: UUID) -> list[Position]:
        return db.query(Position).filter_by(livraison_id=livraison_id).order_by(Position.timestamp).all()

    @staticmethod
    def maj_derniere_position(db: Session, livreur_id: UUID, data: PositionUpdate) -> Position:
        position = db.query(Position).filter(Position.livreur_id == livreur_id).order_by(Position.timestamp.desc()).first()
        if position:
            position.latitude = data.latitude
            position.longitude = data.longitude
            position.timestamp = datetime.utcnow()
            db.commit()
            db.refresh(position)
            return position
        else:
            raise ValueError("Position non trouvée pour ce livreur")
        
    @staticmethod
    def supprimer_position(db: Session, position_id: UUID) -> bool:
        position = db.query(Position).filter(Position.id == position_id).first()
        if not position:
            return False
        db.delete(position)
        db.commit()
        return True
