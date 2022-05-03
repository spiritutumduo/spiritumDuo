from asyncpg import ForeignKeyViolationError
from SdTypes import Permissions
from models import Pathway, db, PathwayMilestoneType
from .mutation_type import mutation
from authentication.authentication import needsAuthorization
from graphql.type import GraphQLResolveInfo
from common import DataCreatorInputErrors


@mutation.field("deletePathway")
@needsAuthorization([Permissions.PATHWAY_DELETE])
async def resolve_delete_pathway(
    obj=None,
    info: GraphQLResolveInfo = None,
    id: int = None,
    userErrors: DataCreatorInputErrors = None,
) -> Pathway:
    userErrors = DataCreatorInputErrors()

    async with db.transaction() as tx:
        try:
            await PathwayMilestoneType.delete.where(
                PathwayMilestoneType.pathway_id == int(id)
            ).gino.status()
            pathway: Pathway = await Pathway.get(int(id))
            await pathway.delete()
            return True
        except ForeignKeyViolationError:
            userErrors.addError(
                "id", "You cannot remove a pathway with a relation")
            return userErrors