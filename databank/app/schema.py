import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from .models import Peptoid as PeptoidModel, Residue as ResidueModel, Author as AuthorModel

class Peptoid(SQLAlchemyObjectType):
    class Meta:
        model = PeptoidModel
        interfaces = (relay.Node, )

class Residue(SQLAlchemyObjectType):
    class Meta:
        model = ResidueModel
        interfaces = (relay.Node, )

class Author(SQLAlchemyObjectType):
    class Meta:
        model = AuthorModel
        interfaces = (relay.Node, )

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    peptoids = SQLAlchemyConnectionField(Peptoid.connection)
    residues = SQLAlchemyConnectionField(Residue.connection)
    authors = SQLAlchemyConnectionField(Author.connection)

schema = graphene.Schema(query=Query)