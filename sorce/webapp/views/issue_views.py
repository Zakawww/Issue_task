from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView, View, FormView, ListView

from webapp.base_view import FormView as CustomFormView
from webapp.forms import SearchForm, IssueForm
from webapp.models import Issue
from django.utils.http import urlencode


class IndexView(ListView):
    model = Issue
    template_name = 'issues/index.html'
    context_object_name = 'issues'
    ordering = '-updated_date'
    paginate_by = 5  # отображает 5 статьи
    paginate_orphans = 2  # отображает на последней страницы сколько будет статей
    page_kwarg = "page"  # можно переопределить

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_value:
            return Issue.objects.filter(
                Q(summary__icontains=self.search_value) | Q(description__icontains=self.search_value))
        return Issue.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            query = urlencode({'search': self.search_value})
            context['query'] = query
            context['search'] = self.search_value
        return context

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get('search')


class DetailView(TemplateView):
    template_name = 'issues/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = kwargs.get("pk")
        issues = get_object_or_404(Issue, pk=pk)
        context['issues'] = issues
        return context


class DeleteView(View):
    def get(self, request, pk):
        issue = get_object_or_404(Issue, pk=pk)
        return render(request, 'issues/index.html', {'issue': issue})

    def post(self, request, pk):
        issue = get_object_or_404(Issue, pk=pk)
        issue.delete()
        return redirect('index')


class CreateView(CustomFormView):
    template_name = 'issues/create.html'
    form_class = IssueForm

    def form_valid(self, form):
        self.issue = form.save()
        return super().form_valid(form)

    def get_redirect_url(self):
        return reverse('detail', kwargs={'pk': self.issue.pk})


class UpdateView(FormView):
    form_class = IssueForm
    template_name = "issues/update.html"

    def dispatch(self, request, *args, **kwargs):
        self.issue = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issues'] = self.issue
        return context

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['instance'] = self.issue
        return form_kwargs

    def form_valid(self, form):
        self.issue = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("detail", kwargs={"pk": self.issue.pk})

    def get_object(self):
        return get_object_or_404(Issue, pk=self.kwargs.get("pk"))
