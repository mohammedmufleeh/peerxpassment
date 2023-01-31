from django import forms
from .models import User, Department

class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'password', 'user_department', 'role']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = False
        self.fields['phone'].required = False
        self.fields['password'].required = True

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        phone = cleaned_data.get("phone")

        if not email and not phone:
            raise forms.ValidationError("Email or Phone Number is required.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class DepartmentCreateForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('name', 'description')


class NewTicketForm(forms.Form):
    subject = forms.CharField(max_length=255)
    body = forms.CharField(widget=forms.Textarea)
    priority = forms.ChoiceField(choices=[('low', 'Low'), ('normal', 'Normal'), ('high', 'High'),('urgent','Urgent')])
    email = forms.EmailField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))

