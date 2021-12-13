from . import db
from sqlalchemy import func, false, Enum
from SdTypes import DecisionTypes

class OnPathway(db.Model):
    __tablename__ = "on_pathway"

    id = db.Column(db.Integer(), primary_key=True)
    patient = db.Column(db.Integer(), db.ForeignKey('patient.id'), nullable=False)
    pathway = db.Column(db.Integer(), db.ForeignKey('pathway.id'), nullable=False)
    is_discharged = db.Column(db.Boolean(), server_default=false(), default=False, nullable=False)
    awaiting_decision_type = db.Column(
     Enum(DecisionTypes, native_enum=False), default=DecisionTypes.TRIAGE.value,
     server_default=DecisionTypes.TRIAGE.value, nullable=False
    )
    added_at = db.Column(db.DateTime(), server_default=func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )
