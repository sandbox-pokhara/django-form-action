from functools import wraps
from typing import Any
from typing import Callable
from typing import Type
from typing import TypeVar
from typing import cast

from django.contrib import admin
from django.db.models import Model
from django.db.models import QuerySet
from django.forms import Form
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render


def render_form(
    modeladmin: "admin.ModelAdmin[M]",
    request: HttpRequest,
    form: Form,
    title: str,
    action: str = "",
    qs: Any = None,
):
    context = {
        "site_header": admin.site.site_header,
        "site_title": admin.site.site_title,
        "title": title,
        "action": action,
        "form": form,
        "queryset": qs,
        "cl": modeladmin.get_changelist_instance(request),
        "opts": modeladmin.model._meta,
    }
    return HttpResponse(
        render(request, "django_form_action/intermediate.html", context)
    )


F = TypeVar("F", bound=Form)
M = TypeVar("M", bound=Model)


def form_action(
    model_cls: Type[M],  # only used for typing
    form_cls: Type[F],
    description: str,
    pre_render_form: (
        Callable[["admin.ModelAdmin[M]", HttpRequest, QuerySet[M], F], Any]
        | None
    ) = None,
):
    """
    :param pre_render: Runs before form is rendered in intermediate page,
    can be used to make modifications to form dynamically
    """

    def decorator(
        func: Callable[
            ["admin.ModelAdmin[M]", HttpRequest, QuerySet[M], F],
            HttpResponse | None,
        ],
    ) -> Callable[
        ["admin.ModelAdmin[M]", HttpRequest, QuerySet[M]], HttpResponse | None
    ]:
        @wraps(func)
        def wrapper(
            modeladmin: "admin.ModelAdmin[M]",
            request: HttpRequest,
            queryset: QuerySet[M],
        ) -> HttpResponse | None:
            action = cast(str, request.POST["action"])
            if request.POST.get("submit") is not None:
                my_form = form_cls(request.POST, request.FILES)
                if my_form.is_valid():
                    # sucess
                    return func(modeladmin, request, queryset, my_form)
                # show form with errors
                return render_form(
                    modeladmin, request, my_form, description, action, queryset
                )
            else:
                # show an empty form
                form = form_cls()
                if pre_render_form is not None:
                    pre_render_form(modeladmin, request, queryset, form)
                return render_form(
                    modeladmin, request, form, description, action, queryset
                )

        wrapper.short_description = description  # type:ignore
        # required because django requires unique name for action names
        wrapper.__name__ = func.__name__
        return wrapper

    return decorator
