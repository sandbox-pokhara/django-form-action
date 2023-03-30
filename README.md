# django-form-action

Django action to add an intermediate page to parse form data

## Installation

```
pip install django-form-action
```

# Usage

```
from django.contrib import admin
from form_action import form_action


@form_action(MyForm, description='Some Label')
def my_django_admin_action(modeladmin, request, queryset, form):
    print(form.cleaned_data['my_field'])


class MyModelAdmin(admin.ModelAdmin):
       actions = [my_django_admin_action]

```
