from django.shortcuts import render, redirect, Http404
from django.core.urlresolvers import reverse
from dashboard.models import PagePos
from .forms import MessageForm, ApplicantForm


def index(request):
    return render(request, 'home/index.html')


def customized_page(request, slug):
    page = PagePos.objects.get_page(slug=slug)
    if not page:
        raise Http404
    return render(request, 'home/customized_page.html', locals())


def contact(request):
    form = MessageForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(reverse('contact'))

    return render(request, 'home/contact.html', locals())


def apply(request):
    form = ApplicantForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(reverse('apply'))

    return render(request, 'home/apply.html', locals())
