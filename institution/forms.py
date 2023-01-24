from django import forms
from django.forms.widgets import TextInput,Textarea,Select,DateInput,CheckboxInput,FileInput

from institution.models import Department, Faculty, Institution, InstitutionAbout, InstitutionContact, InstitutionEvents, InstitutionFacilities, InstitutionGallery, InstitutionManagementTeam, InstitutionTestimonial, Service


class InstitutionForm(forms.ModelForm):

    class Meta:
        model = Institution
        fields = ['name','image','description']

        widgets = {
            'name': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Name'}),
            'description': Textarea(attrs={'class': 'required form-control text-area','rows':'2','placeholder' : 'Enter Description'}),
            'image': FileInput(attrs={'class': 'form-control dropify'}),
        }

    def clean_image(self):

        image_file = self.cleaned_data.get('image')
        if not (image_file.name.endswith(".jpg") or image_file.name.endswith(".jpeg") or image_file.name.endswith(".png")):
            raise forms.ValidationError("Only .jpg or .jpeg or .png files are accepted")
        return image_file


class InstitutionAboutForm(forms.ModelForm):

    class Meta:
        model = InstitutionAbout
        fields = ['title','image','description']

        widgets = {
            'title': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Title'}),
            'description': Textarea(attrs={'class': 'required form-control text-area','rows':'2','placeholder' : 'Enter Description'}),
            'image': FileInput(attrs={'class': 'form-control dropify'}),
        }

    def clean_image(self):

        image_file = self.cleaned_data.get('image')
        if not (image_file.name.endswith(".jpg") or image_file.name.endswith(".jpeg") or image_file.name.endswith(".png")):
            raise forms.ValidationError("Only .jpg or .jpeg or .png files are accepted")
        return image_file


class InstitutionFacilityForm(forms.ModelForm):

    class Meta:
        model = InstitutionFacilities
        fields = ['title','image','designation']

        widgets = {
            'title': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Title'}),
            'designation': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Designation'}),
            'image': FileInput(attrs={'class': 'form-control dropify'}),
        }

    def clean_image(self):

        image_file = self.cleaned_data.get('image')
        if not (image_file.name.endswith(".jpg") or image_file.name.endswith(".jpeg") or image_file.name.endswith(".png")):
            raise forms.ValidationError("Only .jpg or .jpeg or .png files are accepted")
        return image_file


class InstitutionDepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = ['department_name']

        widgets = {
            'department_name': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Department Name'}),
        }


class InstitutionTestimonialForm(forms.ModelForm):

    class Meta:
        model = InstitutionTestimonial
        fields = ['title','designation','description']

        widgets = {
            'title': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Title'}),
            'designation': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Designation'}),
            'description': Textarea(attrs={'class': 'required form-control text-area','rows':'2','placeholder' : 'Enter Description'}),
        }


class InstitutionContactForm(forms.ModelForm):

    class Meta:
        model = InstitutionContact
        fields = ['phone','email','location','location_url','facebook','instagram','linkedin','twitter','whatsapp','address']

        widgets = {
            'phone': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Phone'}),
            'email': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Email'}),
            'location': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Location'}),
            'location_url': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Location URL'}),
            'facebook': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Facebook'}),
            'instagram': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Instagram'}),
            'linkedin': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter LinkedIn'}),
            'twitter': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Twitter'}),
            'whatsapp': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Whatsapp'}),
            'address': Textarea(attrs={'class': 'required form-control text-area','rows':'2','placeholder' : 'Enter Address'}),
        }


class InstitutionGalleryForm(forms.ModelForm):

    class Meta:
        model = InstitutionGallery
        fields = ['image']

        widgets = {
            'image': FileInput(attrs={'class': 'form-control dropify'}),
        }

    def clean_image(self):

        image_file = self.cleaned_data.get('image')
        if not (image_file.name.endswith(".jpg") or image_file.name.endswith(".jpeg") or image_file.name.endswith(".png")):
            raise forms.ValidationError("Only .jpg or .jpeg or .png files are accepted")
        return image_file


class InstitutionEventForm(forms.ModelForm):

    class Meta:
        model = InstitutionEvents
        fields = ['title','time','date','image','description']

        widgets = {
            'title': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Title'}),
            'time': TextInput(attrs={'class': 'required form-control h-20', 'type':'time', 'value':'13:45:00','id':'example-time-input','placeholder' : 'Enter Time'}),
            'date': TextInput(attrs={'class': 'required form-control h-20','type':'date', 'value':'2011-08-19', 'id':'example-date-input','placeholder' : 'Enter Date'}),
            'description': Textarea(attrs={'class': 'required form-control text-area','rows':'2','placeholder' : 'Enter Description'}),
            'image': FileInput(attrs={'class': 'form-control dropify'}),
        }

    def clean_image(self):

        image_file = self.cleaned_data.get('image')
        if not (image_file.name.endswith(".jpg") or image_file.name.endswith(".jpeg") or image_file.name.endswith(".png")):
            raise forms.ValidationError("Only .jpg or .jpeg or .png files are accepted")
        return image_file


class EventForm(forms.ModelForm):

    class Meta:
        model = InstitutionEvents
        fields = ['institution','title','time','date','image','description']

        widgets = {
            'institution': Select(attrs={'class': 'required form-control h-20'}),
            'title': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Title'}),
            'time': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Time'}),
            'date': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Date'}),
            'description': Textarea(attrs={'class': 'required form-control text-area','rows':'2','placeholder' : 'Enter Description'}),
            'image': FileInput(attrs={'class': 'form-control dropify'}),
        }

    def clean_image(self):

        image_file = self.cleaned_data.get('image')
        if not (image_file.name.endswith(".jpg") or image_file.name.endswith(".jpeg") or image_file.name.endswith(".png")):
            raise forms.ValidationError("Only .jpg or .jpeg or .png files are accepted")
        return image_file


class InstitutionManagementTeamForm(forms.ModelForm):

    class Meta:
        model = InstitutionManagementTeam
        fields = ['name','designation','image']

        widgets = {
            'name': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Title'}),
            'designation': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Designation'}),
            'image': FileInput(attrs={'class': 'form-control dropify'}),
        }

    def clean_image(self):

        image_file = self.cleaned_data.get('image')
        if not (image_file.name.endswith(".jpg") or image_file.name.endswith(".jpeg") or image_file.name.endswith(".png")):
            raise forms.ValidationError("Only .jpg or .jpeg or .png files are accepted")
        return image_file


class DepartmentFacultyForm(forms.ModelForm):

    class Meta:
        model = Faculty
        fields = ['name','designation','image']

        widgets = {
            'name': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Title'}),
            'designation': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Designation'}),
            'image': FileInput(attrs={'class': 'form-control dropify'}),
        }

    def clean_image(self):

        image_file = self.cleaned_data.get('image')
        if not (image_file.name.endswith(".jpg") or image_file.name.endswith(".jpeg") or image_file.name.endswith(".png")):
            raise forms.ValidationError("Only .jpg or .jpeg or .png files are accepted")
        return image_file


class DepartmentServicesForm(forms.ModelForm):

    class Meta:
        model = Service
        fields = ['name','description','image']

        widgets = {
            'name': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Name'}),
            'description': Textarea(attrs={'class': 'required form-control text-area','rows':'2','placeholder' : 'Enter Description'}),
            'image': FileInput(attrs={'class': 'form-control dropify'}),
        }

    def clean_image(self):

        image_file = self.cleaned_data.get('image')
        if not (image_file.name.endswith(".jpg") or image_file.name.endswith(".jpeg") or image_file.name.endswith(".png")):
            raise forms.ValidationError("Only .jpg or .jpeg or .png files are accepted")
        return image_file