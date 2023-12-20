from fastapi import Request
from fastapi.responses import RedirectResponse
from sqladmin import ModelView, action

from euanh_website.defaults import Session, templates
from euanh_website.models import ContactSubmission


class ContactSubmissionView(ModelView, model=ContactSubmission):
    column_list = [
        ContactSubmission.id,
        ContactSubmission.name,
        ContactSubmission.email,
        ContactSubmission.created_on,
    ]

    form_excluded_columns = ["created_on", "updated_on"]
