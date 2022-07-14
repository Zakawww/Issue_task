from django.views import View
from django.shortcuts import render, get_object_or_404, redirect

from webapp.forms import IssueForm
from webapp.models import Issue


class FormView(View):
    form_class = None
    template_name = None
    redirect_url = ""

    def get_redirect_url(self):
        return redirect(self.redirect_url)

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = self.get_context_data(form=form)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        return kwargs

    def form_valid(self, form):
        # return self.get_redirect_url()
        return redirect(self.get_redirect_url())

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return render(self.request, self.template_name, context)

