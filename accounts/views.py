from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail,BadHeaderError
import logging
from django.contrib.auth import login
from .forms import CustomUserCreationForm

# Регистрация с отправкой письма
class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')  # замените на ваш url по имени

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = 'Добро пожаловать в наш сервис'
        message = 'Спасибо, что зарегистрировались в нашем сервисе!'
        from_email = None
        recipient_list = [user_email]
        try:
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            logging.error(f"Ошибка при отправке письма: {e}")

# Вход пользователя
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('home')  # куда перенаправлять после логина

# Выход пользователя
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')