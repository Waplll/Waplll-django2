from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy


from .forms import ChangeUserInfoForm
from .models import AdvUser
from django.contrib.auth.views import PasswordChangeView
from .forms import RegisterUserForm
from django.views.generic import UpdateView, CreateView, TemplateView, DeleteView



def index(request):
   return render(request, 'main/index.html')



@login_required
def profile(request):
   return render(request, 'main/profile.html')


class BBLoginView(LoginView):
   template_name = 'main/login.html'


class BBLogoutView(LoginRequiredMixin, LogoutView):
   template_name = 'main/logout.html'


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin,UpdateView):
   model = AdvUser
   template_name = 'main/change_user_info.html'
   form_class = ChangeUserInfoForm
   success_url = reverse_lazy('main:profile')
   success_message = 'Личные данные пользователя изменены'


   def dispatch(self, request, *args, **kwargs):
       self.user_id = request.user.pk
       return super().dispatch(request, *args, **kwargs)


   def get_object(self, queryset=None):
       if not queryset:
           queryset = self.get_queryset()
       return get_object_or_404(queryset, pk=self.user_id)


class BBPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
   template_name = 'main/password_change.html'
   success_url = reverse_lazy('main:profile')
   success_message = 'Пароль пользователя изменен'



class RegisterUserView(CreateView):
   model = AdvUser
   template_name = 'main/register_user.html'
   form_class = RegisterUserForm
   success_url = reverse_lazy('main:register_done')


class RegisterDoneView(TemplateView):
   template_name = 'main/register_done.html'

class DeleteUserView(LoginRequiredMixin, DeleteView):
   model = AdvUser
   template_name = 'main/delete_user.html'
   success_url = reverse_lazy('main:index')

   def dispatch(self, request, *args, **kwargs):
       self.user_id = request.user.pk
       return super().dispatch(request, *args, **kwargs)

   def post(self, request, *args, **kwargs):
       logout(request)
       messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
       return super().post(request, *args, **kwargs)

   def get_object(self, queryset=None):
       if not queryset:
           queryset = self.get_queryset()
       return get_object_or_404(queryset, pk=self.user_id)