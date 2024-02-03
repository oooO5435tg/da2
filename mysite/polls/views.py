from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, get_object_or_404
from .models import User, Service, Order
from django.views import generic
from .forms import RegisterUserForm
from django.views.generic import UpdateView, CreateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import HttpResponseBadRequest


def index(request):
    service_list = Service.objects.order_by('-service_date')[:5]
    return render(request, 'index.html', {'service_list': service_list})


def my_services(request):
    service_list = Service.objects.filter(username=request.user)
    return render(request, 'polls/service_list.html', {'service_list': service_list})

def services_all(request):
    service_list = Service.objects.all()
    return render(request, 'polls/services_all.html', {'service_list': service_list})


class SepServiceView(LoginRequiredMixin, generic.DetailView):
    pk_url_kwarg = 'id'
    model = Service
    template_name = 'polls/separate_service.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:  # Проверяем аутентификацию пользователя
            context['orders'] = Order.objects.filter(user=self.request.user, service=self.object)
        return context

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:  # Проверяем аутентификацию пользователя
            service = self.get_object()
            order = Order(user=request.user, service=service)
            order.save()
            messages.success(request, 'Услуга/товар успешно заказана')
            return redirect('polls:profile')
        else:
            return redirect('polls:login')



def order_service(request, service_id):
    # Получаем объект услуги/товара по его идентификатору
    try:
        service = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        return HttpResponseBadRequest('Услуга/товар не найден')

    # Проверяем, является ли пользователь авторизованным
    if not request.user.is_authenticated:
        return HttpResponseBadRequest('Пользователь не авторизован')

    else:
        # Добавляем услугу/товар в список заказанных услуг/товаров текущего пользователя
        order = Order(user=request.user, service=service)
        order.save()
        messages.success(request, 'Услуга/товар успешно заказана')

        # Перенаправляем на страницу профиля пользователя
        return redirect('polls:profile')


class StudioLoginView(LoginView):
    template_name = 'registration/login.html'


class StudioLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'registration/login.html'


class RegisterUserView(CreateView):
    model = User
    template_name = 'registration/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('polls:login')


@login_required
def profile(request):
    current_user = request.user
    service_list = Order.objects.filter(user=current_user)
    context = {'service_list': service_list}
    return render(request, 'registration/profile.html', context)

def search_service(request):
    query = request.GET.get('query', '')
    results = []

    if query:
        results = Service.objects.filter(service_name__icontains=query)

    context = {'results': results}
    return render(request, "polls/service_search.html", context)
