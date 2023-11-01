from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from .models import AllUsers,CustomUser
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import hashlib

def user_login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        pass1=request.POST.get('password')
        md5 = hashlib.md5()
        md5.update(pass1.encode('utf-8'))
        md5_hash = md5.hexdigest()
       
        user = AllUsers.objects.get(email=email)

        if user.password== md5_hash:
            return redirect('dashboard')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'registration/login.html')


def home(request):
    return render(request, 'home/index.html')

def dashboard(request):
    return render(request, 'dashboard/dash.html')



def reviewed(request):
    cervic_data = CervicData.objects.all()
    return render(request, 'dashboard/reviewed.html', {'cervic_data': cervic_data})

def cervic_data_detail(request, cervic_data_id):
    cervic_data = get_object_or_404(CervicData, pk=cervic_data_id)
    return render(request, 'dashboard/detail.html', {'cervic_data': cervic_data})




from django.views.generic.list import ListView
from yourapp.models import CervicData  # Import your model

class ReviewedListView(ListView):
    model = CervicData
    template_name = 'dashboard/reviewed.html'
    context_object_name = 'cervic_data'

    def get_queryset(self):
        # Filter the queryset to include entries where final_diagnosis_by is empty
        return CervicData.objects.filter(final_diagnosis_by='')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Calculate the total count of data where final_diagnosis_by is empty
        total_empty_final_diagnosis = self.get_queryset().count()
        context['total_empty_final_diagnosis'] = total_empty_final_diagnosis
        return context


<div>
    <p>Total Data with Final Diagnosis By Empty: {{ total_empty_final_diagnosis }}</p>
</div>
