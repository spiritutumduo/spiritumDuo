from typing import List, Dict, Optional
from aiodataloader import DataLoader
from models import MilestoneType
import logging

class MilestoneTypeLoader(DataLoader):
    loader_name = "_milestone_type_loader"
    _db = None

    def __init__(self, db):
        super().__init__()
        self._db = db

    @classmethod
    def _get_loader_from_context(cls, context) -> "MilestoneTypeLoader":
        if cls.loader_name not in context:
            context[cls.loader_name] = cls(db=context['db'])
        return context[cls.loader_name]

    async def fetch(self, keys) -> Dict[int, MilestoneType]:
        async with self._db.acquire(reuse=False) as conn:
            query = MilestoneType.query.where(MilestoneType.id.in_(keys))
            result = await conn.all(query)
            logging.info(result)

            returnData = {}
            for milestone in result:
                returnData[milestone.id] = milestone

            return returnData

    async def batch_load_fn(self, keys) -> List[MilestoneType]:
        fetchDict = await self.fetch([int(i) for i in keys])
        sortedData = []
        for key in keys:
            sortedData.append(fetchDict.get(int(key)))
        return sortedData

    @classmethod
    async def load_from_id(cls, context=None, id=None) -> Optional[MilestoneType]:
        if not id:
            return None
        return await cls._get_loader_from_context(context).load(id)

    @classmethod
    async def load_many_from_id(cls, context=None, ids=None) -> Optional[List[MilestoneType]]:
        if not ids:
            return None
        return await cls._get_loader_from_context(context).load_many(ids)
