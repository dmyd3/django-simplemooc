from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(UserCreationForm):

    #email = forms.EmailField(label="E-Mail") #desnecessario pois já está no fields
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmação de Senha', widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                'A confirmação de senha nao está correta',
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        #user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
                
        if commit:
            user.save()
        return user
    
    class Meta:
        model = User
        fields = ['username', 'email']

class EditAccountForm(forms.ModelForm):

    class Meta:
        model = User
        #fields eh uma lista com os campos a serem alterados
        fields = ['username','email','first_name','last_name']