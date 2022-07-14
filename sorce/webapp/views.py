from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView, View, FormView

from .base_view import FormView as CustomFormView
from .forms import SearchForm, IssueForm
from .models import Issue


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = SearchForm()
        issues = Issue.objects.all()
        context['issues'] = issues
        context['form'] = form
        return context


class DetailView(TemplateView):
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = kwargs.get("pk")
        issues = get_object_or_404(Issue, pk=pk)
        context['issues'] = issues
        return context


class DeleteView(View):
    def get(self, request, pk):
        issue = get_object_or_404(Issue, pk=pk)
        return render(request, 'index.html', {'issue': issue})

    def post(self, request, pk):
        issue = get_object_or_404(Issue, pk=pk)
        issue.delete()
        return redirect('index')


class CreateView(CustomFormView):
    template_name = 'create.html'
    form_class = IssueForm

    def form_valid(self, form):
        # data = {}
        # type = form.cleaned_data.pop('type')
        # for key, value in form.cleaned_data.items():
        #     if value is not None:
        #         data[key] = value
        # self.issue = Issue.objects.create(**data)
        # self.issue.type.set(type)
        self.issue = form.save()
        return super().form_valid(form)

    def get_redirect_url(self):
        return reverse('detail', kwargs={'pk': self.issue.pk})


class UpdateView(FormView):
    form_class = IssueForm
    template_name = "update.html"

    def dispatch(self, request, *args, **kwargs):
        self.issue = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issues'] = self.issue
        return context

    # def get_initial(self):
    #     initial = {}
    #     for key in 'summary', 'description', 'status', 'type':
    #         initial[key] = getattr(self.issue, key)
    #     initial['type'] = self.issue.type.all()
    #     return initial

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['instance'] = self.issue
        return form_kwargs

    def form_valid(self, form):
        # type = form.cleaned_data.pop('type')
        # for key, value in form.cleaned_data.items():
        #     if value is not None:
        #         setattr(self.issue, key, value)
        # self.issue.save()
        # self.issue.type.set(type)
        self.issue = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("detail", kwargs={"pk": self.issue.pk})

    def get_object(self):
        # pk = self.kwargs.get('pk')
        # return get_object_or_404(Issue, pk=pk)
        return get_object_or_404(Issue, pk=self.kwargs.get("pk"))


def search(request):
    form = SearchForm(data=request.GET)
    if form.is_valid():
        summary = form.cleaned_data['summary']
        issues = Issue.objects.filter(summary__contains=summary)
        return render(request, 'index.html', {'issues': issues, 'form': form})
    else:
        return redirect('index')
