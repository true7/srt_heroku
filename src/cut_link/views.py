from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import View

from .models import CutURL
from .forms import URLForm
from .utils import json_data_func


class HomeView(View):

    def get(self, request, *args, **kwargs):
        form = URLForm()
        context = {'form': form}

        instance = CutURL()
        json_data = json_data_func(instance)
        context['json_data'] = json_data

        return render(request, 'content.html', context=context)

    def post(self, request, *args, **kwargs):
        form = URLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            if not url.startswith('http'):
                url = 'http://' + url
            obj, created = CutURL.objects.get_or_create(url=url)
            context = {
                'form': form,
                'obj': obj,
            }
            if not created:
                context['created'] = '(Already exists in DataBase)'
        else:
            context = {'form': form}

        instance = CutURL()
        json_data = json_data_func(instance)
        context['json_data'] = json_data

        return render(request, 'content.html', context=context)


class URLRedirectView(View):
    
    def get(self, request, shortlink=None, *args, **kwargs):
        obj = get_object_or_404(CutURL, shortlink=shortlink)

        return HttpResponseRedirect(obj.url)
