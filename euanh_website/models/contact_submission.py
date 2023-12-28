from sqlalchemy import Boolean, Column, Integer, String, Text

from euanh_website.models.base import CommonBase


class ContactSubmission(CommonBase):
    __tablename__ = "contact_submissions"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    read = Column(Boolean, nullable=False, default=False)
    spam = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<ContactSubmission(name='{self.name}', email='{self.email}')>"
