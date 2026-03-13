from django.shortcuts import render, redirect
from .models import LostItem, FoundItem
from .forms import LostItemForm, FoundItemForm


def home(request):
    return render(request, "home.html")


def lost_items(request):

    items = LostItem.objects.all()

    return render(request, "lost_items.html", {"items": items})


def found_items(request):

    items = FoundItem.objects.all()

    return render(request, "found_items.html", {"items": items})


def report_lost(request):

    if request.method == "POST":

        form = LostItemForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("lost_items")

    else:
        form = LostItemForm()

    return render(request, "report_lost.html", {"form": form})


def report_found(request):

    if request.method == "POST":

        form = FoundItemForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("found_items")

    else:
        form = FoundItemForm()

    return render(request, "report_found.html", {"form": form})