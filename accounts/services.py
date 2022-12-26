import dataclasses
import datetime
import jwt
from . import models
from django.conf import settings
from typing import TYPE_CHECKING


"""
cette classe UserDataClass permet de transformer le retour dict
register en un format convenable
"""

if TYPE_CHECKING:
    from .models import User

@dataclasses.dataclass
class UserDataClass:
    first_name: str
    last_name: str
    email: str
    password: str = None
    id: int = None

    @classmethod
    def from_instance(cls, user: "User") -> "UserDataClass":

        return cls(
           first_name=user.first_name,
           last_name=user.last_name,
           email=user.email,
           id=user.id
        )

"""
creer et enregistrer l'utilisateur
"""
def create_user(user_dc: 'UserDataClass') -> "UserDataClass":
    instance = models.User(
        first_name=user_dc.first_name,
        last_name=user_dc.last_name,
        email=user_dc.email 
    )

    if user_dc.password is not None:
        instance.set_password(user_dc.password)
    instance.save()

    return UserDataClass.from_instance(instance)


def user_email_selector(email:str) -> "User":
    user = models.User.objects.filter(email=email).first()

    return user 

def create_token(user_id:int) -> str:
    payload = dict(
        id=user_id,
        exp=datetime.datetime.utcnow() + datetime.timedelta(hours=24), #delais d'expiration
        iat=datetime.datetime.utcnow()
    )
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

    return token