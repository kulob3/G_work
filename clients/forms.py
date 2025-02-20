from django.forms import ModelForm, BooleanField, DateInput

from clients.models import Client


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
            if field_name == 'date_of_birth':
                field.widget = DateInput(attrs={'type': 'date'})





class ClientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Client
        exclude = ['email']