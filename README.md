# django-form-action

Django action to add an intermediate page to parse form data

## Installation

```
pip install django-form-action
```

## Usage

```
from django.contrib import admin
from django.contrib import messages
from django.forms import CharField
from django.forms import Form

from dummyapp.models import Fruit
from form_action import form_action


class MyForm(Form):
    message = CharField()


@form_action(MyForm, description="Do some task")
def my_action(modeladmin, request, queryset, form):
    msg = form.cleaned_data["message"]
    messages.add_message(request, messages.INFO, f"Got message: {msg}")


@admin.register(Fruit)
class MyModelAdmin(admin.ModelAdmin):
    actions = [my_action]
```
