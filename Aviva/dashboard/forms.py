from django import forms
from .models import CervicData
from .models import AllUsers

class UserFilterForm(forms.Form):
    usercategory = forms.ChoiceField(choices=[], required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate choices dynamically from the database
        usercategories = AllUsers.objects.values_list('usercategory', flat=True).distinct()
        self.fields['usercategory'].choices = [('', 'All')] + [(category, category) for category in usercategories]


        
class FacilityFilterForm(forms.Form):
    state = forms.ChoiceField(
        choices=[('All States', 'All States')] + [(state, state) for state in CervicData.objects.values_list('state', flat=True).distinct()],
        required=False
    )
    facility = forms.ChoiceField(
        choices=[('All Facilities', 'All Facilities')],
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(FacilityFilterForm, self).__init__(*args, **kwargs)
        if 'state' in self.data:
            state = self.data.get('state')
            if state != 'All States':
                facilities = CervicData.objects.filter(state=state).values_list('facility', flat=True).distinct()
                self.fields['facility'].choices = [('All Facilities', 'All Facilities')] + [(facility, facility) for facility in facilities]
