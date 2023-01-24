from itertools import count
import json
import datetime

from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from django.forms import inlineformset_factory

from main.decorators import role_required
from main.functions import generate_form_errors, get_auto_id
from institution.models import Department, Faculty, Institution, InstitutionAbout,InstitutionContact, InstitutionFacilities, InstitutionGallery, InstitutionManagementTeam, InstitutionTestimonial, Service, InstitutionEvents
from institution.forms import DepartmentFacultyForm, DepartmentServicesForm, EventForm, InstitutionAboutForm, InstitutionContactForm, InstitutionDepartmentForm, InstitutionEventForm, InstitutionFacilityForm, InstitutionForm, InstitutionGalleryForm, InstitutionManagementTeamForm, InstitutionTestimonialForm

# Create your views here.
@login_required
@role_required(['superadmin'])
def institution(request,pk):
    """
    institution single page
    :param request:
    :return: institution view
    """
    # try :
    instance = Institution.objects.get(pk=pk, is_deleted=False)
    fasilities = InstitutionFacilities.objects.filter(institution=instance, is_deleted=False)[:4]
    testimonials = InstitutionTestimonial.objects.filter(institution=instance, is_deleted=False)[:4]
    departments = Department.objects.filter(institution=instance, is_deleted=False)[:4]
    gallery = InstitutionGallery.objects.filter(institution=instance, is_deleted=False)[:4]
    management_team = InstitutionManagementTeam.objects.filter(institution=instance, is_deleted=False)[:6]
    events = InstitutionEvents.objects.filter(institution=instance, is_deleted=False)[:4]
    about = InstitutionAbout.objects.filter(institution=instance, is_deleted=False).first()
    contacts = InstitutionContact.objects.filter(institution=instance, is_deleted=False).first()

    context = {
        'instance': instance,
        'fasilities': fasilities,
        'testimonials': testimonials,
        'departments': departments,
        'management_team': management_team,
        'events': events,
        'gallery': gallery,
        'about': about,
        'contact': contacts,

        'page_name' : 'Institution',
        'page_title' : 'Institution',
        }
    return render(request, 'admin_panel/institution/institution.html', context)
    # except:
    #     return redirect(reverse('institution:institution_list'))


@login_required
@role_required(['superadmin'])
def institution_list(request):
    """
    institution listings
    :param request:
    :return: institution list view
    """
    instances = Institution.objects.filter(is_deleted=False).order_by("-date_added")

    filter_data = {}
    query = request.GET.get("q")

    if query:

        instances = instances.filter(
            Q(auto_id__icontains=query) |
            Q(name__icontains=query) |
            Q(category__name__icontains=query)
        )
        title = "Institution - %s" % query
        filter_data['q'] = query


    context = {
        'instances': instances,
        'page_name' : 'Institution',
        'page_title' : 'Institution',
        'filter_data' : filter_data
    }

    return render(request, 'admin_panel/institution/institution_list.html', context)


@login_required
@role_required(['superadmin'])
def create_institution(request):
    """
    create operation of institution
    :param request:
    :return:
    """
    FasilityFormset = formset_factory(InstitutionFacilityForm, extra=1)
    DepartmentFormset = formset_factory(InstitutionDepartmentForm, extra=1)
    TestimonialFormset = formset_factory(InstitutionTestimonialForm, extra=1)
    ManagementTeamFormset = formset_factory(InstitutionManagementTeamForm, extra=1)

    # check pk for getting instance
    message = ''
    if request.method == 'POST':
        institution_form = InstitutionForm(request.POST,files=request.FILES)
        about_form = InstitutionAboutForm(request.POST,files=request.FILES)
        contact_form = InstitutionContactForm(request.POST,files=request.FILES)

        fasility_formset = FasilityFormset(request.POST,files=request.FILES, prefix='fasility_formset', form_kwargs={'empty_permitted': False})
        department_formset = DepartmentFormset(request.POST,files=request.FILES, prefix='department_formset', form_kwargs={'empty_permitted': False})
        testimonial_formset = TestimonialFormset(request.POST,files=request.FILES, prefix='testimonial_formset', form_kwargs={'empty_permitted': False})
        management_team_formset = ManagementTeamFormset(request.POST,files=request.FILES, prefix='management_team_formset', form_kwargs={'empty_permitted': False})

        if institution_form.is_valid() and about_form.is_valid() and fasility_formset.is_valid() and department_formset.is_valid() and testimonial_formset.is_valid() and management_team_formset.is_valid() :

            data = institution_form.save(commit=False)
            data.auto_id = get_auto_id(Institution)
            data.creator = request.user
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            if fasility_formset.is_valid():
                for form in fasility_formset:

                    fasility_data = form.save(commit=False)
                    fasility_data.auto_id = get_auto_id(InstitutionFacilities)
                    fasility_data.creator = request.user
                    fasility_data.date_updated = datetime.datetime.today()
                    fasility_data.updater = request.user
                    fasility_data.institution = data
                    fasility_data.save()

            if department_formset.is_valid():
                for form in department_formset:

                    department_data = form.save(commit=False)
                    department_data.auto_id = get_auto_id(Department)
                    department_data.creator = request.user
                    department_data.date_updated = datetime.datetime.today()
                    department_data.updater = request.user
                    department_data.institution = data
                    department_data.save()

            if testimonial_formset.is_valid():
                for form in testimonial_formset:

                    testimonial_data = form.save(commit=False)
                    testimonial_data.auto_id = get_auto_id(InstitutionTestimonial)
                    testimonial_data.creator = request.user
                    testimonial_data.date_updated = datetime.datetime.today()
                    testimonial_data.updater = request.user
                    testimonial_data.institution = data
                    testimonial_data.save()

            if management_team_formset.is_valid():
                for form in management_team_formset:

                    management_team_data = form.save(commit=False)
                    management_team_data.auto_id = get_auto_id(InstitutionManagementTeam)
                    management_team_data.creator = request.user
                    management_team_data.date_updated = datetime.datetime.today()
                    management_team_data.updater = request.user
                    management_team_data.institution = data
                    management_team_data.save()

            about_data = about_form.save(commit=False)
            about_data.auto_id = get_auto_id(InstitutionAbout)
            about_data.creator = request.user
            about_data.date_updated = datetime.datetime.today()
            about_data.updater = request.user
            about_data.institution = data
            about_data.save()

            contact_data = contact_form.save(commit=False)
            contact_data.auto_id = get_auto_id(InstitutionContact)
            contact_data.creator = request.user
            contact_data.date_updated = datetime.datetime.today()
            contact_data.updater = request.user
            contact_data.institution = data
            contact_data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Institution created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('institution:institution_list')
            }

        else:
            message = generate_form_errors(institution_form, formset=False)
            message += generate_form_errors(about_form, formset=False)
            message += generate_form_errors(contact_form, formset=False)

            message += generate_form_errors(fasility_formset, formset=True)
            message += generate_form_errors(department_formset, formset=True)
            message += generate_form_errors(testimonial_formset, formset=True)
            message += generate_form_errors(management_team_formset, formset=True)
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        institution_form = InstitutionForm()
        about_form = InstitutionAboutForm()
        contact_form = InstitutionContactForm()

        fasility_formset = FasilityFormset(prefix='fasility_formset')
        department_formset = DepartmentFormset(prefix='department_formset')
        testimonial_formset = TestimonialFormset(prefix='testimonial_formset')
        management_team_formset = ManagementTeamFormset(prefix='management_team_formset')

        context = {
            'institution_form': institution_form,
            'about_form': about_form,
            'contact_form': contact_form,

            'fasility_formset': fasility_formset,
            'department_formset': department_formset,
            'testimonial_formset': testimonial_formset,
            'management_team_formset': management_team_formset,

            'page_name' : 'Create Institution',
            'page_title' : 'Create Institution',
            'is_rich_text' : True,
            'is_need_select2' : True,
            'is_need_datetime_picker' : True,
            'url' : reverse('institution:create_institution'),
        }

        return render(request, 'admin_panel/create/create_institution.html',context)


@login_required
@role_required(['superadmin'])
def edit_institution(request,pk):
    """
    edit operation of institution
    :param request:
    :param pk:
    :return:
    """

    instance = Institution.objects.get(pk=pk, is_deleted=False)
    about = InstitutionAbout.objects.filter(institution=instance, is_deleted=False).first()
    contact = InstitutionContact.objects.filter(institution=instance, is_deleted=False).first()

    fasilities = InstitutionFacilities.objects.filter(institution=instance, is_deleted=False)
    department = Department.objects.filter(institution=instance, is_deleted=False)
    testimonial = InstitutionTestimonial.objects.filter(institution=instance, is_deleted=False)
    management_team = InstitutionManagementTeam.objects.filter(institution=instance, is_deleted=False)

    if fasilities.exists():
        f_extra = 0
    else:
        f_extra = 1

    if department.exists():
        d_extra = 0
    else:
        d_extra = 1

    if testimonial.exists():
        t_extra = 0
    else:
        t_extra = 1

    if management_team.exists():
        m_extra = 0
    else:
        m_extra = 1

    FacilityFormset = inlineformset_factory(
        Institution,
        InstitutionFacilities,
        extra=f_extra,
        form=InstitutionFacilityForm,
    )

    DepartmentFormset = inlineformset_factory(
        Institution,
        Department,
        extra=d_extra,
        form=InstitutionDepartmentForm,
    )
    TestimonialFormset = inlineformset_factory(
        Institution,
        InstitutionTestimonial,
        extra=t_extra,
        form=InstitutionTestimonialForm,
    )

    ManagementTeamFormset = inlineformset_factory(
        Institution,
        InstitutionManagementTeam,
        extra=m_extra,
        form=InstitutionManagementTeamForm,
    )

    message = ''

    if request.method == 'POST':
        institution_form = InstitutionForm(request.POST,files=request.FILES,instance=instance)
        if about :
            about_form = InstitutionAboutForm(request.POST,files=request.FILES,instance=about)
        else :
            about_form = InstitutionAboutForm(request.POST,files=request.FILES)
        if contact :
            contact_form = InstitutionContactForm(request.POST,files=request.FILES,instance=contact)
        else :
            contact_form = InstitutionContactForm(request.POST,files=request.FILES)

        fasility_formset = FacilityFormset(request.POST,request.FILES,instance=instance, prefix='fasility_formset', form_kwargs={'empty_permitted': False},queryset=fasilities)
        department_formset = DepartmentFormset(request.POST,request.FILES,instance=instance, prefix='department_formset', form_kwargs={'empty_permitted': False},queryset=department)
        testimonial_formset = TestimonialFormset(request.POST,request.FILES,instance=instance, prefix='testimonial_formset', form_kwargs={'empty_permitted': False},queryset=testimonial)
        management_team_formset = ManagementTeamFormset(request.POST,request.FILES,instance=instance, prefix='management_team_formset', form_kwargs={'empty_permitted': False},queryset=management_team)

        if institution_form.is_valid() and about_form.is_valid() and contact_form.is_valid() :

            data = institution_form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            about_data = about_form.save(commit=False)
            if not about :
                about_data.auto_id = get_auto_id(InstitutionAbout)
                about_data.creator = request.user
                about_data.institution = data
            about_data.date_updated = datetime.datetime.today()
            about_data.updater = request.user
            about_data.save()

            contact_data = contact_form.save(commit=False)
            if not contact :
                contact_data.auto_id = get_auto_id(InstitutionAbout)
                contact_data.creator = request.user
                contact_data.institution = data
            contact_data.date_updated = datetime.datetime.today()
            contact_data.updater = request.user
            contact_data.save()

            if fasility_formset.is_valid():
                for form in fasility_formset:
                    if form not in fasility_formset.deleted_forms:
                        # print(fasility_formset)
                        f_data = form.save(commit=False)
                        f_data.date_updated = datetime.datetime.today()
                        f_data.updater = request.user
                        if not f_data.auto_id :
                            f_data.auto_id = get_auto_id(InstitutionFacilities)
                            f_data.creator = request.user

                        f_data.save()

                for f in fasility_formset.deleted_forms:
                    f.instance.delete()
            else:
                message = fasility_formset.errors

                response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
                }

            if department_formset.is_valid():
                for form in department_formset:
                    if form not in department_formset.deleted_forms:
                        # print(department_formset)
                        d_data = form.save(commit=False)
                        d_data.date_updated = datetime.datetime.today()
                        d_data.updater = request.user
                        if not d_data.auto_id :
                            d_data.auto_id = get_auto_id(Department)
                            d_data.creator = request.user

                        d_data.save()

                for d in department_formset.deleted_forms:
                    d.instance.delete()
            else:
                message = fasility_formset.errors

                response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
                }

            if testimonial_formset.is_valid():
                for form in testimonial_formset:
                    if form not in testimonial_formset.deleted_forms:
                        # print(testimonial_formset)
                        t_data = form.save(commit=False)
                        t_data.date_updated = datetime.datetime.today()
                        t_data.updater = request.user
                        if not t_data.auto_id :
                            t_data.auto_id = get_auto_id(InstitutionTestimonial)
                            t_data.creator = request.user

                        t_data.save()

                for t in testimonial_formset.deleted_forms:
                    t.instance.delete()
            else:
                message = fasility_formset.errors

                response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
                }

            if management_team_formset.is_valid():
                for form in management_team_formset:
                    if form not in management_team_formset.deleted_forms:
                        # print(management_team_formset)
                        m_data = form.save(commit=False)
                        m_data.date_updated = datetime.datetime.today()
                        m_data.updater = request.user
                        if not m_data.auto_id :
                            m_data.auto_id = get_auto_id(InstitutionManagementTeam)
                            m_data.creator = request.user

                        m_data.save()

                for m in management_team_formset.deleted_forms:
                    m.instance.delete()
            else:
                message = fasility_formset.errors

                response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
                }

            response_data = {
            "status": "true",
            "title": "Successfully Updated",
            "message": "Institution Updated Successfully.",
            'redirect': 'true',
            "redirect_url": reverse('institution:institution_list'),
            "return" : True,
            }

        else:
            # message = generate_form_errors(form, formset=False)

            response_data = {
                "status": "false",
                "title": "Failed",
                "message": "form validation error",
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        institution_form = InstitutionForm(instance=instance)
        about_form = InstitutionAboutForm(instance=about)
        contact_form = InstitutionContactForm(instance=contact)

        fasility_formset = FacilityFormset(prefix='fasility_formset',instance=instance,queryset=fasilities)
        department_formset = DepartmentFormset(prefix='department_formset',instance=instance,queryset=department)
        testimonial_formset = TestimonialFormset(prefix='testimonial_formset',instance=instance,queryset=testimonial)
        management_team_formset = ManagementTeamFormset(prefix='management_team_formset',instance=instance,queryset=management_team)

        context = {
            'institution_form': institution_form,
            'about_form': about_form,
            'contact_form': contact_form,

            'fasility_formset' : fasility_formset,
            'department_formset' : department_formset,
            'testimonial_formset' : testimonial_formset,
            'management_team_formset' : management_team_formset,

            'page_name' : 'Edit Institution',
            'is_rich_text' : True,
        }

        return render(request, 'admin_panel/create/create_institution.html', context)


@login_required
@role_required(['superadmin'])
def delete_institution(request, pk):
    """
    institution deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    instance = Institution.objects.get(pk=pk, is_deleted=False)
    s = instance.is_deleted = True
    s.save()

    InstitutionAbout.objects.filter(institution=instance, is_deleted=False).update(is_deleted=True)
    InstitutionContact.objects.filter(institution=instance, is_deleted=False).update(is_deleted=True)
    InstitutionFacilities.objects.filter(institution=instance, is_deleted=False).update(is_deleted=True)
    Department.objects.filter(institution=instance, is_deleted=False).update(is_deleted=True)
    InstitutionTestimonial.objects.filter(institution=instance, is_deleted=False).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Institution Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('institution:institution_list')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@role_required(['superadmin'])
def institution_facility_single(request,pk):
    """
    institution_facility sigle view
    :param request:
    :return: institution
    """
    instance = InstitutionFacilities.objects.get(pk=pk,is_deleted=False)

    context = {
        'instance': instance,
        'page_name' : 'Institution Facilities',
        'page_title' : 'Institution Facilities',
        'active_page_name' : 'Facility single view',
    }

    return render(request, 'admin_panel/institution/single.html', context)


@login_required
@role_required(['superadmin'])
def institution_facilities(request,institution_pk):
    """
    institution_facilities by institution based
    :param request:
    :return: institution
    """
    instances = InstitutionFacilities.objects.filter(institution__pk=institution_pk,is_deleted=False)

    context = {
        'instances': instances,
        'page_name' : 'Institution Facilities',
        'page_title' : 'Institution Facilities',
        'active_page_name' : 'Facility single view',
    }

    return render(request, 'admin_panel/institution/fasilities_list.html', context)


@login_required
@role_required(['superadmin'])
def create_institution_facility(request,pk):
    """
    create operation of institution_facilitys
    :param request:
    :param pk: institution pk
    :return:
    """
    institution = Institution.objects.get(pk=pk,is_deleted=False)
    if request.method == 'POST':
        # if instance go to edit
        form = InstitutionFacilityForm(request.POST,request.FILES)

        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(InstitutionFacilities)
            data.creator = request.user
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.institution = institution
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "InstitutionFacilities created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('institution:institution', kwargs={'pk':pk})
            }

        else:
            message =generate_form_errors(form , formset=False)
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        form = InstitutionFacilityForm()

        context = {
            'form': form,
            'page_name' : 'Create Institution Facilities',
            'page_title' : 'Create Institution Facilities',
            'url' : reverse('institution:create_institution_facility'),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def edit_institution_facility(request,pk):
    """
    edit operation of institution_facility
    :param request:
    :param pk:
    :return:
    """
    # institution = request.GET.get("institution")

    instance = get_object_or_404(InstitutionFacilities, pk=pk)

    message = ''
    if request.method == 'POST':
        form = InstitutionFacilityForm(request.POST,request.FILES,instance=instance)

        if form.is_valid():

            #update product
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "InstitutionFacilities Update successfully.",
                'redirect': 'true',
                "redirect_url": reverse('institution:institution', kwargs={'pk':instance.institution.pk})
            }

        else:
            message = generate_form_errors(form ,formset=False)


            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        form = InstitutionFacilityForm(instance=instance)

        context = {
            'form': form,
            'page_name' : 'Update Institution Facilities',
            'page_title' : 'Update Institution Facilities',
            'is_need_select2' : True,
            'url' : reverse('institution:institution', kwargs={'pk':instance.institution.pk}),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def delete_institution_facility(request, pk):
    """
    institution_facility deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    instance = InstitutionFacilities.objects.get(pk=pk)
    instance.is_deleted = True
    instance.save()

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Institution Facilities Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('institution:institution', kwargs={'pk':instance.institution.pk})
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@role_required(['superadmin'])
def institution_about_single(request,pk):
    """
    institution_about sigle view
    :param request:
    :return: institution_about single view
    """
    instance = InstitutionAbout.objects.filter(pk=pk,is_deleted=False)

    # if institution :
    #     instance = instance.filter(institution__pk=institution)

    context = {
        'instance': instance,
        'page_name' : 'Our Institution About',
        'page_title' : 'Our Institution About',
        'active_page_name' : 'InstitutionAbout single view',
    }

    return render(request, 'admin_panel/institution/single.html', context)


@login_required
@role_required(['superadmin'])
def create_institution_about(request,pk):
    """
    create operation of institution_abouts
    :param request:
    :param pk: institution pk
    :return:
    """
    institution = Institution.objects.get(pk=pk,is_deleted=False)
    if request.method == 'POST':
        # if instance go to edit
        form = InstitutionAboutForm(request.POST,request.FILES)

        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(InstitutionAbout)
            data.creator = request.user
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.institution = institution
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Institution About created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('institution:institution', kwargs={'pk':pk})
            }

        else:
            message =generate_form_errors(form , formset=False)
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        form = InstitutionAboutForm()

        context = {
            'form': form,
            'page_name' : 'Create Institution About',
            'page_title' : 'Create Institution About',
            'url' : reverse('institution:create_institution_about'),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def edit_institution_about(request,pk):
    """
    edit operation of institution_about
    :param request:
    :param pk:
    :return:
    """
    # institution = request.GET.get("institution")
    instance = get_object_or_404(InstitutionAbout, pk=pk)

    message = ''
    if request.method == 'POST':
        form = InstitutionAboutForm(request.POST,request.FILES,instance=instance)

        if form.is_valid():

            #update product
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "Institution About Update successfully.",
                'redirect': 'true',
                "redirect_url": reverse('institution:institution', kwargs={'pk':instance.institution.pk})
            }

        else:
            message = generate_form_errors(form ,formset=False)


            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        form = InstitutionAboutForm(instance=instance)

        context = {
            'form': form,
            'page_name' : 'Update Institution About',
            'page_title' : 'Update Institution About',
            'is_need_select2' : True,
            'url' : reverse('institution:institution', kwargs={'pk':instance.institution.pk}),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def delete_institution_about(request, pk):
    """
    institution_about deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    instance = InstitutionAbout.objects.get(pk=pk)
    instance.is_deleted = True
    instance.save()

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Institution About Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('institution:institution', kwargs={'pk':instance.institution.pk})
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@role_required(['superadmin'])
def institution_testimonial_single(request,pk):
    """
    institution_testimonial sigle view
    :param request:
    :return: institution_testimonial single view
    """
    instance = InstitutionTestimonial.objects.filter(pk=pk,is_deleted=False)

    # if institution :
    #     instance = instance.filter(institution__pk=institution)

    context = {
        'instance': instance,
        'page_name' : 'Our Institution About',
        'page_title' : 'Our Institution About',
        'active_page_name' : 'InstitutionTestimonial single view',
    }

    return render(request, 'admin_panel/institution/single.html', context)


@login_required
@role_required(['superadmin'])
def institution_testimonials(request,institution_pk):
    """
    institution testimonials list view
    :param request:
    :return: institution_testimonials
    """
    instances = InstitutionTestimonial.objects.filter(institution__pk=institution_pk,is_deleted=False)

    context = {
        'instances': instances,
        'page_name' : 'Testimonials',
        'page_title' : 'Testimonials',
        'active_page_name' : 'Institution Testimonial List',
    }

    return render(request, 'admin_panel/institution/testimonials_list.html', context)


@login_required
@role_required(['superadmin'])
def create_institution_testimonial(request,pk):
    """
    create operation of institution_testimonials
    :param request:
    :param pk: institution pk
    :return:
    """
    institution = Institution.objects.get(pk=pk,is_deleted=False)
    if request.method == 'POST':
        # if instance go to edit
        form = InstitutionTestimonialForm(request.POST,request.FILES)

        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(InstitutionTestimonial)
            data.creator = request.user
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.institution = institution
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Institution About created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('institution:institution', kwargs={'pk':pk})
            }

        else:
            message =generate_form_errors(form , formset=False)
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        form = InstitutionTestimonialForm()

        context = {
            'form': form,
            'page_name' : 'Create Institution About',
            'page_title' : 'Create Institution About',
            'url' : reverse('institution:create_institution_testimonial'),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def edit_institution_testimonial(request,pk):
    """
    edit operation of institution_testimonial
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(InstitutionTestimonial, pk=pk)

    message = ''
    if request.method == 'POST':
        form = InstitutionTestimonialForm(request.POST,request.FILES,instance=instance)

        if form.is_valid():

            #update product
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "Institution About Update successfully.",
                'redirect': 'true',
                "redirect_url": reverse('institution:institution', kwargs={'pk':instance.institution.pk}),
            }

        else:
            message = generate_form_errors(form ,formset=False)


            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        form = InstitutionTestimonialForm(instance=instance)

        context = {
            'form': form,
            'page_name' : 'Edit Testimonial',
            'page_title' : 'Edit Testimonial',
            'is_need_select2' : True,
            'url' : reverse('institution:institution', kwargs={'pk':instance.institution.pk}),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def delete_institution_testimonial(request, pk):
    """
    institution_testimonial deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    # institution = request.GET.get("institution")
    instance = InstitutionTestimonial.objects.get(pk=pk)
    instance.is_deleted = True
    instance.save()

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Institution About Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('institution:institution', kwargs={'pk':instance.institution.pk})
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@role_required(['superadmin'])
def institution_department_single(request,pk):
    """
    institution_department sigle view
    :param request:
    :return: institution_department single view
    """
    instance = Department.objects.get(pk=pk,is_deleted=False)
    faculty = Faculty.objects.filter(department=instance,is_deleted=False)
    service = Service.objects.filter(department=instance,is_deleted=False)

    context = {
        'instance': instance,
        'faculty': faculty,
        'service': service,

        'page_name' : 'Department',
        'page_title' : 'Department',
        'active_page_name' : 'Department single view',
    }

    return render(request, 'admin_panel/institution/department.html', context)


@login_required
@role_required(['superadmin'])
def institution_departments(request,institution_pk):
    """
    institution department list view by institution
    :param request:
    :return: institution_department list view
    """
    instances = Department.objects.filter(institution__pk=institution_pk,is_deleted=False)

    context = {
        'instances': instances,

        'page_name' : 'Department',
        'page_title' : 'Department',
        'active_page_name' : 'Department List view',
    }

    return render(request, 'admin_panel/institution/department_list.html', context)


@login_required
@role_required(['superadmin'])
def create_institution_department(request,pk):
    """
    create operation of institution_departments
    :param request:
    :param pk: institution pk
    :return:
    """
    institution = Institution.objects.get(pk=pk,is_deleted=False)
    if request.method == 'POST':
        # if instance go to edit
        form = InstitutionDepartmentForm(request.POST,request.FILES)

        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(Department)
            data.creator = request.user
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.institution = institution
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Institution Department created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('institution:institution', kwargs={'pk':pk})
            }

        else:
            message =generate_form_errors(form , formset=False)
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        form = InstitutionDepartmentForm()

        context = {
            'form': form,
            'page_name' : 'Create Institution Department',
            'page_title' : 'Create Institution Department',
            'url' : reverse('institution:create_institution_department'),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def edit_institution_department(request,pk):
    """
    edit operation of institution_department
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(Department, pk=pk)

    message = ''
    if request.method == 'POST':
        form = InstitutionDepartmentForm(request.POST,request.FILES,instance=instance)

        if form.is_valid():

            #update product
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "Institution Department Update successfully.",
                'redirect': 'true',
                "redirect_url": reverse('institution:institution', kwargs={'pk':instance.institution.pk}),
            }

        else:
            message = generate_form_errors(form ,formset=False)


            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        form = InstitutionDepartmentForm(instance=instance)

        context = {
            'form': form,
            'page_name' : 'Edit Testimonial',
            'page_title' : 'Edit Testimonial',
            'is_need_select2' : True,
            'url' : reverse('institution:institution', kwargs={'pk':instance.institution.pk}),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def delete_institution_department(request, pk):
    """
    institution_department deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    # institution = request.GET.get("institution")
    instance = Department.objects.get(pk=pk)
    instance.is_deleted = True
    instance.save()

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Institution Department Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('institution:institution', kwargs={'pk':instance.institution.pk})
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@role_required(['superadmin'])
def institution_contact_single(request,pk):
    """
    institution_contact sigle view
    :param request:
    :return: institution_contact single view
    """
    instance = InstitutionContact.objects.filter(pk=pk,is_deleted=False)

    # if institution :
    #     instance = instance.filter(institution__pk=institution)

    context = {
        'instance': instance,
        'page_name' : 'Institution Contact',
        'page_title' : 'Institution Contact',
        'active_page_name' : 'Institution Contact single view',
    }

    return render(request, 'admin_panel/institution/single.html', context)


@login_required
@role_required(['superadmin'])
def create_institution_contact(request,pk):
    """
    create operation of institution_contacts
    :param request:
    :param pk: institution pk
    :return:
    """
    institution = Institution.objects.get(pk=pk,is_deleted=False)
    if request.method == 'POST':
        # if instance go to edit
        form = InstitutionContactForm(request.POST,request.FILES)

        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(InstitutionContact)
            data.creator = request.user
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.institution = institution
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Institution InstitutionContact created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('institution:institution', kwargs={'pk':pk})
            }

        else:
            message =generate_form_errors(form , formset=False)
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        form = InstitutionContactForm()

        context = {
            'form': form,
            'page_name' : 'Create Institution Institution Contact',
            'page_title' : 'Create Institution Institution Contact',
            'url' : reverse('institution:create_institution_contact'),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def edit_institution_contact(request,pk):
    """
    edit operation of institution_contact
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(InstitutionContact, pk=pk)

    message = ''
    if request.method == 'POST':
        form = InstitutionContactForm(request.POST,request.FILES,instance=instance)

        if form.is_valid():

            #update product
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "Institution Institution Contact Update successfully.",
                'redirect': 'true',
                "redirect_url": reverse('institution:institution', kwargs={'pk':instance.institution.pk}),
            }

        else:
            message = generate_form_errors(form ,formset=False)


            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        form = InstitutionContactForm(instance=instance)

        context = {
            'form': form,
            'page_name' : 'Edit Contact',
            'page_title' : 'Edit Contact',
            'is_need_select2' : True,
            'url' : reverse('institution:institution', kwargs={'pk':instance.institution.pk}),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def delete_institution_contact(request, pk):
    """
    institution_contact deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    # institution = request.GET.get("institution")
    instance = InstitutionContact.objects.get(pk=pk)
    instance.is_deleted = True
    instance.save()

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Institution InstitutionContact Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('institution:institution', kwargs={'pk':instance.institution.pk})
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@role_required(['superadmin'])
def institution_gallery_list(request,institution_pk):
    """
    institution gallery list view by institution
    :param request:
    :return: institution gallery list view
    """
    instances = InstitutionGallery.objects.filter(institution__pk=institution_pk,is_deleted=False)

    context = {
        'instances': instances,

        'page_name' : 'Gallery',
        'page_title' : 'Gallery',
        'active_page_name' : 'Gallery List view',
    }

    return render(request, 'admin_panel/institution/galleries_list.html', context)


@login_required
@role_required(['superadmin'])
def create_institution_gallery(request):
    """
    create operation of institution_gallerys
    :param request:
    :param pk: institution pk
    :return:
    """
    institute_pk = request.GET.get('institute')
    if institute_pk :
            institution = Institution.objects.get(pk=institute_pk,is_deleted=False)

    GalleryFormset = formset_factory(InstitutionGalleryForm, extra=1)

    if request.method == 'POST':
        # if instance go to edit
        print(institute_pk)

        if institute_pk :
            gallery_formset = GalleryFormset(request.POST,files=request.FILES, prefix='gallery_formset', form_kwargs={'empty_permitted': False})
        else:
            form = InstitutionGalleryForm(request.POST,request.FILES)

        if gallery_formset.is_valid():
            for form in gallery_formset:
                data = form.save(commit=False)
                data.auto_id = get_auto_id(InstitutionGallery)
                data.creator = request.user
                data.date_updated = datetime.datetime.today()
                data.updater = request.user
                if institute_pk :
                    data.institution = institution
                data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Institution Gallery created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('institution:institution', kwargs={'pk':institute_pk}),
            }

        else:
            message =generate_form_errors(gallery_formset , formset=True)
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        gallery_formset = GalleryFormset(prefix='gallery_formset')

        context = {
            'gallery_formset': gallery_formset,
            'page_name' : 'Create Institution Gallery',
            'page_title' : 'Create Institution Gallery',
            'url' : reverse('institution:create_institution_gallery')+"?institute="+institute_pk,
        }

        return render(request, 'admin_panel/create/create_institution_gallery.html',context)


@login_required
@role_required(['superadmin'])
def delete_institution_gallery(request, pk):
    """
    institution_gallery deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    # institution = request.GET.get("institution")
    instance = InstitutionGallery.objects.get(pk=pk)
    instance.is_deleted = True
    instance.save()

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Institution Gallery Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('institution:institution', kwargs={'pk':instance.institution.pk})
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@role_required(['superadmin'])
def create_institution_management_team(request,pk):
    """
    create operation of institution_management_teams
    :param request:
    :param pk: institution pk
    :return:
    """
    institution = Institution   .objects.get(pk=pk,is_deleted=False)
    if request.method == 'POST':
        # if instance go to edit
        form = InstitutionManagementTeamForm(request.POST,request.FILES)

        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(InstitutionManagementTeam)
            data.creator = request.user
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.institution = institution
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Management Team created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('institution:institution', kwargs={'pk':pk})
            }

        else:
            message =generate_form_errors(form , formset=False)
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        form = InstitutionManagementTeamForm()

        context = {
            'form': form,
            'page_name' : 'Create Management Team',
            'page_title' : 'Create Management Team',
            'url' : reverse('institution:create_institution_management_team', kwargs={'pk':pk}),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def edit_institution_management_team(request,pk):
    """
    edit operation of institution_management_team
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(InstitutionManagementTeam, pk=pk)

    message = ''
    if request.method == 'POST':
        form = InstitutionManagementTeamForm(request.POST,request.FILES,instance=instance)

        if form.is_valid():

            #update product
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "Management Team Update successfully.",
                'redirect': 'true',
                "redirect_url": reverse('institution:institution', kwargs={'pk':instance.institution.pk}),
            }

        else:
            message = generate_form_errors(form ,formset=False)


            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        form = InstitutionManagementTeamForm(instance=instance)

        context = {
            'form': form,
            'page_name' : 'Edit Gallery',
            'page_title' : 'Edit Gallery',
            'is_need_select2' : True,
            'url' : reverse('institution:institution', kwargs={'pk':instance.institution.pk}),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def delete_institution_management_team(request, pk):
    """
    institution_management_team deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    # institution = request.GET.get("institution")
    instance = InstitutionManagementTeam.objects.get(pk=pk)
    instance.is_deleted = True
    instance.save()

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Management Team Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('institution:institution', kwargs={'pk':instance.institution.pk})
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@role_required(['superadmin'])
def create_department_faculty(request,pk):
    """
    create operation of department_facultys
    :param request:
    :param pk: department pk
    :return:
    """
    department = Department.objects.get(pk=pk,is_deleted=False)
    if request.method == 'POST':
        # if instance go to edit
        form = DepartmentFacultyForm(request.POST,request.FILES)

        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(Faculty)
            data.creator = request.user
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.department = department
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Department Faculty created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('institution:institution_department', kwargs={'pk':pk})
            }

        else:
            message =generate_form_errors(form , formset=False)
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        form = DepartmentFacultyForm()

        context = {
            'form': form,
            'page_name' : 'Create Department Faculty',
            'page_title' : 'Create Department Faculty',
            'url' : reverse('institution:create_department_faculty', kwargs={'pk':pk}),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def edit_department_faculty(request,pk):
    """
    edit operation of department_faculty
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(Faculty, pk=pk)

    message = ''
    if request.method == 'POST':
        form = DepartmentFacultyForm(request.POST,request.FILES,instance=instance)

        if form.is_valid():

            #update product
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "Department Faculty Update successfully.",
                'redirect': 'true',
                "redirect_url": reverse('institution:institution_department', kwargs={'pk':instance.department.pk}),
            }

        else:
            message = generate_form_errors(form ,formset=False)


            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        form = DepartmentFacultyForm(instance=instance)

        context = {
            'form': form,
            'page_name' : 'Edit Testimonial',
            'page_title' : 'Edit Testimonial',
            'is_need_select2' : True,
            'url' : reverse('institution:edit_department_faculty', kwargs={'pk':pk}),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def delete_department_faculty(request, pk):
    """
    department faculty deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    instance = Faculty.objects.get(pk=pk)
    instance.is_deleted = True
    instance.save()

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Department Faculty Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('institution:institution_department', kwargs={'pk':instance.department.pk})
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')



@login_required
@role_required(['superadmin'])
def create_department_services(request,pk):
    """
    create operation of department services
    :param request:
    :param pk: department pk
    :return:
    """
    department = Department.objects.get(pk=pk,is_deleted=False)
    if request.method == 'POST':
        # if instance go to edit
        form = DepartmentServicesForm(request.POST,request.FILES)

        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(Service)
            data.creator = request.user
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.department = department
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Department Service created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('institution:institution_department', kwargs={'pk':pk})
            }

        else:
            message =generate_form_errors(form , formset=False)
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        form = DepartmentServicesForm()

        context = {
            'form': form,
            'page_name' : 'Create Department Service',
            'page_title' : 'Create Department Service',
            'url' : reverse('institution:create_department_services', kwargs={'pk':pk}),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def edit_department_services(request,pk):
    """
    edit operation of department_services
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(Service, pk=pk)

    message = ''
    if request.method == 'POST':
        form = DepartmentServicesForm(request.POST,request.FILES,instance=instance)

        if form.is_valid():

            #update product
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "Department Service Update successfully.",
                'redirect': 'true',
                "redirect_url": reverse('institution:institution_department', kwargs={'pk':instance.department.pk}),
            }

        else:
            message = generate_form_errors(form ,formset=False)


            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        form = DepartmentServicesForm(instance=instance)

        context = {
            'form': form,
            'page_name' : 'Edit Testimonial',
            'page_title' : 'Edit Testimonial',
            'is_need_select2' : True,
            'url' : reverse('institution:edit_department_services', kwargs={'pk':pk}),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def delete_department_services(request, pk):
    """
    department faculty deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    instance = Service.objects.get(pk=pk)
    instance.is_deleted = True
    instance.save()

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Department Service Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('institution:institution_department', kwargs={'pk':instance.department.pk})
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@role_required(['superadmin'])
def create_institute_events(request):
    """
    create operation of institute events
    :param request:
    :param pk: event pk
    :return:
    """
    institution = request.GET.get("institution")
    if institution :
        institution = Institution.objects.get(pk=institution,is_deleted=False)

    if request.method == 'POST':
        if institution :
            form = InstitutionEventForm(request.POST,request.FILES)
        else :
            form = EventForm(request.POST,request.FILES)

        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(InstitutionEvents)
            data.creator = request.user
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            if institution :
                data.institution = institution
            data.save()

            print(institution.pk)
            if institution :
                re_url = reverse('institution:institution', kwargs={'pk': institution.pk})
            else :
                re_url = reverse('institution:institution_events_list')
            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Department InstitutionEvents created successfully.",
                'redirect': 'true',
                "redirect_url": re_url,
            }

        else:
            message =generate_form_errors(form , formset=False)
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        if institution :
            form = InstitutionEventForm()
        else :
            form = EventForm()

        context = {
            'form': form,
            'page_name' : 'Create Department InstitutionEvents',
            'page_title' : 'Create Department InstitutionEvents',
            'url' : reverse('institution:create_institute_events')+"?institution="+str(institution.pk),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def edit_institute_events(request,pk):
    """
    edit operation of institute_events
    :param request:
    :param pk:
    :return:
    """
    institution = request.GET.get("institution")

    instance = get_object_or_404(InstitutionEvents, pk=pk)

    message = ''
    if request.method == 'POST':
        if institution :
            form = InstitutionEventForm(request.POST,request.FILES,instance=instance)
        else :
            form = EventForm(request.POST,request.FILES,instance=instance)

        if form.is_valid():
            #update product
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            if institution :
                re_url = reverse('institution:institution', kwargs={'pk': institution})
            else :
                re_url = reverse('institution:institution_events_list')

            response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "Event Updated successfully.",
                'redirect': 'true',
                "redirect_url": re_url,
            }

        else:
            message = generate_form_errors(form ,formset=False)


            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        if institution :
            form = InstitutionEventForm(instance=instance)
        else :
            form = EventForm(instance=instance)

        context = {
            'form': form,
            'page_name' : 'Edit Testimonial',
            'page_title' : 'Edit Testimonial',
            'is_need_select2' : True,
            'url' : reverse('institution:edit_institute_events', kwargs={'pk':pk})+"?institution="+str(institution),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def delete_institute_events(request, pk):
    """
    event deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    institution = request.GET.get("institution")

    instance = InstitutionEvents.objects.get(pk=pk)
    instance.is_deleted = True
    instance.save()

    if institution :
        re_url = reverse('institution:institution', kwargs={'pk': institution.pk})
    else :
        re_url = reverse('institution:institution_events_list')

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Department InstitutionEvents Successfully Deleted.",
        "redirect": "true",
        "redirect_url": re_url,
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


