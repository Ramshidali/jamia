from django import forms
from django.forms.widgets import TextInput,Textarea,Select,EmailInput,URLInput,FileInput

from web.models import Careers, Gallery, ManagementTeam, Mission, News, Spotlight, Testimonial, Vision, Contact

class SpotlightForm(forms.ModelForm):

    class Meta:
        model = Spotlight
        fields = ['title','image']

        widgets = {
            'title': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Title'}),
            'image': FileInput(attrs={'class': 'form-control dropify'}),
        }

    def clean_image(self):

        image_file = self.cleaned_data.get('image')
        if not (image_file.name.endswith(".jpg") or image_file.name.endswith(".jpeg") or image_file.name.endswith(".png")):
            raise forms.ValidationError("Only .jpg or .jpeg or .png files are accepted")
        return image_file

class NewsForm(forms.ModelForm):

    class Meta:
        model = News
        fields = ['title','description']

        widgets = {
            'title': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Title'}),
        }

class GalleryForm(forms.ModelForm):

    class Meta:
        model = Gallery
        fields = ['image']

        widgets = {
            'image': FileInput(attrs={'class': 'form-control dropify'}),
        }

    def clean_image(self):

        image_file = self.cleaned_data.get('image')
        if not (image_file.name.endswith(".jpg") or image_file.name.endswith(".jpeg") or image_file.name.endswith(".png")):
            raise forms.ValidationError("Only .jpg or .jpeg or .png files are accepted")
        return image_file


class TestimonialForm(forms.ModelForm):

    class Meta:
        model = Testimonial
        fields = ['title','designation','description']

        widgets = {
            'title': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Title'}),
            'designation': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Designation'}),
            'description': Textarea(attrs={'class': 'required form-control text-area','placeholder' : 'Enter Description'}),
        }


class VisionForm(forms.ModelForm):

    class Meta:
        model = Vision
        fields = ['image','description']

        widgets = {
            'image': FileInput(attrs={'class': 'form-control dropify'}),
            'description': Textarea(attrs={'class': 'required form-control text-area','placeholder' : 'Enter Description'}),
        }

    def clean_image(self):

        image_file = self.cleaned_data.get('image')
        if not (image_file.name.endswith(".jpg") or image_file.name.endswith(".jpeg") or image_file.name.endswith(".png")):
            raise forms.ValidationError("Only .jpg or .jpeg or .png files are accepted")
        return image_file


class MissionForm(forms.ModelForm):

    class Meta:
        model = Mission
        fields = ['image','description']

        widgets = {
            'image': FileInput(attrs={'class': 'form-control dropify'}),
            'description': Textarea(attrs={'class': 'required form-control text-area','placeholder' : 'Enter Description'}),
        }

    def clean_image(self):

        image_file = self.cleaned_data.get('image')
        if not (image_file.name.endswith(".jpg") or image_file.name.endswith(".jpeg") or image_file.name.endswith(".png")):
            raise forms.ValidationError("Only .jpg or .jpeg or .png files are accepted")
        return image_file


class ManagementTeamForm(forms.ModelForm):

    class Meta:
        model = ManagementTeam
        fields = ['name','designation','image','description']

        widgets = {
            'name': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Name'}),
            'designation': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Designation'}),
            'description': Textarea(attrs={'class': 'required form-control text-area','placeholder' : 'Enter Description'}),
            'image': FileInput(attrs={'class': 'form-control dropify'}),
        }

    def clean_image(self):

        image_file = self.cleaned_data.get('image')
        if not (image_file.name.endswith(".jpg") or image_file.name.endswith(".jpeg") or image_file.name.endswith(".png")):
            raise forms.ValidationError("Only .jpg or .jpeg or .png files are accepted")
        return image_file


class CareersForm(forms.ModelForm):

    class Meta:
        model = Careers
        fields = ['designation_name','description','status']

        widgets = {
            'designation_name': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Designation Name'}),
            'description': Textarea(attrs={'class': 'required form-control text-area','placeholder' : 'Enter Description'}),
            'status': Select(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Status'}),
        }


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['phone','email','location','location_url','address','facebook','instagram','linkedin','twitter','whatsapp']

        widgets = {
            'phone': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Phone'}),
            'email': EmailInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Email'}),
            'location': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Location'}),
            'location_url': URLInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Location URL'}),
            'facebook': URLInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Facebook URL'}),
            'instagram': URLInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Instagram URL'}),
            'linkedin': URLInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Linkedin URL'}),
            'twitter': URLInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Twitter URL'}),
            'whatsapp': URLInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Whatsapp URL'}),
            'description': Textarea(attrs={'class': 'required form-control text-area','placeholder' : 'Enter Description'}),
        }