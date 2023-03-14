from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.views.generic import TemplateView, FormView, CreateView, ListView, UpdateView, DeleteView, DetailView, View
from django.core.exceptions import ValidationError
from .forms import ContactUsForm, RegistrationFormSeller, RegistrationForm, RegistrationFormSeller2
from django.urls import reverse_lazy, reverse
from .models import SellerAdditional, CustomUser, Contact, Product, ProductInCart, Cart
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from firstproject import settings
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
# def index(request):
#     return render(request, 'firstapp/index.html')


class Index(TemplateView):
    template_name = 'firstapp/index.html'

    def get_context_data(self, **kwargs):
        age = 10
        arr = ['ali', 'ahmad', 'asad']
        dic = {'a': 'one', 'b': 'two'}
        context = {'age': age, 'array': arr, 'dic': dic}
        return context


def contactus(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        query = request.POST.get('query')
        print(email)
        # print(name + email + phone + query)
    return render(request, 'firstapp/contactus.html')


def contactus2(request):
    if request.method == 'POST':
        # name = request.POST.get('name')
        # email = request.POST.get('email')
        # phone = request.POST.get('phone')
        # query = request.POST.get('query')
        # print(name + email + phone + query)
        # print(email)
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Thank You")
        else:
            return render(request, 'firstapp/contactus.html', {'form': form})
    return render(request, 'firstapp/contactus2.html', {'form': ContactUsForm})


class ContactUs(FormView):
    form_class = ContactUsForm
    template_name = 'firstapp/contactus2.html'
    # success_url = '/'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        if len(form.cleaned_data.get('query')) > 10:
            form.add_error('query', 'Query length is not valid')
            return render(self.request, 'firstapp/contactus2.html', {'form': form})
        form.save()
        response = super().form_valid(form)
        return response

    def form_invalid(self, form):
        if len(form.cleaned_data.get('query')) > 10:
            form.add_error('query', 'Query length is not valid')
            # form.errors['__all__'] = 'Query length is not right. It should be in 10 digits.')
        response = super().form_valid(form)
        return response


# class RegisterViewSeller(CreateView):
#     template_name = 'firstapp/register.html'
#     form_class = RegistrationForm
#     success_url = reverse_lazy('index')
#
# def post(self, request, *args, **kwargs):
#     response = super().post(request, *args, **kwargs)
#     if response.status_code == 302:
#         gst = request.POST.get('gst')
#         warehouse_location = request.POST.get('warehouse_location')
#         user = CustomUser.objects.get(email=request.POST.get('email'))
#         s_add = SellerAdditional.objects.create(user=user, gst=gst, warehouse_location=warehouse_location)
#         return response
#     else:
#         return response


class RegisterView(CreateView):
    template_name = 'firstapp/registerbasicuser.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('signup')

    def post(self, request, *args, **kwargs):
        # form = RegistrationForm(request.POST)
        user_email = request.POST.get('email')
        try:
            existing_user = CustomUser.objects.get(email=user_email)
            if existing_user.is_active == False:
                existing_user.delete()
        except:
            pass
        response = super().post(request, *args, **kwargs)
        if response.status_code == 302:
            user = CustomUser.objects.get(email=user_email)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate Your Account.'
            message = render_to_string('firstapp/registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            print(message)
            to_email = user_email
            # form = RegistrationForm(request.POST)   # here we are again calling all its validations
            form = self.get_form()
            try:
                send_mail(
                    subject=mail_subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[to_email],
                    fail_silently=False,
                    # if it fails due to some error or email id then it get silenced without affecting others
                )
                messages.success(request,
                                 "link has been sent to your email id. please check your inbox and if its not there "
                                 "check your spam as well.")
                return self.render_to_response({'form': form})
            except:
                form.add_error('', 'Error Occurred In Sending Mail, Try Again')
                messages.error(request, "Error Occurred In Sending Mail, Try Again")
                return self.render_to_response({'form': form})
        else:
            return response


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist) as e:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Successfully Logged In")
        return redirect(reverse_lazy('index'))
        # return HttpResponse('Thank you for your email confirmation. Now you can log in your account.')
    else:
        return HttpResponse('Activation link is invalid or your account is already Verified! Try To Login')


class LoginViewUser(LoginView):
    template_name = 'firstapp/login.html'
    # form_class = RegistrationForm
    # success_url = reverse_lazy('index')


class RegisterViewSeller(LoginRequiredMixin, CreateView):
    template_name = 'firstapp/registerseller.html'
    form_class = RegistrationFormSeller2
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = self.request.user
        user.type.append(user.Types.SELLER)
        user.save()
        form.instance.user = self.request.user
        return super().form_valid(form)


class LogoutViewUser(LogoutView):
    success_url = reverse_lazy('index')
