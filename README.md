# django-form-action

Django action/button with an intermediate page to parse data from a form

## Installation

Just install the pakage from PyPI

```
pip install django-form-action
```

## Usage

Django admin action with form
![Demo Form Action](https://raw.githubusercontent.com/sandbox-pokhara/django-form-action/master/demo/form-action.gif)

```python
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

Or use it as an extra button with form
![Demo Extra Button](https://raw.githubusercontent.com/sandbox-pokhara/django-form-action/master/demo/extra-button.gif)

```python
from django.contrib import admin
from django.forms import CharField
from django.forms import Form
from django.http.response import HttpResponse

from dummyapp.models import Fruit
from form_action.decorators import extra_button
from form_action.mixins import ExtraButtonMixin


class MyForm(Form):
    message = CharField()


@extra_button("Test Button", MyForm)
def test(request, form):
    msg = form.cleaned_data["message"]
    return HttpResponse(f"Got message: {msg}")


@admin.register(Fruit)
class MyModelAdmin(ExtraButtonMixin, admin.ModelAdmin):
    extra_buttons = [test]

```
