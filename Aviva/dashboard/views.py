from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from .models import AllUsers
from .auth_backends import LegacyModelBackend
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import hashlib
from django.views.generic import ListView,  DetailView
from .forms import *
from django.views.generic import TemplateView
from django.contrib import messages
from django.utils.decorators import method_decorator



# Custom decorator to check if the user is logged in
def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'user_id' in request.session:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')  # Replace 'login' with your actual login URL pattern

    return wrapper

@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = AllUsers.objects.get(email=email)

            # Check if the provided password matches the stored MD5 hash
            md5_hash = hashlib.md5(password.encode()).hexdigest()
            if md5_hash == user.password:
                # Passwords match, authenticate the user
                request.session['user_id'] = user.userid
                return redirect('dashboard')
            else:
           
                return HttpResponse("Login failed")

        except AllUsers.DoesNotExist:
            return HttpResponse("user doesnt exist")

    return render(request, 'registration/login.html')

@method_decorator(login_required, name='dispatch')
class ReviewedListView(ListView):
    model = CervicData
    template_name = 'dashboard/reviewed.html'
    context_object_name = 'cervic_data'

    def get_queryset(self):
        # Filter the queryset to exclude entries where final_diagnosis_by is empty
        return CervicData.objects.exclude(final_diagnosis_by__exact='')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PendingListView(ListView):
    model = CervicData
    template_name = 'dashboard/pending.html'
    context_object_name = 'cervic_data'

    def get_queryset(self):
        # Filter the queryset to include entries where final_diagnosis_by is empty
        return CervicData.objects.filter(final_diagnosis_by='')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CervicDataDetailView(DetailView):
    model = CervicData
    template_name = 'dashboard/detail.html'
    context_object_name = 'cervic_data'
    def get_context_data(self, *args, **kwargs):
        # Access the 'pk' parameter from self.kwargs
        context = super(CervicDataDetailView, self).get_context_data(*args, **kwargs)
        return context





def my_form_view(request):
    # You can add your logic for rendering the form with available states here.
    states = CervicData.objects.values_list('state', flat=True).distinct()
    return render(request, 'test.html', {'states': states})

def filter_cervic_data(request):
    cervic_data = CervicData.objects.all()
    selected_state = None
    selected_facility = None

    if request.method == 'POST':
        form = FacilityFilterForm(request.POST)
        if form.is_valid():
            selected_state = form.cleaned_data.get('state')
            selected_facility = form.cleaned_data.get('facility')

            if selected_facility != 'All Facilities':
                cervic_data = cervic_data.filter(facility=selected_facility)
        else:
            cervic_data = CervicData.objects.all()
    else:
        form = FacilityFilterForm()

    context = {
        'cervic_data': cervic_data,
        'form': form,
        'selected_state': selected_state,
        'selected_facility': selected_facility,
    }

    return render(request, 'dashboard/report.html', context)
    #return render(request, 'test.html', context)



def get_facilities(request):
    state_id = request.GET.get('state_id')
    facilities = CervicData.objects.filter(state=state_id).values_list('facility', flat=True).distinct()
    facilities_dict = {facility: facility for facility in facilities}
    return JsonResponse({'facilities': facilities_dict})

def home(request):
    return render(request, 'home/index.html')


def pending(request):
    return render(request, 'dashboard/pending.html')

def analytics(request):
    return render(request, 'dashboard/analysis.html')


@csrf_exempt
@login_required
def dashboard(request):
    return render(request, 'dashboard/dash.html')