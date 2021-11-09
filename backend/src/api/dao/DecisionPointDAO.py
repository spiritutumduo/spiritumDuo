from datetime import datetime
from typing import Iterable

from api.models import decisionpoint_orm, patient_orm

# Interface between database and GraphQL
class _interface:
    def __init__(self, id:int, patient:patient_orm, clinician:int, type:str, added_at:datetime, updated_at:datetime, clinic_history:str, comorbidities:str):
        self.id=id
        self.patient=patient
        self.clinician=clinician
        self.type=type
        self.added_at=added_at
        self.updated_at=updated_at
        self.clinic_history=clinic_history
        self.comorbidities=comorbidities

# DAO object
class DecisionPointDAO:
    def __init__(self, id:int=None, patient:int=None, clinician:int=None, type:str=None, added_at:datetime=None, updated_at:datetime=None, clinic_history:str=None, comorbidities:str=None):
        self.id=id
        self.patient=patient
        self.clinician=clinician
        self.type=type
        self.added_at=added_at
        self.updated_at=updated_at
        self.clinic_history=clinic_history
        self.comorbidities=comorbidities
        self._orm: decisionpoint_orm = decisionpoint_orm()

        if id:
            self._orm.id=id
            self._orm.patient=patient
            self._orm.clinician=clinician
            self._orm.type=type
            self._orm.added_at=added_at
            self._orm.updated_at=updated_at
            self._orm.clinic_history=clinic_history
            self._orm.comorbidities=comorbidities

    @classmethod
    def read(cls, id:int=None):
        try:
            if not id:
                returnData=decisionpoint_orm.objects.all()
            else:
                returnData=decisionpoint_orm.objects.get(id=id)
            returnList=[]
            
            if isinstance(returnData, Iterable):
                for row in returnData:
                    returnList.append(
                        cls(
                            id=row.id,
                            patient=row.patient,
                            clinician=row.clinician,
                            type=row.type,
                            added_at=row.added_at,
                            updated_at=row.updated_at,
                            clinic_history=row.clinic_history,
                            comorbidities=row.comorbidities,
                        )
                    )
                return returnList
            else:
                return cls(
                    id=returnData.id,
                    patient=returnData.patient,
                    clinician=returnData.clinician,
                    type=returnData.type,
                    added_at=returnData.added_at,
                    updated_at=returnData.updated_at,
                    clinic_history=returnData.clinic_history,
                    comorbidities=returnData.comorbidities,
                )
        except (decisionpoint_orm.DoesNotExist):
            return False

    def delete(self):
        self._orm.delete()
        
    def save(self):
        self._orm.patient=self.patient
        self._orm.clinician=self.clinician
        self._orm.type=self.type
        self._orm.added_at=self.added_at
        self._orm.updated_at=self.updated_at
        self._orm.clinic_history=self.clinic_history
        self._orm.comorbidities=self.comorbidities
        self._orm.save()
        self.id=self._orm.id