from fastapi import Request
from fastapi.responses import RedirectResponse
from sqladmin import ModelView, action

from euanh_website.defaults import Session
from euanh_website.models import BlogPost


class BlogPostView(ModelView, model=BlogPost):
    column_list = [
        BlogPost.id,
        BlogPost.title,
        BlogPost.is_published,
        BlogPost.preview,
        BlogPost.author,
        BlogPost.created_on,
        BlogPost.updated_on,
    ]

    form_excluded_columns = ["created_on", "updated_on"]

    column_default_sort = ("created_on", True)

    edit_template = "blog_post_admin_edit.jinja"
    create_template = "blog_post_admin_create.jinja"

    @action(
        name="publish_articles",
        label="Publish Articles",
        confirmation_message="Are you sure you want to publish these articles?",
        add_in_detail=True,
        add_in_list=True,
    )
    def action_publish(self, request: Request) -> RedirectResponse:
        pks = request.query_params.get("pks", "").split(",")
        if pks:
            pks = [int(pk) for pk in pks]
            with Session() as session:
                models = session.query(BlogPost).filter(BlogPost.id.in_(pks)).all()
                for model in models:
                    model.is_published = True
                session.commit()

        referer = request.headers.get("Referer")
        if referer:
            return RedirectResponse(referer)
        return RedirectResponse(request.url_for("admin:list", identity=self.identity))

    @action(
        name="unpublish_articles",
        label="Unpublish Articles",
        confirmation_message="Are you sure you want to unpublish these articles?",
        add_in_detail=True,
        add_in_list=True,
    )
    def action_unpublish(self, request: Request) -> RedirectResponse:
        pks = request.query_params.get("pks", "").split(",")
        if pks:
            pks = [int(pk) for pk in pks]
            with Session() as session:
                models = session.query(BlogPost).filter(BlogPost.id.in_(pks)).all()
                for model in models:
                    model.is_published = False
                session.commit()

        referer = request.headers.get("Referer")
        if referer:
            return RedirectResponse(referer)
        return RedirectResponse(request.url_for("admin:list", identity=self.identity))
