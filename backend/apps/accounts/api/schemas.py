import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType

User = get_user_model()

class AccountType(DjangoObjectType):
    class Meta:
        model = User
        fields = [
            "user_id",
            "person_id",
            "business_id",
            
            "email",
            "username",
            "first_name",
            "last_name",
            "business_name",
            "role",
            "tel",
            "dob",
            
            "zip_code",
            "address_line",
            "city",
            "state",
            "country",
            
            "is_active",
            "is_verified",
        ]
        
class Query(graphene.ObjectType):
    users = graphene.List(AccountType)
    user  = graphene.Field(AccountType, user_id=graphene.ID(required=True))

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_user(self, info, user_id=None):
        if not user_id:
            raise ValueError("Must provide an ID")
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class CreateAccountType(DjangoObjectType):
    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "business_name",
            "role",
            "tel",
            "dob",
            
            "zip_code",
            "address_line",
            "city",
            "state",
            "country",
        ]

class CreateUser(graphene.Mutation):
    class Arguments:
        email           = graphene.String(required=True)
        username        = graphene.String()
        password        = graphene.String(required=True)
        first_name      = graphene.String()
        last_name       = graphene.String()
        dob             = graphene.Date()
        tel             = graphene.String()
        
        business_name   = graphene.String()
        role            = graphene.String()
        
        address_line    = graphene.String()
        city            = graphene.String()
        state           = graphene.String()
        zip_code        = graphene.Int()
        country         = graphene.String()
        
    account = graphene.Field(CreateAccountType)
    
    @staticmethod
    def mutate(root, info, **data):
        # Validate input data here if necessary
        new_account = User(**data)
        new_account.set_password(data.get('password'))
        new_account.save()
        return CreateUser(account=new_account)

schema = graphene.Schema(query=Query, mutation=CreateUser)