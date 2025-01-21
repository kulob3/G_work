from django.forms import ModelForm, BooleanField
from service.models import Service


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'




class ServiceForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Service
        fields = '__all__'