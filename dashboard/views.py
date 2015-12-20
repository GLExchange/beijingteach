from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from home.models import Message
from .models import Snippet
from .forms import SnippetForm

dashboard_login_required = login_required(login_url='/dashboard/login/')


@dashboard_login_required
def index(request):
    messages = Message.objects.order_by('-updated')
    return render(request, 'dashboard/index.html', locals())


@dashboard_login_required
def snippets(request):
    snippets = Snippet.objects.order_by('-updated')
    return render(request, 'dashboard/snippets.html', locals())


@dashboard_login_required
def new_snippet(request):
    form = SnippetForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(reverse('dashboard:snippets'))

    return render(request, 'dashboard/edit_snippet.html', locals())


@dashboard_login_required
def update_snippet(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    initial = {}
    if snippet.has_pos():
        initial = {'position': snippet.position.slug}

    form = SnippetForm(request.POST or None, initial=initial, instance=snippet)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(reverse('dashboard:snippets'))

    return render(request, 'dashboard/edit_snippet.html', locals())


def login_user(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', reverse('dashboard:index'))
            return redirect(next_url)
        else:
            message = "The username and password were incorrect."

    return render(request, 'dashboard/login.html', locals())
