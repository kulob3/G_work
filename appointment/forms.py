from django.forms import ModelForm, BooleanField, DateInput, TimeInput
from appointment.models import Appointment


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class AppointmentForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Appointment
        exclude = ['name', 'client', 'appointment_number_int', 'price', 'status']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
            'time': TimeInput(attrs={'type': 'time'}),
        }

class AdminAppointmentForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Appointment
        exclude = ['appointment_number_int']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
            'time': TimeInput(attrs={'type': 'time'}),
        }