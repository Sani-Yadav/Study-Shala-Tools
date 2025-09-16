from django.shortcuts import render
from django.views.generic import ListView
from django.http import JsonResponse
from django.db.models import Count
from .models import Hospital, EmergencyContact

def health_home(request):
    hospitals = Hospital.objects.all()
    contacts = EmergencyContact.objects.all()
    return render(request, 'health_assist/health_home.html', {'hospitals': hospitals, 'contacts': contacts})

class HospitalListView(ListView):
    model = Hospital
    template_name = 'health_assist/hospital_list.html'
    context_object_name = 'hospitals'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Hospital.objects.all().order_by('name')
        
        # Get filter parameters
        state = self.request.GET.get('state')
        district = self.request.GET.get('district')
        search = self.request.GET.get('search')
        
        # Apply filters
        if state:
            queryset = queryset.filter(state__iexact=state)
        if district:
            queryset = queryset.filter(district__iexact=district)
        if search:
            queryset = queryset.filter(name__icontains=search)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Sample data for states and districts
        sample_states_districts = {
            'उत्तर प्रदेश': ['लखनऊ', 'कानपुर', 'वाराणसी', 'आगरा', 'मेरठ'],
            'बिहार': ['पटना', 'गया', 'भागलपुर', 'मुजफ्फरपुर', 'दरभंगा'],
            'महाराष्ट्र': ['मुंबई', 'पुणे', 'नागपुर', 'नासिक', 'औरंगाबाद'],
            'राजस्थान': ['जयपुर', 'जोधपुर', 'उदयपुर', 'कोटा', 'अजमेर'],
            'पंजाब': ['अमृतसर', 'लुधियाना', 'जालंधर', 'पटियाला', 'बठिंडा']
        }
        
        # Get states from database or use sample data
        states = list(Hospital.objects.values_list('state', flat=True).distinct().order_by('state'))
        if not states:
            states = list(sample_states_districts.keys())
        
        # Get districts based on selected state or use sample data
        selected_state = self.request.GET.get('state', '')
        if selected_state and selected_state in sample_states_districts:
            districts = sample_states_districts[selected_state]
        else:
            districts = list(Hospital.objects.filter(
                state=selected_state
            ).values_list('district', flat=True).distinct().order_by('district'))
            if not districts and selected_state in sample_states_districts:
                districts = sample_states_districts[selected_state]
        
        context['states'] = states
        context['districts'] = districts
        context['current_state'] = selected_state
        context['current_district'] = self.request.GET.get('district', '')
        context['current_search'] = self.request.GET.get('search', '')
        context['sample_states_districts'] = sample_states_districts
        return context

def get_districts(request):
    """API endpoint to get districts for a given state"""
    state = request.GET.get('state')
    
    if not state:
        return JsonResponse({'error': 'State parameter is required'}, status=400)
    
    # Sample data for states and districts
    sample_states_districts = {
        'उत्तर प्रदेश': ['लखनऊ', 'कानपुर', 'वाराणसी', 'आगरा', 'मेरठ'],
        'बिहार': ['पटना', 'गया', 'भागलपुर', 'मुजफ्फरपुर', 'दरभंगा'],
        'महाराष्ट्र': ['मुंबई', 'पुणे', 'नागपुर', 'नासिक', 'औरंगाबाद'],
        'राजस्थान': ['जयपुर', 'जोधपुर', 'उदयपुर', 'कोटा', 'अजमेर'],
        'पंजाब': ['अमृतसर', 'लुधियाना', 'जालंधर', 'पटियाला', 'बठिंडा']
    }
    
    # Check if state exists in sample data
    if state in sample_states_districts:
        return JsonResponse({
            'districts': sample_states_districts[state]
        })
    
    # If not in sample data, try to get from database
    try:
        districts = Hospital.objects.filter(
            state=state
        ).values_list('district', flat=True).distinct().order_by('district')
        
        return JsonResponse({
            'districts': list(districts)
        })
    except Exception as e:
        return JsonResponse({
            'error': 'Error fetching districts',
            'details': str(e)
        }, status=500)