import graphene
from .types import UserType, _InputUserType
from api.models.SdUser import SdUser


# Interface between database and GraphQL
class _interface:
    def __init__(self, id:int=None, first_name:str=None,last_name:str=None,username:str=None,password:str=None,is_staff:str=None,is_superuser:str=None):
        self.id=id,
        self.first_name=first_name
        self.last_name=last_name
        self.username=username
        self.password=password
        self.is_staff=is_staff
        self.is_superuser=is_superuser


class CreateUser(graphene.Mutation): # Create class inheriting mutation class
    user=graphene.Field(UserType) # Define base return data of mutation
    class Arguments: # arguments the function can take
        userInput=graphene.Argument(_InputUserType)
    def mutate(self, info, userInput): # function to handle mutation
        newUser=SdUser(
            first_name=userInput.first_name,
            last_name=userInput.last_name,
            username=userInput.username,
            password=userInput.password,
            is_staff=userInput.is_staff,
            is_superuser=userInput.is_superuser
        )
        newUser.save()
        return CreateUser(user=_interface(
            id=newUser.id,
            first_name=newUser.first_name,
            last_name=newUser.last_name,
            username=newUser.username,
            password=newUser.password,
            is_staff=newUser.is_staff,
            is_superuser=newUser.is_superuser,
        ))