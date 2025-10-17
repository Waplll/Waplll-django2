
from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .models import user_registrated, AdvUser


class ChangeUserInfoForm(forms.ModelForm):
   email = forms.EmailField(required=True, label='Адрес электронной почты')

   class Meta:
       model = AdvUser
       fields = ('username', 'email', 'fio')

class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html()
    )
    password2 = forms.CharField(
        label='Пароль (повторно)',
        widget=forms.PasswordInput,
        help_text='Повторите тот же самый пароль еще раз'
    )
    fio = forms.CharField(label='ФИО', max_length=100)
    username = forms.CharField(label='Логин', max_length=30)
    consent = forms.BooleanField(label='Согласие на обработку персональных данных')

    def clean_fio(self):
        fio = self.cleaned_data.get('fio')
        valid_characters = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯа-бвгдеёжзийклмнопрстуфхцчшщъыьэюя '

        if not all(char in valid_characters for char in fio):
            raise ValidationError('ФИО может содержать только кириллические буквы, пробелы и дефисы.')

        if not any(char in 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯа' for char in fio):
            raise ValidationError('ФИО должно содержать хотя бы одну кириллическую букву.')

        return fio

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if AdvUser.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким адресом электронной почты уже существует.')
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', ValidationError(
                'Введенные пароли не совпадают.'
            ))

    def clean_consent(self):
        consent = self.cleaned_data.get('consent')
        if not consent:
            raise ValidationError('Необходимо дать согласие на обработку персональных данных.')
        return consent

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = True
        user.is_activated = True
        if commit:
            user.save()
            # Отправка сигнала о регистрации пользователя
            user_registrated.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = AdvUser
        fields = ('username', 'fio', 'email', 'password1', 'password2', 'consent')