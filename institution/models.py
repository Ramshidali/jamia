import datetime
from pyexpat import model
from django.db import models

from main.models import BaseModel

from versatileimagefield.fields import VersatileImageField

# Create your models here.

class Institution(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = VersatileImageField('Image', upload_to="institution/institution")

    class Meta:
        db_table = 'institution'
        verbose_name = ('Institution')
        verbose_name_plural = ('Institution')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.name)


class InstitutionAbout(BaseModel):
    institution = models.ForeignKey(Institution,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = VersatileImageField('Image', upload_to="institution/about")

    class Meta:
        db_table = 'institution_about'
        verbose_name = ('Institution About')
        verbose_name_plural = ('Institution About')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.pk)


class InstitutionGallery(BaseModel):
    institution = models.ForeignKey(Institution,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    image = VersatileImageField('Image', upload_to="institution/gallery")

    class Meta:
        db_table = 'institution_Gallery'
        verbose_name = ('Institution Gallery')
        verbose_name_plural = ('Institution Gallery')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.id)


class InstitutionEvents(BaseModel):
    institution = models.ForeignKey(Institution,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    time = models.TimeField()
    date = models.DateField()
    description = models.TextField()
    image = VersatileImageField('Image', upload_to="institution/events")


    class Meta:
        db_table = 'institution_events'
        verbose_name = ('Institution Events')
        verbose_name_plural = ('Institution Events')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.title)

    def event_status(self):
        now = datetime.datetime.now()
        event = InstitutionEvents.objects.get(pk=self.pk,is_deleted=False)
        # print(now)
        # print(event)
        if now.date() < event.date :
            status = "upcomming"
        elif now.date() > event.date :
            status = "completed"
        elif now.date() == event.date :
            if now.time() > event.time :
                status = "completed"
            else :
                status = "today"
        return status


class InstitutionTestimonial(BaseModel):
    institution = models.ForeignKey(Institution,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        db_table = 'institution_testimonial'
        verbose_name = ('Institution Testimonial')
        verbose_name_plural = ('Institution Testimonial')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.title)


class InstitutionManagementTeam(BaseModel):
    institution = models.ForeignKey(Institution,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    image = VersatileImageField('Image', upload_to="institution/management_team")

    class Meta:
        db_table = 'institution_management_team'
        verbose_name = ('Institution Management Team')
        verbose_name_plural = ('Institution Management Team')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.name)


class InstitutionFacilities(BaseModel):
    institution = models.ForeignKey(Institution,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    image = VersatileImageField('Image', upload_to="institution/facilities")

    class Meta:
        db_table = 'institution_facilities'
        verbose_name = ('Institution Facilities')
        verbose_name_plural = ('Institution Facilities')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.title)


class Department(BaseModel):
    institution = models.ForeignKey(Institution,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    department_name = models.CharField(max_length=200)

    class Meta:
        db_table = 'institution_department'
        verbose_name = ('Institution Department')
        verbose_name_plural = ('Institution Department')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.department_name)


class Faculty(BaseModel):
    department = models.ForeignKey(Department,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    image = VersatileImageField('Image', upload_to="institution/faculty")

    class Meta:
        db_table = 'institution_faculty'
        verbose_name = ('Institution Faculty')
        verbose_name_plural = ('Institution Faculty')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.name)


class Service(BaseModel):
    department = models.ForeignKey(Department,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = VersatileImageField('Image', upload_to="institution/service")

    class Meta:
        db_table = 'institution_service'
        verbose_name = ('Institution Service')
        verbose_name_plural = ('Institution Service')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.name)


class InstitutionContact(BaseModel):
    institution = models.ForeignKey(Institution,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    address = models.TextField()
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    location = models.CharField(max_length=200)
    location_url = models.URLField(null=True,blank=True)
    facebook = models.URLField(null=True,blank=True)
    instagram = models.URLField(null=True,blank=True)
    linkedin = models.URLField(null=True,blank=True)
    twitter = models.URLField(null=True,blank=True)
    whatsapp = models.URLField(null=True,blank=True)

    class Meta:
        db_table = 'institution_contact'
        verbose_name = ('Institution Contact')
        verbose_name_plural = ('Institution Contact')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.institution.name)