from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Phone, Rating
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
import json

@csrf_exempt
@login_required
def rate_phone(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        data = json.loads(request.body)   
        phone_id = data.get('phone_id')   
        stars = data.get('stars')        
        phone = Phone.objects.get(id=phone_id)
        phone.rating_set.create(stars=stars, user=request.user)
        return JsonResponse({'status': 'ok'})
    else:
        return HttpResponseBadRequest('This endpoint only accepts AJAX POST requests')

def recommended_phones(request):
    viewed_manufacturer = request.session.get('viewed_manufacturer', None)
    if viewed_manufacturer is not None:
        # Get other phones from this manufacturer.
        recommended_phones = Phone.objects.filter(manufacturer__name=viewed_manufacturer)
    else:
        # If the user hasn't viewed any phones yet, just show some random ones.
        recommended_phones = Phone.objects.order_by('?')[:5]

    context = {
        'recommended_phones': recommended_phones,
    }
    return render(request, 'recommended_phones.html', context)

def view_phone(request, phone_id):
    phone = get_object_or_404(Phone, pk=phone_id)

    request.session['viewed_manufacturer'] = phone.manufacturer.name

    context = {
        'phone': phone,  
    }


    return render(request, 'phones/view_phone.html', context)

class MyMemberView(LoginRequiredMixin, View):
    pass

class MyAdminView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name='Administrators').exists()

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request, template_name = "web/login.html", context={"form":form})
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_group = Group.objects.get(name='Users')
            user.groups.add(user_group)
            user.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})
def browse_phones(request):
    name_query = request.GET.get('name')
    os_query = request.GET.get('os')
    manufacturer_query = request.GET.get('manufacturer')

    phones = Phone.objects.all()

    os_choices = Phone.objects.values_list('os', flat=True).distinct()
    manufacturer_choices = Phone.objects.values_list('manufacturer', flat=True).distinct()

    if name_query:
        phones = phones.filter(name__icontains=name_query)

    if os_query:
        phones = phones.filter(os=os_query)

    if manufacturer_query:
        phones = phones.filter(manufacturer=manufacturer_query)

    return render(request, 'browse_phones.html', {'phones': phones, 'os_choices': os_choices, 'manufacturer_choices': manufacturer_choices})

def home(request):
    return render(request, 'home.html')
def about(request):
    return render(request, 'about.html')
def phone_detail(request, phone_id):
    phone = get_object_or_404(Phone, pk=phone_id)
    return render(request, 'phone_detail.html', {'phone': phone})

