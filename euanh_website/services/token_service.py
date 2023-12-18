import secrets
from datetime import datetime, timezone

from euanh_website.defaults import Session
from euanh_website.models import UserToken


class TokenService:
    def __init__(self, token=None):
        self.token = token

    def verify(self):
        if not self.token:
            return False
        with Session() as session:
            token = session.query(UserToken).filter_by(token=self.token).first()
            if token is not None and token.expiry > datetime.now(timezone.utc):
                return True
            elif token is not None:
                session.delete(token)
                session.commit()
                return False
            else:
                return False

    def generate_token(self):
        return secrets.token_urlsafe(64)

    def create_token(self, user_id):
        with Session() as session:
            token = secrets.token_urlsafe(64)
            user_token = UserToken(user_id=user_id, token=token)
            session.add(user_token)
            session.commit()
            return token

    def delete_token(self):
        with Session() as session:
            token = session.query(UserToken).filter_by(token=self.token).first()
            session.delete(token)
            session.commit()
            return True
