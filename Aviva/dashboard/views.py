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
from PIL import Image
from io import BytesIO
from django.db.models import Count
from django.db.models import Q 
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.urls import reverse
from base64 import b64encode

from django.views import View
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.core.exceptions import SuspiciousOperation




#view to lead to landing page
def home(request):
    return render(request, 'home/index.html')


#view in charge of login logic 
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
                request.session['fullname'] = user.fullname  # Store the user's name in the session
                return redirect('dashboard')
            else:
                return HttpResponse('error')

        except AllUsers.DoesNotExist:
            pass  # User not found
    return render(request, 'registration/login.html')

#view in charge of logout
def logout(request):
    if 'userid' in request.session:
        session_key = request.session.session_key
        request.session.flush()  # Clear the session data
        Session.objects.filter(session_key=session_key).delete()  # Delete the session from the database
    return redirect('login')  # Redirect to the login page after logout



#view in charge of first dashboard page
@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'dashboard2/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Check if the values are already stored in the session
        stored_values = self.request.session.get('dashboard_values', None)

        if stored_values is None:
            # a) Total number of patients
            total_patients = CervicData.objects.count()

            # b) Total number of patients with final diagnosis data
            patients_with_final_diagnosis = CervicData.objects.exclude(final_diagnosis='').count()

            # c) Total number of patients without final diagnosis data
            patients_without_final_diagnosis = CervicData.objects.filter(final_diagnosis='').count()

            # d) Total number of patients with initial_diagnosis as "positive"
            patients_with_positive_initial_diagnosis = CervicData.objects.filter(initial_diagnosis='positive').count()

            # Save the values in the session for future use
            self.request.session['dashboard_values'] = {
                'total_patients': total_patients,
                'patients_with_final_diagnosis': patients_with_final_diagnosis,
                'patients_without_final_diagnosis': patients_without_final_diagnosis,
                'patients_with_positive_initial_diagnosis': patients_with_positive_initial_diagnosis,
            }

        else:
            # Retrieve the values from the session
            total_patients = stored_values['total_patients']
            patients_with_final_diagnosis = stored_values['patients_with_final_diagnosis']
            patients_without_final_diagnosis = stored_values['patients_without_final_diagnosis']
            patients_with_positive_initial_diagnosis = stored_values['patients_with_positive_initial_diagnosis']

        fullname = self.request.session.get('fullname', '')

        context['fullname'] = fullname
        context['total_patients'] = total_patients
        context['patients_with_final_diagnosis'] = patients_with_final_diagnosis
        context['patients_without_final_diagnosis'] = patients_without_final_diagnosis
        context['patients_with_positive_initial_diagnosis'] = patients_with_positive_initial_diagnosis

        return context


#view in charge of reviewed page
@method_decorator(login_required, name='dispatch')
class ReviewedListView(ListView):
    model = CervicData
    template_name = 'dashboard2/reviewed.html'
    context_object_name = 'cervic_data'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Check if the values are already stored in the session
        stored_values = self.request.session.get('dashboard_values', None)

        if stored_values is None:
            # a) Total number of patients
            total_patients = CervicData.objects.count()

            # b) Total number of patients with final diagnosis data
            patients_with_final_diagnosis = CervicData.objects.exclude(final_diagnosis='').count()

            # c) Total number of patients without final diagnosis data
            patients_without_final_diagnosis = CervicData.objects.filter(final_diagnosis='').count()

            # d) Total number of patients with initial_diagnosis as "positive"
            patients_with_positive_initial_diagnosis = CervicData.objects.filter(initial_diagnosis='positive').count()

            # Save the values in the session for future use
            self.request.session['dashboard_values'] = {
                'total_patients': total_patients,
                'patients_with_final_diagnosis': patients_with_final_diagnosis,
                'patients_without_final_diagnosis': patients_without_final_diagnosis,
                'patients_with_positive_initial_diagnosis': patients_with_positive_initial_diagnosis,
            }

        else:
            # Retrieve the values from the session
            total_patients = stored_values['total_patients']
            patients_with_final_diagnosis = stored_values['patients_with_final_diagnosis']
            patients_without_final_diagnosis = stored_values['patients_without_final_diagnosis']
            patients_with_positive_initial_diagnosis = stored_values['patients_with_positive_initial_diagnosis']

        fullname = self.request.session.get('fullname', '')

        context['fullname'] = fullname
        context['total_patients'] = total_patients
        context['patients_with_final_diagnosis'] = patients_with_final_diagnosis
        context['patients_without_final_diagnosis'] = patients_without_final_diagnosis
        context['patients_with_positive_initial_diagnosis'] = patients_with_positive_initial_diagnosis

        return context

    def get_queryset(self):
        # Filter the queryset to exclude entries where final_diagnosis_by is empty
        return CervicData.objects.exclude(final_diagnosis_by__exact='')

    def render_to_response(self, context, **response_kwargs):
        # Call the parent render_to_response method
        response = super().render_to_response(context, **response_kwargs)

        # Optionally, you can add more logic here before returning the response
        # For example, you may want to update the session values again based on some conditions

        return response


#view in charge of pending page
@method_decorator(login_required, name='dispatch')
class PendingListView(ListView):
    model = CervicData
    template_name = 'dashboard2/pending.html'
    context_object_name = 'cervic_data'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Check if the values are already stored in the session
        stored_values = self.request.session.get('dashboard_values', None)

        if stored_values is None:
            # a) Total number of patients
            total_patients = CervicData.objects.count()

            # b) Total number of patients with final diagnosis data
            patients_with_final_diagnosis = CervicData.objects.exclude(final_diagnosis='').count()

            # c) Total number of patients without final diagnosis data
            patients_without_final_diagnosis = CervicData.objects.filter(final_diagnosis='').count()

            # d) Total number of patients with initial_diagnosis as "positive"
            patients_with_positive_initial_diagnosis = CervicData.objects.filter(initial_diagnosis='positive').count()

            # Save the values in the session for future use
            self.request.session['dashboard_values'] = {
                'total_patients': total_patients,
                'patients_with_final_diagnosis': patients_with_final_diagnosis,
                'patients_without_final_diagnosis': patients_without_final_diagnosis,
                'patients_with_positive_initial_diagnosis': patients_with_positive_initial_diagnosis,
            }

        else:
            # Retrieve the values from the session
            total_patients = stored_values['total_patients']
            patients_with_final_diagnosis = stored_values['patients_with_final_diagnosis']
            patients_without_final_diagnosis = stored_values['patients_without_final_diagnosis']
            patients_with_positive_initial_diagnosis = stored_values['patients_with_positive_initial_diagnosis']

        fullname = self.request.session.get('fullname', '')

        context['fullname'] = fullname
        context['total_patients'] = total_patients
        context['patients_with_final_diagnosis'] = patients_with_final_diagnosis
        context['patients_without_final_diagnosis'] = patients_without_final_diagnosis
        context['patients_with_positive_initial_diagnosis'] = patients_with_positive_initial_diagnosis

        return context

    def get_queryset(self):
        # Filter the queryset to include entries where final_diagnosis_by is empty
        return CervicData.objects.filter(final_diagnosis_by='')

    def render_to_response(self, context, **response_kwargs):
        # Call the parent render_to_response method
        response = super().render_to_response(context, **response_kwargs)

        # Optionally, you can add more logic here before returning the response
        # For example, you may want to update the session values again based on some conditions

        return response
    

#view in charge of image detail page
@method_decorator(login_required, name='dispatch')
class CervicDataDetailView(DetailView):
    model = CervicData
    template_name = 'dashboard/detail.html'
    context_object_name = 'cervic_data'

    def get_context_data(self, *args, **kwargs):
        context = super(CervicDataDetailView, self).get_context_data(*args, **kwargs)
        fullname = self.request.session.get('fullname', '')
        context['fullname'] = fullname

        # Retrieve the CervicData instance
        cervic_data = self.get_object()

        # Convert base64-encoded strings to image objects
        image = self.decode_base64_to_image(cervic_data.image_base64)
        acetic_acid_image = self.decode_base64_to_image(cervic_data.aceticacid_base64)
        lugols_image = self.decode_base64_to_image(cervic_data.lugolsiodine_base64)

        context['image'] = image
        context['acetic_acid_image'] = acetic_acid_image
        context['lugols_image'] = lugols_image

        return context

    def decode_base64_to_image(self, base64_string):
        if base64_string:
            # Ensure the base64 string is in bytes
            if isinstance(base64_string, str):
                # Add padding if it's missing
                padding = '=' * (4 - len(base64_string) % 4)
                base64_string += padding

                # Remove any characters that are not part of the base64 alphabet
                base64_string = ''.join(c for c in base64_string if c.isalnum() or c in '+/')

                # Convert to bytes
                base64_data = base64_string.encode('utf-8')
            else:
                base64_data = base64_string

            try:
                # Decode the base64 string to bytes
                image_data = base64.b64decode(base64_data)
                # Create an Image object from the bytes
                image = Image.open(BytesIO(image_data))
                return image
            except Exception as e:
                print(f"Error decoding base64: {e}")
                return None
        return None
    
    
#view in charge of analytics page
@method_decorator(login_required, name='dispatch')
class AnalyticsView(TemplateView):
    template_name = 'dashboard2/analysis.html'

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
        

        # Query the CervicData model for data to create the pie chart
        final_diagnosis_data = CervicData.objects.values('final_diagnosis').annotate(count=Count('id'))
        fullname = self.request.session.get('fullname', '')

        

        # Create data for the pie chart
        labels = [data['final_diagnosis'] for data in final_diagnosis_data]
        count = [data['count'] for data in final_diagnosis_data]

        # Create the pie chart
        pie_chart_fig = plt.figure(figsize=(6, 6))
        plt.pie(count, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title('Distribution of Final Diagnoses')

        # Save the pie chart image as base64 and pass it to the template
        buffer = BytesIO()
        plt.figure(pie_chart_fig)
        plt.savefig(buffer, format='png')
        pie_chart_image = buffer.getvalue()
        buffer.close()
        pie_chart_image_base64 = base64.b64encode(pie_chart_image).decode()
        
        context['fullname'] = fullname
        context['final_diagnosis_data'] = final_diagnosis_data
        context['pie_chart_image'] = pie_chart_image_base64
        context['patients_with_positive_initial_diagnosis'] = patients_with_positive_initial_diagnosis
        
        context['bar_chart_image'] = chart_images[0]
        context['area_chart_image'] = chart_images[1]

        return context


#view in charge of report page
@method_decorator(login_required, name='dispatch')   
class CervicDataFilterView(View):
    template_name = 'dashboard2/report.html'
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

        context.update(self.get_context_data())  # Add the additional context data

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

        context.update(self.get_context_data())  # Add the additional context data

        return render(request, self.template_name, context)

    def get_context_data(self):
        context = {
            # a) Total number of patients
            'total_patients': CervicData.objects.count(),

            # b) Total number of patients with final diagnosis data
            'patients_with_final_diagnosis': CervicData.objects.exclude(final_diagnosis='').count(),

            # c) Total number of patients without final diagnosis data
            'patients_without_final_diagnosis': CervicData.objects.filter(final_diagnosis='').count(),

            # d) Total number of patients with initial_diagnosis as "positive"
            'patients_with_positive_initial_diagnosis': CervicData.objects.filter(initial_diagnosis='positive').count(),
        }

        return context


class GetFacilitiesView(View):
    def get(self, request):
        state_id = request.GET.get('state_id')
        facilities = CervicData.objects.filter(state=state_id).values_list('facility', flat=True).distinct()
        facilities_dict = {facility: facility for facility in facilities}
        return JsonResponse({'facilities': facilities_dict})











def display_images(request):
    cervic_data_list = CervicData.objects.all()

    if cervic_data_list:
        images_list = []

        for cervic_data in cervic_data_list:
            image1_base64 = b64encode(cervic_data.image_base64).decode('utf-8') if cervic_data.image_base64 else None
            aceticacid_base64 = b64encode(cervic_data.aceticacid_base64).decode('utf-8') if cervic_data.aceticacid_base64 else None
            lugolsiodine_base64 = b64encode(cervic_data.lugolsiodine_base64).decode('utf-8') if cervic_data.lugolsiodine_base64 else None

            images_list.append({
                'image1_base64': image1_base64,
                'aceticacid_base64': aceticacid_base64,
                'lugolsiodine_base64': lugolsiodine_base64,
            })

        context = {
            'images_list': images_list,
        }

        return render(request, 'test.html', context)
    else:
        return HttpResponse("No data found in the database.")
