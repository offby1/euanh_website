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
        ContactSubmission.read,
        ContactSubmission.spam,
        ContactSubmission.created_on,
    ]

    form_excluded_columns = ["created_on", "updated_on"]

    column_default_sort = ("created_on", True)

    @action(
        name="mark_as_read",
        label="Mark as Read",
        confirmation_message="Are you sure you want to mark these submissions as read?",
        add_in_detail=True,
        add_in_list=True,
    )
    def action_mark_as_read(self, request: Request) -> RedirectResponse:
        pks = request.query_params.get("pks", "").split(",")
        if pks:
            pks = [int(pk) for pk in pks]
            with Session() as session:
                models = (
                    session.query(ContactSubmission)
                    .filter(ContactSubmission.id.in_(pks))
                    .all()
                )
                for model in models:
                    model.read = True
                session.commit()

        referer = request.headers.get("Referer")
        if referer:
            return RedirectResponse(referer)
        return RedirectResponse(request.url_for("admin:list", identity=self.identity))

    @action(
        name="mark_as_unread",
        label="Mark as Unread",
        confirmation_message="Are you sure you want to mark these submissions as unread?",
        add_in_detail=True,
        add_in_list=True,
    )
    def action_mark_as_unread(self, request: Request) -> RedirectResponse:
        pks = request.query_params.get("pks", "").split(",")
        if pks:
            pks = [int(pk) for pk in pks]
            with Session() as session:
                models = (
                    session.query(ContactSubmission)
                    .filter(ContactSubmission.id.in_(pks))
                    .all()
                )
                for model in models:
                    model.read = False
                session.commit()

        referer = request.headers.get("Referer")
        if referer:
            return RedirectResponse(referer)
        return RedirectResponse(request.url_for("admin:list", identity=self.identity))

    @action(
        name="mark_as_spam",
        label="Mark as Spam",
        confirmation_message="Are you sure you want to mark these submissions as spam?",
        add_in_detail=True,
        add_in_list=True,
    )
    def action_mark_as_spam(self, request: Request) -> RedirectResponse:
        pks = request.query_params.get("pks", "").split(",")
        if pks:
            pks = [int(pk) for pk in pks]
            with Session() as session:
                models = (
                    session.query(ContactSubmission)
                    .filter(ContactSubmission.id.in_(pks))
                    .all()
                )
                for model in models:
                    model.spam = True
                session.commit()

        referer = request.headers.get("Referer")
        if referer:
            return RedirectResponse(referer)
        return RedirectResponse(request.url_for("admin:list", identity=self.identity))

    @action(
        name="mark_as_not_spam",
        label="Mark as Not Spam",
        confirmation_message="Are you sure you want to mark these submissions as not spam?",
        add_in_detail=True,
        add_in_list=True,
    )
    def action_mark_as_not_spam(self, request: Request) -> RedirectResponse:
        pks = request.query_params.get("pks", "").split(",")
        if pks:
            pks = [int(pk) for pk in pks]
            with Session() as session:
                models = (
                    session.query(ContactSubmission)
                    .filter(ContactSubmission.id.in_(pks))
                    .all()
                )
                for model in models:
                    model.spam = False
                session.commit()

        referer = request.headers.get("Referer")
        if referer:
            return RedirectResponse(referer)
        return RedirectResponse(request.url_for("admin:list", identity=self.identity))
