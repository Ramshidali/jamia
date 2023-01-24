import json
import datetime

from django.db.models import Q
from django.urls import reverse
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from main.decorators import role_required
from main.functions import generate_form_errors, get_auto_id
from web.forms import CareersForm, GalleryForm, ManagementTeamForm, MissionForm, NewsForm, SpotlightForm, TestimonialForm, VisionForm, ContactForm
from web.models import AppliedCareers, Careers, Gallery, ManagementTeam, Mission, News, Spotlight, Testimonial, Vision, Contact, Enquiry
# Create your views here.

@login_required
@role_required(['superadmin'])
def spotlight_view(request):
    """
    spotlight listings
    :param request:
    :return: spotlight list view
    """
    instances = Spotlight.objects.filter(is_deleted=False).order_by("-id")

    filter_data = {}
    query = request.GET.get("q")

    if query:

        instances = instances.filter(
            Q(auto_id__icontains=query) |
            Q(name__icontains=query)
        )
        title = "Spotlight - %s" % query
        filter_data['q'] = query


    context = {
        'instances': instances,
        'page_name' : 'Spotlights',
        'page_title' : 'Spotlights',
        'filter_data' :filter_data,
    }

    return render(request, 'admin_panel/spotlight/spotlight_list.html', context)


@login_required
@role_required(['superadmin'])
def create_spotlight_view(request):
    """
    create operation of spotlight
    :param request:
    :param pk:
    :return:
    """
    if request.method == 'POST':
        # if instance go to edit
        form = SpotlightForm(request.POST,request.FILES)

        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(Spotlight)
            data.creator = request.user
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Spotlight created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('web:spotlight')
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

        form = SpotlightForm()

        context = {
            'form': form,
            'page_name' : 'Create Spotlight',
            'page_title' : 'Create Spotlight',
            'url' : reverse('web:create_spotlight'),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def edit_spotlight_view(request,pk):
    """
    edit operation of spotlight
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(Spotlight, pk=pk)

    message = ''
    if request.method == 'POST':
        form = SpotlightForm(request.POST,request.FILES,instance=instance)

        if form.is_valid():

            #update product
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "Spotlight Update successfully.",
                'redirect': 'true',
                "redirect_url": reverse('web:spotlight')
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

        form = SpotlightForm(instance=instance)

        context = {
            'form': form,
            'instance': instance,
            'page_name' : 'Update Spotlight',
            'page_title' : 'Update Spotlight',
            'is_need_select2' : True,
            'url' : reverse('web:spotlight'),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def delete_spotlight_view(request, pk):
    """
    spotlight deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    Spotlight.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Spotlight Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('web:spotlight')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@role_required(['superadmin'])
def news_view(request,pk):
    """
    news single page
    :param request:
    :return: news view
    """
    instance = News.objects.get(pk=pk, is_deleted=False)

    context = {
        'instance': instance,
        'page_name' : 'News',
        'page_title' : 'News',
    }

    return render(request, 'admin_panel/news/news.html', context)


@login_required
@role_required(['superadmin'])
def news_list_view(request):
    """
    news listings
    :param request:
    :return: news list view
    """
    instances = News.objects.filter(is_deleted=False).order_by("-date_added")

    filter_data = {}
    query = request.GET.get("q")

    if query:

        instances = instances.filter(
            Q(auto_id__icontains=query) |
            Q(name__icontains=query) |
            Q(category__name__icontains=query)
        )
        title = "News - %s" % query
        filter_data['q'] = query


    context = {
        'instances': instances,
        'page_name' : 'News',
        'page_title' : 'News',
        'filter_data' : filter_data
    }

    return render(request, 'admin_panel/news/news_list.html', context)


@login_required
@role_required(['superadmin'])
def create_news_view(request):
    """
    create operation of news
    :param request:
    :return:
    """
    # check pk for getting instance
    message = ''
    if request.method == 'POST':
        form = NewsForm(request.POST,files=request.FILES)

        if form.is_valid():

            #create product
            data = form.save(commit=False)
            data.auto_id = get_auto_id(News)
            data.creator = request.user
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "news created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('news:news_list')
            }

        else:
            message = generate_form_errors(form, formset=False)

            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        form = NewsForm()

        context = {
            'form': form,
            'page_name' : 'Create News',
            'page_title' : 'Create News',
            'is_rich_text' : True,
            'is_need_select2' : True,
            'is_need_datetime_picker' : True,
            'url' : reverse('news:create_news'),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def edit_news_view(request,pk):
    """
    edit operation of News
    :param request:
    :param pk:
    :return:
    """
    news_instance = get_object_or_404(News, pk=pk)

    message = ''

    if request.method == 'POST':
        form = NewsForm(request.POST,files=request.FILES,instance=news_instance)

        if form.is_valid() :

            #create product
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
            "status": "true",
            "title": "Successfully Updated",
            "message": "news Updated Successfully.",
            'redirect': 'true',
            "redirect_url": reverse('news:news_list'),
            "return" : True,
            }

        else:
            message = generate_form_errors(form, formset=False)

            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        form = NewsForm(instance=news_instance)

        context = {
            'form': form,
            'instance': news_instance,
            'message': message,
            'pro_instance': news_instance,
            'page_name' : 'Edit News',
            'is_rich_text' : True,
        }

        return render(request, 'admin_panel/create/create.html', context)


@login_required
@role_required(['superadmin'])
def delete_news_view(request, pk):
    """
    news deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    News.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "news Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('news:news_list')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@role_required(['superadmin'])
def gallery(request,pk):
    """
    gallery single page
    :param request:
    :return: gallery view
    """
    instance = Gallery.objects.get(pk=pk, is_deleted=False)

    context = {
        'instance': instance,
        'page_name' : 'gallery',
        'page_title' : 'gallery',
    }

    return render(request, 'admin_panel/web/gallery.html', context)


@login_required
@role_required(['superadmin'])
def gallery_list(request):
    """
    gallery listings
    :param request:
    :return: gallery list view
    """
    instances = Gallery.objects.filter(is_deleted=False).order_by("-date_added")

    filter_data = {}
    query = request.GET.get("q")

    if query:

        instances = instances.filter(
            Q(auto_id__icontains=query) |
            Q(name__icontains=query) |
            Q(category__name__icontains=query)
        )
        title = "gallery - %s" % query
        filter_data['q'] = query


    context = {
        'instances': instances,
        'page_name' : 'gallery',
        'page_title' : 'gallery',
        'filter_data' : filter_data
    }

    return render(request, 'admin_panel/web/gallery_list.html', context)


@login_required
@role_required(['superadmin'])
def create_gallery(request):
    """
    create operation of gallery
    :param request:
    :return:
    """
    # check pk for getting instance
    message = ''
    if request.method == 'POST':
        form = GalleryForm(request.POST,files=request.FILES)

        if form.is_valid():

            #create product
            data = form.save(commit=False)
            data.auto_id = get_auto_id(Gallery)
            data.creator = request.user
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "gallery created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('web:gallery_list')
            }

        else:
            message = generate_form_errors(form, formset=False)

            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        form = GalleryForm()

        context = {
            'form': form,
            'page_name' : 'Create gallery',
            'page_title' : 'Create gallery',
            'is_rich_text' : True,
            'is_need_select2' : True,
            'is_need_datetime_picker' : True,
            'url' : reverse('web:create_gallery'),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def edit_gallery(request,pk):
    """
    edit operation of gallery
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(Gallery, pk=pk)

    message = ''

    if request.method == 'POST':
        form = GalleryForm(request.POST,files=request.FILES,instance=instance)

        if form.is_valid() :

            #create product
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
            "status": "true",
            "title": "Successfully Updated",
            "message": "gallery Updated Successfully.",
            'redirect': 'true',
            "redirect_url": reverse('web:gallery_list'),
            "return" : True,
            }

        else:
            message = generate_form_errors(form, formset=False)

            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        form = GalleryForm(instance=instance)

        context = {
            'form': form,
            'instance': instance,
            'message': message,
            'pro_instance': instance,
            'page_name' : 'Edit gallery',
            'is_rich_text' : True,
        }

        return render(request, 'admin_panel/create/create.html', context)


@login_required
@role_required(['superadmin'])
def delete_gallery(request, pk):
    """
    gallery deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    Gallery.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Gallery Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('web:gallery_list')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@role_required(['superadmin'])
def testimonial(request,pk):
    """
    testimonial single page
    :param request:
    :return: testimonial view
    """
    instance = Testimonial.objects.get(pk=pk, is_deleted=False)

    context = {
        'instance': instance,
        'page_name' : 'Testimonial',
        'page_title' : 'Testimonial',
    }

    return render(request, 'admin_panel/web/testimonial.html', context)


@login_required
@role_required(['superadmin'])
def testimonial_list(request):
    """
    testimonial listings
    :param request:
    :return: testimonial list view
    """
    instances = Testimonial.objects.filter(is_deleted=False).order_by("-date_added")

    filter_data = {}
    query = request.GET.get("q")

    if query:

        instances = instances.filter(
            Q(auto_id__icontains=query) |
            Q(name__icontains=query) |
            Q(category__name__icontains=query)
        )
        title = "testimonial - %s" % query
        filter_data['q'] = query


    context = {
        'instances': instances,
        'page_name' : 'Testimonial',
        'page_title' : 'Testimonial',
        'filter_data' : filter_data
    }

    return render(request, 'admin_panel/web/testimonial_list.html', context)


@login_required
@role_required(['superadmin'])
def create_testimonial(request):
    """
    create operation of testimonial
    :param request:
    :return:
    """
    # check pk for getting instance
    message = ''
    if request.method == 'POST':
        form = TestimonialForm(request.POST,files=request.FILES)

        if form.is_valid():

            data = form.save(commit=False)
            data.auto_id = get_auto_id(Testimonial)
            data.creator = request.user
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "testimonial created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('web:testimonial_list')
            }

        else:
            message = generate_form_errors(form, formset=False)

            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        form = TestimonialForm()

        context = {
            'form': form,
            'page_name' : 'Create Testimonial',
            'page_title' : 'Create Testimonial',
            'is_rich_text' : True,
            'is_need_select2' : True,
            'is_need_datetime_picker' : True,
            'url' : reverse('web:create_testimonial'),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def edit_testimonial(request,pk):
    """
    edit operation of testimonial
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(Testimonial, pk=pk)

    message = ''

    if request.method == 'POST':
        form = TestimonialForm(request.POST,files=request.FILES,instance=instance)

        if form.is_valid() :

            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
            "status": "true",
            "title": "Successfully Updated",
            "message": "testimonial Updated Successfully.",
            'redirect': 'true',
            "redirect_url": reverse('web:testimonial_list'),
            "return" : True,
            }

        else:
            message = generate_form_errors(form, formset=False)

            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        form = TestimonialForm(instance=instance)

        context = {
            'form': form,
            'instance': instance,
            'message': message,
            'pro_instance': instance,
            'page_name' : 'Edit Testimonial',
            'is_rich_text' : True,
        }

        return render(request, 'admin_panel/create/create.html', context)


@login_required
@role_required(['superadmin'])
def delete_testimonial(request, pk):
    """
    testimonial deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    Testimonial.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "testimonial Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('web:testimonial_list')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@role_required(['superadmin'])
def vision_list(request):
    """
    vision listings
    :param request:
    :return: vision list view
    """
    instances = Vision.objects.filter(is_deleted=False).order_by("-date_added")

    filter_data = {}
    query = request.GET.get("q")

    if query:

        instances = instances.filter(
            Q(auto_id__icontains=query) |
            Q(name__icontains=query) |
            Q(category__name__icontains=query)
        )
        title = "Vision - %s" % query
        filter_data['q'] = query


    context = {
        'instances': instances,
        'page_name' : 'Vision',
        'page_title' : 'Vision',
        'filter_data' : filter_data
    }

    return render(request, 'admin_panel/web/vision_list.html', context)


@login_required
@role_required(['superadmin'])
def create_vision(request):
    """
    create operation of vision
    :param request:
    :return:
    """
    # check pk for getting instance
    message = ''
    if request.method == 'POST':
        form = VisionForm(request.POST,files=request.FILES)

        if form.is_valid():

            #create product
            data = form.save(commit=False)
            data.auto_id = get_auto_id(Vision)
            data.creator = request.user
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Vision created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('web:vision_list')
            }

        else:
            message = generate_form_errors(form, formset=False)

            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        form = VisionForm()

        context = {
            'form': form,
            'page_name' : 'Create Vision',
            'page_title' : 'Create Vision',
            'is_rich_text' : True,
            'is_need_select2' : True,
            'is_need_datetime_picker' : True,
            'url' : reverse('web:create_vision'),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def edit_vision(request,pk):
    """
    edit operation of vision
    :param request:
    :param pk:
    :return:
    """
    vision_instance = get_object_or_404(Vision, pk=pk)

    message = ''

    if request.method == 'POST':
        form = VisionForm(request.POST,files=request.FILES,instance=vision_instance)

        if form.is_valid() :

            #create product
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
            "status": "true",
            "title": "Successfully Updated",
            "message": "Vision Updated Successfully.",
            'redirect': 'true',
            "redirect_url": reverse('web:vision_list'),
            "return" : True,
            }

        else:
            message = generate_form_errors(form, formset=False)

            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        form = VisionForm(instance=vision_instance)

        context = {
            'form': form,
            'instance': vision_instance,
            'message': message,
            'pro_instance': vision_instance,
            'page_name' : 'Edit Vision',
            'is_rich_text' : True,
        }

        return render(request, 'admin_panel/create/create.html', context)


@login_required
@role_required(['superadmin'])
def delete_vision(request, pk):
    """
    web deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    Vision.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Vision Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('web:vision_list')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@role_required(['superadmin'])
def mission_list(request):
    """
    mission listings
    :param request:
    :return: mission list view
    """
    instances = Mission.objects.filter(is_deleted=False).order_by("-date_added")

    filter_data = {}
    query = request.GET.get("q")

    if query:

        instances = instances.filter(
            Q(auto_id__icontains=query) |
            Q(name__icontains=query) |
            Q(category__name__icontains=query)
        )
        title = "Mission - %s" % query
        filter_data['q'] = query


    context = {
        'instances': instances,
        'page_name' : 'Mission',
        'page_title' : 'Mission',
        'filter_data' : filter_data
    }

    return render(request, 'admin_panel/web/mission_list.html', context)


@login_required
@role_required(['superadmin'])
def create_mission(request):
    """
    create operation of mission
    :param request:
    :return:
    """
    # check pk for getting instance
    message = ''
    if request.method == 'POST':
        form = MissionForm(request.POST,files=request.FILES)

        if form.is_valid():

            data = form.save(commit=False)
            data.auto_id = get_auto_id(Mission)
            data.creator = request.user
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Mission created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('web:mission_list')
            }

        else:
            message = generate_form_errors(form, formset=False)

            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        form = MissionForm()

        context = {
            'form': form,
            'page_name' : 'Create Mission',
            'page_title' : 'Create Mission',
            'is_rich_text' : True,
            'is_need_select2' : True,
            'is_need_datetime_picker' : True,
            'url' : reverse('web:create_mission'),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def edit_mission(request,pk):
    """
    edit operation of mission
    :param request:
    :param pk:
    :return:
    """
    mission_instance = get_object_or_404(Mission, pk=pk)

    message = ''

    if request.method == 'POST':
        form = MissionForm(request.POST,files=request.FILES,instance=mission_instance)

        if form.is_valid() :

            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
            "status": "true",
            "title": "Successfully Updated",
            "message": "Mission Updated Successfully.",
            'redirect': 'true',
            "redirect_url": reverse('web:mission_list'),
            "return" : True,
            }

        else:
            message = generate_form_errors(form, formset=False)

            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        form = MissionForm(instance=mission_instance)

        context = {
            'form': form,
            'instance': mission_instance,
            'message': message,
            'pro_instance': mission_instance,
            'page_name' : 'Edit Mission',
            'is_rich_text' : True,
        }

        return render(request, 'admin_panel/create/create.html', context)


@login_required
@role_required(['superadmin'])
def delete_mission(request, pk):
    """
    mission deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    Mission.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Mission Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('web:mission_list')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@role_required(['superadmin'])
def management_team(request,pk):
    """
    management_team single page
    :param request:
    :return: management_team view
    """
    try:
        instance = ManagementTeam.objects.get(pk=pk, is_deleted=False)
        context = {
            'instance': instance,
            'page_name' : 'Management Team',
            'page_title' : 'Management Team',
            }
        return render(request, 'admin_panel/web/management_team/management_team.html', context)
    except:
        return redirect(reverse('web:management_team_list'))


@login_required
@role_required(['superadmin'])
def management_team_list(request):
    """
    management_team listings
    :param request:
    :return: management_team list view
    """
    instances = ManagementTeam.objects.filter(is_deleted=False).order_by("-date_added")

    filter_data = {}
    query = request.GET.get("q")

    if query:

        instances = instances.filter(
            Q(auto_id__icontains=query) |
            Q(name__icontains=query) |
            Q(category__name__icontains=query)
        )
        title = "ManagementTeam - %s" % query
        filter_data['q'] = query


    context = {
        'instances': instances,
        'page_name' : 'Management Team',
        'page_title' : 'Management Team',
        'filter_data' : filter_data
    }

    return render(request, 'admin_panel/web/management_team/management_team_list.html', context)


@login_required
@role_required(['superadmin'])
def create_management_team(request):
    """
    create operation of management_team
    :param request:
    :return:
    """
    # check pk for getting instance
    message = ''
    if request.method == 'POST':
        form = ManagementTeamForm(request.POST,files=request.FILES)

        if form.is_valid():

            data = form.save(commit=False)
            data.auto_id = get_auto_id(ManagementTeam)
            data.creator = request.user
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "ManagementTeam created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('web:management_team_list')
            }

        else:
            message = generate_form_errors(form, formset=False)

            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        form = ManagementTeamForm()

        context = {
            'form': form,
            'page_name' : 'Create Management Team',
            'page_title' : 'Create Management Team',
            'is_rich_text' : True,
            'is_need_select2' : True,
            'is_need_datetime_picker' : True,
            'url' : reverse('web:create_management_team'),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def edit_management_team(request,pk):
    """
    edit operation of management_team
    :param request:
    :param pk:
    :return:
    """
    management_team_instance = get_object_or_404(ManagementTeam, pk=pk)

    message = ''

    if request.method == 'POST':
        form = ManagementTeamForm(request.POST,files=request.FILES,instance=management_team_instance)

        if form.is_valid() :

            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
            "status": "true",
            "title": "Successfully Updated",
            "message": "Management Team Updated Successfully.",
            'redirect': 'true',
            "redirect_url": reverse('web:management_team_list'),
            "return" : True,
            }

        else:
            message = generate_form_errors(form, formset=False)

            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        form = ManagementTeamForm(instance=management_team_instance)

        context = {
            'form': form,
            'instance': management_team_instance,
            'message': message,
            'pro_instance': management_team_instance,
            'page_name' : 'Edit Management Team',
            'is_rich_text' : True,
        }

        return render(request, 'admin_panel/create/create.html', context)


@login_required
@role_required(['superadmin'])
def delete_management_team(request, pk):
    """
    management_team deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    ManagementTeam.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Management Team Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('web:management_team_list')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@role_required(['superadmin'])
def careers_view(request):
    """
    careers listings
    :param request:
    :return: careers list view
    """
    instances = Careers.objects.filter(is_deleted=False).order_by("-id")

    filter_data = {}
    query = request.GET.get("q")

    if query:

        instances = instances.filter(
            Q(auto_id__icontains=query) |
            Q(name__icontains=query)
        )
        title = "Careers - %s" % query
        filter_data['q'] = query


    context = {
        'instances': instances,
        'page_name' : 'Careers',
        'page_title' : 'Careers',
        'filter_data' :filter_data,
    }

    return render(request, 'admin_panel/web/careers_list.html', context)


@login_required
@role_required(['superadmin'])
def create_careers_view(request):
    """
    create operation of careers
    :param request:
    :param pk:
    :return:
    """
    if request.method == 'POST':
        # if instance go to edit
        form = CareersForm(request.POST,request.FILES)

        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(Careers)
            data.creator = request.user
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Careers created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('web:careers_list')
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

        form = CareersForm()

        context = {
            'form': form,
            'page_name' : 'Create Careers',
            'page_title' : 'Create Careers',
            'url' : reverse('web:create_careers'),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def edit_careers_view(request,pk):
    """
    edit operation of careers
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(Careers, pk=pk)

    message = ''
    if request.method == 'POST':
        form = CareersForm(request.POST,request.FILES,instance=instance)

        if form.is_valid():

            #update product
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "Careers Update successfully.",
                'redirect': 'true',
                "redirect_url": reverse('web:careers')
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

        form = CareersForm(instance=instance)

        context = {
            'form': form,
            'instance': instance,
            'page_name' : 'Update Careers',
            'page_title' : 'Update Careers',
            'is_need_select2' : True,
            'url' : reverse('web:careers'),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def delete_careers_view(request, pk):
    """
    careers deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    Careers.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Careers Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('web:careers')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@role_required(['superadmin'])
def applied_careers_view(request):
    """
    applied careers listings
    :param request:
    :return: careers list view
    """
    instances = AppliedCareers.objects.filter(is_deleted=False).order_by("-id")

    filter_data = {}
    query = request.GET.get("q")

    if query:

        instances = instances.filter(
            Q(auto_id__icontains=query) |
            Q(name__icontains=query) |
            Q(career__designation_name__icontains=query) |
            Q(career__status__icontains=query)
        )
        title = "Applied Careers - %s" % query
        filter_data['q'] = query


    context = {
        'instances': instances,
        'page_name' : 'Applied Careers',
        'page_title' : 'Applied Careers',
        'filter_data' :filter_data,
    }

    return render(request, 'admin_panel/web/applied_careers_list.html', context)


@login_required
@role_required(['superadmin'])
def contact_view(request):
    """
    contact
    :param request:
    :return: contact view
    """
    instance = Contact.objects.filter(is_deleted=False).order_by("-id").first()

    context = {
        'instance': instance,
        'page_name' : 'Contact',
        'page_title' : 'Contact',
    }

    return render(request, 'admin_panel/web/contact_list.html', context)


@login_required
@role_required(['superadmin'])
def create_contact_view(request):
    """
    create operation of contact
    :param request:
    :param pk:
    :return:
    """
    if request.method == 'POST':
        # if instance go to edit
        form = ContactForm(request.POST,request.FILES)

        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(Contact)
            data.creator = request.user
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Contact created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('web:contact_list')
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

        form = ContactForm()

        context = {
            'form': form,
            'page_name' : 'Create Contact',
            'page_title' : 'Create Contact',
            'url' : reverse('web:create_contact'),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def edit_contact_view(request,pk):
    """
    edit operation of contact
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(Contact, pk=pk)

    message = ''
    if request.method == 'POST':
        form = ContactForm(request.POST,request.FILES,instance=instance)

        if form.is_valid():

            #update product
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "Contact Update successfully.",
                'redirect': 'true',
                "redirect_url": reverse('web:contact_list')
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

        form = ContactForm(instance=instance)

        context = {
            'form': form,
            'instance': instance,
            'page_name' : 'Update Contact',
            'page_title' : 'Update Contact',
            'is_need_select2' : True,
            'url' : reverse('web:edit_contact', kwargs={'pk':pk}),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def delete_contact_view(request, pk):
    """
    contact deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    Contact.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Contact Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('web:contact_list')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@role_required(['superadmin'])
def enquiry_view(request):
    """
    Enquiry
    :param request:
    :return: enquiry view
    """
    instances = Enquiry.objects.filter(is_deleted=False).order_by("-id")

    context = {
        'instances': instances,
        'page_name' : 'Enquiry',
        'page_title' : 'Enquiry',
    }

    return render(request, 'admin_panel/web/enquiry_list.html', context)

@login_required
@role_required(['superadmin'])
def delete_enquiry_view(request, pk):
    """
    enquiry deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    Enquiry.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Enquiy Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('web:enquiry_list')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')