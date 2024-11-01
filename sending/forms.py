from django.forms import ModelForm, BooleanField

from sending.models import Sending


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'




class SendingForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Sending
        fields = '__all__'

class SendingManagerForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Sending
        fields = ['status']