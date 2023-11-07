from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView,  DetailView, TemplateView
from .forms import FacilityFilterForm
from django.utils.decorators import method_decorator
import hashlib
from .models import AllUsers,CervicData
from .decorators import login_required
import matplotlib.pyplot as plt
from django.db.models import Count, Case, When, IntegerField
import base64
from django.db.models import Q 
from io import BytesIO  # Import BytesIO
from django.views import View
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.core.exceptions import SuspiciousOperation








@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = AllUsers.objects.get(email=email)

            # Calculate the MD5 hash of the provided password
            provided_md5_hash = hashlib.md5(password.encode()).hexdigest()

            # Check if the provided MD5 hash matches the legacy MD5 hash
            if provided_md5_hash == user.password:
                request.session['userid'] = user.userid
                return redirect('dashboard')
            else:
                return HttpResponse('error')

        except AllUsers.DoesNotExist:
            pass  # User not found
    return render(request, 'registration/login.html')

def logout(request):
    if 'userid' in request.session:
        session_key = request.session.session_key
        request.session.flush()  # Clear the session data
        Session.objects.filter(session_key=session_key).delete()  # Delete the session from the database
    return redirect('login')  # Redirect to the login page after logout


@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'dashboard/dash.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # a) Total number of patients
        total_patients = CervicData.objects.count()
        context['total_patients'] = total_patients

        # b) Total number of patients with final diagnosis data
        patients_with_final_diagnosis = CervicData.objects.exclude(final_diagnosis='').count()
        context['patients_with_final_diagnosis'] = patients_with_final_diagnosis

        # c) Total number of patients without final diagnosis data
        patients_without_final_diagnosis = CervicData.objects.filter(final_diagnosis='').count()
        context['patients_without_final_diagnosis'] = patients_without_final_diagnosis

        # d) Total number of patients with initial_diagnosis as "positive"
        patients_with_positive_initial_diagnosis = CervicData.objects.filter(initial_diagnosis='positive').count()
        context['patients_with_positive_initial_diagnosis'] = patients_with_positive_initial_diagnosis

        return context


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

        # a) Total number of patients
        total_patients = CervicData.objects.count()
        context['total_patients'] = total_patients

        # b) Total number of patients with final diagnosis data
        patients_with_final_diagnosis = CervicData.objects.exclude(final_diagnosis='').count()
        context['patients_with_final_diagnosis'] = patients_with_final_diagnosis

        # c) Total number of patients without final diagnosis data
        patients_without_final_diagnosis = CervicData.objects.filter(final_diagnosis='').count()
        context['patients_without_final_diagnosis'] = patients_without_final_diagnosis

        # d) Total number of patients with initial_diagnosis as "positive"
        patients_with_positive_initial_diagnosis = CervicData.objects.filter(initial_diagnosis='positive').count()
        context['patients_with_positive_initial_diagnosis'] = patients_with_positive_initial_diagnosis

        return context






@method_decorator(login_required, name='dispatch')
class PendingListView(ListView):
    model = CervicData
    template_name = 'dashboard/pending.html'
    context_object_name = 'cervic_data'

    def get_queryset(self):
        # Filter the queryset to include entries where final_diagnosis_by is empty
        return CervicData.objects.filter(final_diagnosis_by='')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # a) Total number of patients
        total_patients = CervicData.objects.count()
        context['total_patients'] = total_patients

        # b) Total number of patients with final diagnosis data
        patients_with_final_diagnosis = CervicData.objects.exclude(final_diagnosis='').count()
        context['patients_with_final_diagnosis'] = patients_with_final_diagnosis

        # c) Total number of patients without final diagnosis data
        patients_without_final_diagnosis = CervicData.objects.filter(final_diagnosis='').count()
        context['patients_without_final_diagnosis'] = patients_without_final_diagnosis

        # d) Total number of patients with initial_diagnosis as "positive"
        patients_with_positive_initial_diagnosis = CervicData.objects.filter(initial_diagnosis='positive').count()
        context['patients_with_positive_initial_diagnosis'] = patients_with_positive_initial_diagnosis

        return context

@method_decorator(login_required, name='dispatch')
class CervicDataDetailView(DetailView):
    model = CervicData
    template_name = 'dashboard/detail.html'
    context_object_name = 'cervic_data'
    def get_context_data(self, *args, **kwargs):
        # Access the 'pk' parameter from self.kwargs
        context = super(CervicDataDetailView, self).get_context_data(*args, **kwargs)
        return context









def home(request):
    return render(request, 'home/index.html')






@method_decorator(login_required, name='dispatch')
class AnalyticsView(TemplateView):
    template_name = 'dashboard/analysis.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Query the CervicData model to count positive cases in different age ranges
        age_ranges = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71+']
        age_conditions = [
            When(Q(age__isnull=True) | Q(age__lt=0), then=0),  # Handle None and negative age values
            When(age__range=(0, 10), then=1),
            When(age__range=(11, 20), then=2),
            When(age__range=(21, 30), then=3),
            When(age__range=(31, 40), then=4),
            When(age__range=(41, 50), then=5),
            When(age__range=(51, 60), then=6),
            When(age__range=(61, 70), then=7),
            When(age__gte=71, then=8),
        ]
        age_annotation = Case(*age_conditions, output_field=IntegerField())

        positive_age_data = (
            CervicData.objects
            .annotate(age_group=age_annotation)
            .values('age_group')
            .annotate(total_positives=Count('id', filter=Q(initial_diagnosis='positive')))
            .order_by('age_group')
        )

        # Create data for the bar chart
        age_groups = [age_ranges[data['age_group'] - 1] for data in positive_age_data]
        total_positives = [data['total_positives'] for data in positive_age_data]

        # Create the bar chart
        bar_chart_fig = plt.figure(figsize=(10, 6))
        plt.bar(age_groups, total_positives)
        plt.xlabel('Age Range')
        plt.ylabel('Total Positives')
        plt.title('Total Positives by Age Range')
        plt.xticks(rotation=45)

        # Query the CervicData model for data to create the area chart
        data_for_area_chart = (
            CervicData.objects
            .values('date_submitted')
            .annotate(total_positives=Count('id', filter=Q(initial_diagnosis='positive')))
            .order_by('date_submitted')
        )

        # Create data for the area chart
        date_submitted = [data['date_submitted'] for data in data_for_area_chart]
        total_positives_area = [data['total_positives'] for data in data_for_area_chart]

        # Create the area chart
        area_chart_fig = plt.figure(figsize=(10, 6))
        plt.fill_between(date_submitted, total_positives_area, alpha=0.5)
        plt.xlabel('Date Submitted')
        plt.ylabel('Total Positives')
        plt.title('Total Positives Over Time')

        # Save the chart images as base64 and pass them to the template
        chart_images = []
        for chart_fig in [bar_chart_fig, area_chart_fig]:
            buffer = BytesIO()
            plt.figure(chart_fig)
            plt.savefig(buffer, format='png')
            chart_image = buffer.getvalue()
            buffer.close()
            chart_images.append(base64.b64encode(chart_image).decode())
        # a) Total number of patients
        total_patients = CervicData.objects.count()
        context['total_patients'] = total_patients

        # b) Total number of patients with final diagnosis data
        patients_with_final_diagnosis = CervicData.objects.exclude(final_diagnosis='').count()
        context['patients_with_final_diagnosis'] = patients_with_final_diagnosis

        # c) Total number of patients without final diagnosis data
        patients_without_final_diagnosis = CervicData.objects.filter(final_diagnosis='').count()
        context['patients_without_final_diagnosis'] = patients_without_final_diagnosis

        # d) Total number of patients with initial_diagnosis as "positive"
        patients_with_positive_initial_diagnosis = CervicData.objects.filter(initial_diagnosis='positive').count()
        context['patients_with_positive_initial_diagnosis'] = patients_with_positive_initial_diagnosis
        
        context['bar_chart_image'] = chart_images[0]
        context['area_chart_image'] = chart_images[1]

        return context



   
class CervicDataFilterView(View):
    template_name = 'dashboard/report.html'
    form_class = FacilityFilterForm  # Replace with your actual form class

    def get(self, request):
        cervic_data = CervicData.objects.all()
        selected_state = None
        selected_facility = None
        form = self.form_class()

        context = {
            'cervic_data': cervic_data,
            'form': form,
            'selected_state': selected_state,
            'selected_facility': selected_facility,
            'is_filtered': False,  # Flag to indicate whether filtering is applied
        }

        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            selected_state = form.cleaned_data.get('state')
            selected_facility = form.cleaned_data.get('facility')

            cervic_data = CervicData.objects.all()

            if selected_facility != 'All Facilities':
                cervic_data = cervic_data.filter(facility=selected_facility)

            # Count total patients in the selected state
            total_patients_in_state = cervic_data.filter(state=selected_state).count()

            # Count total patients sorted by age ranges
            age_ranges = [
                (0, 19),
                (20, 29),
                (30, 39),
                (40, 49),
                (50, 59),
                (60, 100)  # You can adjust the age ranges as needed
            ]

            age_counts = []
            for age_range in age_ranges:
                min_age, max_age = age_range
                age_count = cervic_data.filter(age__gte=min_age, age__lte=max_age).count()
                age_counts.append((f"{min_age}-{max_age}", age_count))

        else:
            cervic_data = CervicData.objects.all()
            total_patients_in_state = None
            age_counts = []

        context = {
            'cervic_data': cervic_data,
            'form': form,
            'selected_state': selected_state,
            'selected_facility': selected_facility,
            'total_patients_in_state': total_patients_in_state,
            'age_counts': age_counts,
        }

        return render(request, self.template_name, context)
   

class GetFacilitiesView(View):
    def get(self, request):
        state_id = request.GET.get('state_id')
        facilities = CervicData.objects.filter(state=state_id).values_list('facility', flat=True).distinct()
        facilities_dict = {facility: facility for facility in facilities}
        return JsonResponse({'facilities': facilities_dict})