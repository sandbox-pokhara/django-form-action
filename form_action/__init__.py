
from django.contrib import admin
from django.http import HttpResponse
from django.template import RequestContext
from django.template import Template

template = Template('''
{% extends "admin/base_site.html" %}
{% load admin_urls static l10n %}
{% block extrastyle %}
  {{ block.super }}
  <link rel="stylesheet"
        type="text/css"
        href="{% static "admin/css/forms.css" %}">
{% endblock %}
{% block content %}
  <div id="content-main">
    <form method="post">
      {% csrf_token %}
      {% for obj in queryset.all %}<input type="hidden" name="_selected_action" value="{{ obj.pk|unlocalize }}"/>{% endfor %}
      <div>
        {% if form.errors %}<p class="errornote">Please correct the errors below.</p>{% endif %}
        <fieldset class="module aligned wide">
          {% for field in form %}
            <div class="form-row">
              {{ field.errors }}
              {{ field.label_tag }} {{ field }}
              {% if field.help_text %}<div class="help">{{ field.help_text|safe }}</div>{% endif %}
            </div>
          {% endfor %}
        </div>
      </fieldset>
      <div class="submit-row">
        <input type="hidden" name="action" value="{{ action }}"/>
        <input type="submit" name="submit" value="Submit" class="default" />
      </div>
    </form>
  </div>
{% endblock %}
''')


def form_action(form, description):
    def decorator(func):
        def wrapper(modeladmin, request, queryset):
            if request.POST.get('submit') is not None:
                my_form = form(request.POST)
                if my_form.is_valid():
                    return func(modeladmin, request, queryset, my_form)
            else:
                my_form = form()
            context = {
                'action': request.POST['action'],
                'queryset': queryset,
                'site_header': admin.site.site_header,
                'site_title': admin.site.site_title,
                'title': description,
                'form': my_form,
            }
            context = RequestContext(request, context)
            return HttpResponse(template.render(context))
        wrapper.short_description = description
        # required because django requires unique name for action names
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator
