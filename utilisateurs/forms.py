from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from utilisateurs.models import Users

class SignupForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Firstname'})
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lastname'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmer le mot de passe'})
    )

    class Meta:
        model = Users
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']  # Garde ces champs
    # Personnalisation pour masquer 'username', 'first_name', 'last_name'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = ''  # Enlever le texte du label
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        # Tu peux gérer des cas particuliers ici (compte désactivé, etc.)
        pass

    error_messages = {
        'invalid_login': "Email ou mot de passe incorrect. Veuillez réessayer.",
        'inactive': "Ce compte est inactif.",
    }
