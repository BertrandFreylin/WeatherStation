# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import TemplateView


def page_not_found_view(request, exception):
    return redirect(reverse('home'))


class HomeView(TemplateView):
    template_name = 'home.html'

    def dispatch(self, request, *args, **kwargs):
        return super(HomeView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        return context
