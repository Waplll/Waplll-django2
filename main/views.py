from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import UpdateView, CreateView, TemplateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import ChangeUserInfoForm, RegisterUserForm, CreateRequestForm, ChangeRequestStatusForm, CategoryForm
from .models import AdvUser, CreateRequest, Category


def index(request):
    completed_requests = CreateRequest.objects.filter(status='completed').order_by('-timestamp')[:4]
    inprogress_count = CreateRequest.objects.filter(status='inprogress').count()
    context = {
        'completed_requests': completed_requests,
        'inprogress_count': inprogress_count
    }
    return render(request, 'main/index.html', context)


@login_required
def profile(request):
    return render(request, 'main/profile.html')


class BBLoginView(LoginView):
    template_name = 'main/login.html'


class BBLogoutView(LogoutView):
    template_name = 'main/logout.html'
    next_page = 'main:index'


class ChangeUserInfoView(LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('main:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Данные профиля успешно обновлены!')
        return super().form_valid(form)


class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'main/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        messages.success(self.request, 'Регистрация успешна! Вы можете авторизоваться.')
        return super().form_valid(form)


# Представление для создания заявки
class CreateRequestView(LoginRequiredMixin, CreateView):
    model = CreateRequest
    form_class = CreateRequestForm
    template_name = 'main/create_request.html'
    success_url = reverse_lazy('main:user_requests')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = 'new'
        messages.success(self.request, 'Заявка успешно создана!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при создании заявки. Проверьте введенные данные.')
        return super().form_invalid(form)


# Представление для просмотра заявок пользователя (обычный пользователь) или всех заявок (админ)
@login_required
def user_requests(request):
    if request.user.is_staff or request.user.is_superuser:
        # Админ видит все заявки
        requests_list = CreateRequest.objects.all().order_by('-timestamp')
        is_admin = True
    else:
        # Обычный пользователь видит только свои заявки
        requests_list = CreateRequest.objects.filter(user=request.user).order_by('-timestamp')
        is_admin = False

    context = {
        'user_requests': requests_list,
        'is_admin': is_admin,
    }
    return render(request, 'main/user_requests.html', context)


# Проверка прав админа
class IsAdminUser(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


# Представление для удаления заявки (только для админа)
class DeleteRequestView(LoginRequiredMixin, IsAdminUser, DeleteView):
    model = CreateRequest
    success_url = reverse_lazy('main:user_requests')
    template_name = 'main/delete_request_confirm.html'

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Заявка успешно удалена!')
        return super().delete(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для удаления заявок. Только администраторы могут удалять заявки.')
        return redirect('main:user_requests')


# Представление для смены статуса заявки (только для админа)
@login_required
def change_request_status(request, pk):
    # Проверка прав админа
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request,
                       'У вас нет прав для изменения статуса заявок. Только администраторы могут менять статус.')
        return redirect('main:user_requests')

    request_obj = get_object_or_404(CreateRequest, pk=pk)

    if request.method == 'POST':
        form = ChangeRequestStatusForm(request.POST, instance=request_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статус заявки успешно изменен!')
            return redirect('main:user_requests')
    else:
        form = ChangeRequestStatusForm(instance=request_obj)

    context = {
        'form': form,
        'request_obj': request_obj,
    }
    return render(request, 'main/change_request_status.html', context)


# Представление для управления категориями
@login_required
def manage_categories(request):
    categories = Category.objects.all().order_by('name')
    context = {
        'categories': categories,
    }
    return render(request, 'main/manage_categories.html', context)


# Представление для создания категории
@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория успешно создана!')
            return redirect('main:manage_categories')
    else:
        form = CategoryForm()

    context = {
        'form': form,
    }
    return render(request, 'main/create_category.html', context)


# Представление для редактирования категории
@login_required
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория успешно обновлена!')
            return redirect('main:manage_categories')
    else:
        form = CategoryForm(instance=category)

    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'main/edit_category.html', context)


# Представление для удаления категории
@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Категория успешно удалена!')
        return redirect('main:manage_categories')

    context = {
        'category': category,
    }
    return render(request, 'main/delete_category_confirm.html', context)