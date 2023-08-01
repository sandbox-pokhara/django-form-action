from urllib.parse import urljoin

from django.template import engines
from django.urls import path

template = engines["django"].from_string("""
{% extends "admin/change_list.html" %}
{% block object-tools-items %}
  {% for button in extra_buttons %}
    <li>
      <a href="{{ button.url }}">
        {{ button.title }}
      </a>
    </li>
  {% endfor %}
  {{ block.super }}
{% endblock %}
""")


class ExtraButtonMixin:
    change_list_template = template

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_buttons = getattr(self, "extra_buttons", [])
        extra_buttons = [
            {
                "name": b.name,
                "title": b.title,
                "url": urljoin(request.path, f"actions/{b.name}/"),
            }
            for b in extra_buttons
        ]
        extra_context.update({"extra_buttons": extra_buttons})
        return super().changelist_view(request, extra_context)

    def get_urls(self):
        urls = super().get_urls()
        return self.get_extra_urls() + urls

    def get_extra_urls(self):
        extra_buttons = getattr(self, "extra_buttons", [])
        return [
            path(f"actions/{func.name}/", self.admin_site.admin_view(func))
            for func in extra_buttons
        ]
