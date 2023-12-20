import re

from euanh_website.defaults import Session
from euanh_website.models import ContactSubmission


class ContactFormService:
    @classmethod
    def validate_email(cls, email):
        email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
        return email_regex.match(email) is not None

    @classmethod
    def submit(cls, name, email, message):
        if not cls.validate_email(email):
            raise ValueError("Invalid email address")
        with Session() as session:
            contact_submission = ContactSubmission(
                name=name, email=email, message=message
            )
            session.add(contact_submission)
            session.commit()
