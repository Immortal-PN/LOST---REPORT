from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib import messages

from .models import LostItem, FoundItem, ContactMessage
from .forms import LostItemForm, FoundItemForm



# HOME PAGE

def home(request):

    query = request.GET.get('q')

    lost_items = LostItem.objects.all().order_by('-created_at')[:6]
    found_items = FoundItem.objects.all().order_by('-created_at')[:6]

    

    if query:
        lost_items = LostItem.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )

        found_items = FoundItem.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )

    lost_count = LostItem.objects.count()
    found_count = FoundItem.objects.count()
    user_count = User.objects.count()

    return render(request,"home.html",{
        "lost_items":lost_items,
        "found_items":found_items,
        "lost_count":lost_count,
        "found_count":found_count,
        "user_count":user_count
    })



# LOST ITEMS PAGE

def lost_items(request):

    items = LostItem.objects.all().order_by("-created_at")

    return render(request,"lost_items.html",{"items":items})



# FOUND ITEMS PAGE

def found_items(request):

    items = FoundItem.objects.all().order_by('-created_at')

    return render(request, 'found_items.html', {'items': items})



# REPORT LOST ITEM



@login_required
def report_lost(request):

    if request.method == "POST":

        form = LostItemForm(request.POST, request.FILES)

        if form.is_valid():

            item = form.save(commit=False)
            item.user = request.user
            item.save()

            messages.success(request,"Lost item reported successfully")

            return redirect("lost_items")

        else:

            messages.error(request,"Please correct the errors in the form")

    else:

        form = LostItemForm()

    return render(request,"report_lost.html",{"form":form})



# REPORT FOUND ITEM


@login_required
def report_found(request):

    if request.method == "POST":

        form = FoundItemForm(request.POST, request.FILES)

        if form.is_valid():

            item = form.save(commit=False)
            item.user = request.user
            item.save()

            messages.success(request,"Found item reported successfully")

            return redirect("found_items")

        else:

            messages.error(request,"Please correct the errors in the form")

    else:

        form = FoundItemForm()

    return render(request,"report_found.html",{"form":form})



# USER REGISTRATION

def register(request):

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            user.email = request.POST.get("email")
            user.save()

            login(request,user)

            return redirect("home")

    else:

        form = UserCreationForm()

    return render(request,"register.html",{"form":form})



# USER DASHBOARD

@login_required
def profile(request):

    user_lost_items = LostItem.objects.filter(user=request.user)
    user_found_items = FoundItem.objects.filter(user=request.user)

    return render(request,"profile.html",{
        "user_lost_items":user_lost_items,
        "user_found_items":user_found_items
    })



# USER INBOX

@login_required
def inbox(request):

    messages = ContactMessage.objects.filter(receiver=request.user).order_by('-created_at')

    return render(request,"inbox.html",{
        "messages":messages
    })



# CONTACT ITEM OWNER


@login_required
def contact_user(request, user_id):

    receiver = User.objects.get(id=user_id)

    if request.method == "POST":

        message = request.POST.get("message")

        ContactMessage.objects.create(
            sender=request.user,
            receiver=receiver,
            message=message
        )

        # EMAIL NOTIFICATION
        send_mail(
            subject="LostLink Notification",
            message=f"{request.user.username} contacted you regarding an item.\n\nMessage:\n{message}",
            from_email=None,
            recipient_list=[receiver.email],
            fail_silently=True,
        )

        return redirect("home")

    return render(request,"contact.html",{"receiver":receiver})