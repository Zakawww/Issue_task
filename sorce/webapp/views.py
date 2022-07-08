from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, View

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


class CreateView(View):
    def get(self, request, *args, **kwargs):
        form = IssueForm()
        return render(request, 'create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = IssueForm(data=request.POST)
        if form.is_valid():
            Issue.objects.create(
                summary=form.cleaned_data['summary'],
                description=form.cleaned_data['description'],
                status=form.cleaned_data['status'],
                type=form.cleaned_data['type']
            )
            return redirect('index')
        else:
            return render(request, 'create.html', {'form': form})


class UpdateView(View):
    def get(self, request, *args, **kwargs):
        issue_pk = kwargs.get('pk')
        issue = get_object_or_404(Issue, pk=issue_pk)
        form = IssueForm(data={
            'summary': issue.summary,
            'description': issue.description,
            'status': issue.status.id,
            'type': issue.type.id
        })
        return render(request, 'update.html', {'form': form, 'issue': issue})

    def post(self, request, *args, **kwargs):
        form = IssueForm(data=request.POST)
        issue_pk = kwargs.get('pk')
        issue = get_object_or_404(Issue, pk=issue_pk)
        if form.is_valid():
            issue.summary = form.cleaned_data['summary']
            issue.description = form.cleaned_data['description']
            issue.status = form.cleaned_data['status']
            issue.type = form.cleaned_data['type']
            issue.save()
            return redirect('index')
        else:
            return render(request, 'update.html', {'form': form, 'issue': issue})


def search(request):
    form = SearchForm(data=request.GET)
    if form.is_valid():
        summary = form.cleaned_data['summary']
        issues = Issue.objects.filter(summary__contains=summary)
        return render(request, 'index.html', {'issues': issues, 'form': form})
    else:
        return redirect('index')
