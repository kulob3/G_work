from django.forms import ModelForm, BooleanField
from django import forms

from clients.models import Client
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
    clients = forms.ModelMultipleChoiceField(
        queryset=Client.objects.none(),
        widget=forms.SelectMultiple,
        required=True
    )
    class Meta:
        model = Sending
        fields = '__all__'

class SendingManagerForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Sending
        fields = ['status']

class FeedbackForm(forms.Form):
    name = forms.CharField(max_length=100, label='Ваше имя')
    email = forms.EmailField(label='Ваш email')
    message = forms.CharField(widget=forms.Textarea, label='Сообщение')