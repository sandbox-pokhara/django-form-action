# django-form-action

Django action to add an intermediate page to parse form data

## Installation

```
pip install django-form-action
```

# Usage

```
@form_action(MyForm, description='Some Label')
def my_django_admin_action(modeladmin, request, queryset, form):
    ...
    ...
    ...
```
