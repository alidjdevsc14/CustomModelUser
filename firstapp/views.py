from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView, FormView
from .forms import ContactUsForm
from django.urls import reverse_lazy


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

