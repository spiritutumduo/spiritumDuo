from ariadne.objects import ObjectType
from models import DecisionPoint
from common import DataCreatorInputErrors
from typing import Union
AddDecisionPointPayloadObjectType=ObjectType("AddDecisionPointPayload")

@AddDecisionPointPayloadObjectType.field("decisionPoint")
async def resolve(obj:Union[DecisionPoint, DataCreatorInputErrors]=None, *_):
    if type(obj) == DecisionPoint: return obj
    return None

@AddDecisionPointPayloadObjectType.field("userErrors")
async def resolve(obj:Union[DecisionPoint, DataCreatorInputErrors]=None, *_):
    if type(obj) == DataCreatorInputErrors: return obj.errorList
    return None