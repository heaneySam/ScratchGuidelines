from django.shortcuts import render, redirect, get_object_or_404
from django_tables2 import RequestConfig
from .models import CustomGuidelines, TrustGuideline, FavouriteGuideline
from .forms import GuidelineForm
from .tables import GuidelineTable, TrustGuidelineTable, FavouriteGuidelineTable
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


@login_required
@require_POST
def add_to_favourites(request, pk):
    if request.method == 'POST':
        guideline = get_object_or_404(TrustGuideline, pk=pk)
        obj, created = FavouriteGuideline.objects.get_or_create(user=request.user, guideline=guideline)
        if not created:
            obj.delete()  # If it was already a favourite, unfavourite it
            return JsonResponse({'status': 'ok', 'created': False})
        else:
            return JsonResponse({'status': 'ok', 'created': True})


def favourite_guideline(request, pk):
    guideline = get_object_or_404(TrustGuideline, pk=pk)
    FavouriteGuideline.objects.get_or_create(user=request.user, guideline=guideline)
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def unfavourite_guideline(request, pk):
    guideline = get_object_or_404(TrustGuideline, pk=pk)
    FavouriteGuideline.objects.filter(user=request.user, guideline=guideline).delete()
    return JsonResponse({'status': 'ok'})


def trust_guideline_view(request):
    table = TrustGuidelineTable(TrustGuideline.objects.all())
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    context = {
        'table': table
    }
    return render(request, 'tableapp/trust_guidelines_table.html', context)

def delete_guideline(request, pk):
    guideline = CustomGuidelines.objects.get(pk=pk)
    guideline.delete()
    return redirect('guideline_view')

def bulk_delete_guidelines(request):
    if request.method == 'POST':
        ids_to_delete = request.POST.getlist('selection')
        CustomGuidelines.objects.filter(id__in=ids_to_delete).delete()
    return redirect('guideline_view')

def guideline_view(request):
    if request.method == 'POST':
        form = GuidelineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('guideline_view')
    else:
        form = GuidelineForm()

    table = GuidelineTable(CustomGuidelines.objects.all())
    RequestConfig(request, paginate={"per_page": 10}).configure(table)

    context = {
        'form': form,
        'table': table,
        'is_authenticated':request.user.is_authenticated
    }
    return render(request, 'tableapp/customTable.html', context)


# Create your views here.
from django.shortcuts import render

def customTable(request):
    is_authenticated = request.user.is_authenticated
    return render(request, 'tableapp/customTable.html', {'is_authenticated': is_authenticated})


def favourite_guideline_view(request):
    if request.user.is_authenticated:
        user_favourites = FavouriteGuideline.objects.filter(user=request.user)
    else:
        user_favourites = FavouriteGuideline.objects.none()  # Return an empty queryset for anonymous users

    table = FavouriteGuidelineTable(user_favourites, request=request)
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    context = {
        'table': table,
        'is_authenticated': request.user.is_authenticated  # Pass authentication status to the template
    }
    return render(request, 'tableapp/favourite_guidelines_table.html', context)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                #messages.info(request, f"You are now logged in as {username}.")
                return redirect('favourite_guideline_view')  # Redirect to a success page.
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'tableapp/login.html', {'form': form})