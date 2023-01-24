from random import choices
from django.db import models

from main.models import BaseModel

from versatileimagefield.fields import VersatileImageField
from ckeditor.fields import RichTextField

# Create your models here.

CAREER_STATUS_CHOICES = (
    ('full_time', 'Full Time'),
    ('part_time', 'Part Time'),
)

class Spotlight(BaseModel):
    title = models.CharField(max_length=200)
    image = VersatileImageField('Image', upload_to="web/spotlight")

    class Meta:
        db_table = 'web_spotlight'
        verbose_name = ('Spotlight')
        verbose_name_plural = ('Spotlight')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.title)


class News(BaseModel):
    title = models.CharField(max_length=200)
    description = RichTextField()

    class Meta:
        db_table = 'web_news'
        verbose_name = ('News')
        verbose_name_plural = ('News')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.title)


class Gallery(BaseModel):
    image = VersatileImageField('Image', upload_to="web/gallery")

    class Meta:
        db_table = 'web_Gallery'
        verbose_name = ('Web Gallery')
        verbose_name_plural = ('Web Gallery')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.id)


class Testimonial(BaseModel):
    title = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        db_table = 'web_testimonial'
        verbose_name = ('Testimonial')
        verbose_name_plural = ('Testimonial')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.title)


class Vision(BaseModel):
    image = VersatileImageField('Image', upload_to="web/vision")
    description = models.TextField()

    class Meta:
        db_table = 'web_vision'
        verbose_name = ('Vision')
        verbose_name_plural = ('Vision')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.id)


class Mission(BaseModel):
    image = VersatileImageField('Image', upload_to="web/vision")
    description = models.TextField()

    class Meta:
        db_table = 'web_mission'
        verbose_name = ('Mission')
        verbose_name_plural = ('Mission')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.id)


class ManagementTeam(BaseModel):
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    description = models.TextField()
    image = VersatileImageField('Image', upload_to="web/management_team")

    class Meta:
        db_table = 'web_management_team'
        verbose_name = ('Management Team')
        verbose_name_plural = ('Management Team')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.id)


class Careers(BaseModel):
    designation_name = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=10,choices=CAREER_STATUS_CHOICES)

    class Meta:
        db_table = 'web_careers'
        verbose_name = ('Web Careers')
        verbose_name_plural = ('Web Careers')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.designation_name)


class AppliedCareers(BaseModel):
    career = models.ForeignKey(Careers,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    cv = models.FileField()
    date_of_submission = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'web_applied_careers'
        verbose_name = ('Web Applied Careers')
        verbose_name_plural = ('Web Applied Careers')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.name)


class Contact(BaseModel):
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
        db_table = 'web_contact'
        verbose_name = ('Web Contact')
        verbose_name_plural = ('Web Contact')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.id)


class Enquiry(BaseModel):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    description = models.TextField()
    date_of_enquiry = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'web_enquiry'
        verbose_name = ('Web Enquiry')
        verbose_name_plural = ('Web Enquiry')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.name)