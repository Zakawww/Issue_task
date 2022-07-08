from django.shortcuts import render, get_object_or_404, redirect
from .forms import SearchForm, IssueForm
from .models import Issue


# def get_categories():
#     products = Issue.objects.exclude(count=0)
#     categories = []
#     for product in products:
#         category = str(product).split('-')
#         if category[1].strip() not in categories:
#             categories.append(category[1].strip())
#     return categories


def index(request):
    form = SearchForm()
    issues = Issue.objects.order_by('summary')
    # categories = get_categories()
    return render(request, 'index.html', {'issues': issues, 'form': form})


def detail(request, pk):
    issues = get_object_or_404(Issue, pk=pk)
    return render(request, 'detail.html', {'issues': issues})


def delete(request, pk):
    issues = get_object_or_404(Issue, pk=pk)
    issues.delete()
    return redirect('index')


def create(request):
    if request.method == 'GET':
        form = IssueForm()
        return render(request, 'create.html', {'form': form})

    elif request.method == 'POST':
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
            return render(request, 'create.html', context={'form': form})


def update(request, pk):
    issues = get_object_or_404(Issue, pk=pk)

    if request.method == 'GET':
        form = IssueForm(data={
            'summary': issues.summary,
            'description': issues.description,
            'status': issues.category,
            'type': issues.count
        })
        return render(request, 'update.html', context={'form': form, 'issues': issues})

    if request.method == 'POST':
        form = IssueForm(data=request.POST)
        if form.is_valid():
            issues.summary = form.cleaned_data['summary']
            issues.description = form.cleaned_data['description']
            issues.status = form.cleaned_data['status']
            issues.type = form.cleaned_data['type']
            issues.save()
            return redirect('index')
        else:
            return render(request, 'update.html', context={'form': form})

#
# def filter_by_category(request, category):
#     products = Issue.objects.filter(category=category).exclude(count=0).order_by('name')
#     # categories = get_categories()
#     return render(request, 'filter_category.html',
#                   {'products': products, 'categories': categories, 'category': category})


def search(request):
    # categories = get_categories()
    form = SearchForm(data=request.GET)
    if form.is_valid():
        summary = form.cleaned_data['summary']
        issues = Issue.objects.filter(name__contains=summary)
        return render(request, 'index.html', {'issues': issues, 'form': form})
    else:
        return redirect('index')
