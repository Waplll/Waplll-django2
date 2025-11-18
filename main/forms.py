from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .models import user_registrated, AdvUser, CreateRequest, Category
import re


class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'fio')
        labels = {
            'username': 'Имя пользователя',
            'email': 'Email',
            'fio': 'ФИО',
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if AdvUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Пользователь с этим email уже существует')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if AdvUser.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Пользователь с этим именем уже существует')
        return username


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'password1', 'password2', 'fio')
        labels = {
            'username': 'Имя пользователя',
            'email': 'Email',
            'fio': 'ФИО',
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(r'^[\w.@+-]+$', username):
            raise ValidationError('Имя пользователя содержит недопустимые символы')
        if AdvUser.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с этим именем уже существует')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if AdvUser.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с этим email уже существует')
        return email

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        try:
            password_validation.validate_password(password1)
        except ValidationError as e:
            raise ValidationError(e.messages)
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Пароли не совпадают')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = True
        if commit:
            user.save()
            user_registrated.send(sender=self.__class__, instance=user)
        return user


class CreateRequestForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='Категория',
        required=False,
        empty_label='Выберите категорию (необязательно)'
    )

    photo = forms.ImageField(
        label='Фото помещения',
        required=False,
        help_text='Максимальный размер: 2 МБ. Форматы: JPG, PNG, BMP'
    )

    class Meta:
        model = CreateRequest
        fields = ('title', 'description', 'category', 'photo')
        labels = {
            'title': 'Название заявки',
            'description': 'Описание требований к дизайну',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            from .validations import validate_image
            validate_image(photo)
        return photo

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title.strip()) < 3:
            raise ValidationError('Название должно содержать минимум 3 символа')
        return title

    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description.strip()) < 10:
            raise ValidationError('Описание должно содержать минимум 10 символов')
        return description


class ChangeRequestStatusForm(forms.ModelForm):
    class Meta:
        model = CreateRequest
        fields = ('status',)
        labels = {
            'status': 'Статус заявки',
        }
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
        labels = {
            'name': 'Название категории',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name.strip()) < 2:
            raise ValidationError('Название должно содержать минимум 2 символа')
        return name