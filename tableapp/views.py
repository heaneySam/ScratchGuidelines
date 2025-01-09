from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views import View
from django_tables2 import RequestConfig, SingleTableView, SingleTableMixin
from django_filters.views import FilterView
from django_tables2 import RequestConfig, SingleTableView

from .authentication import APIKeyAuthentication
from .models import CustomGuidelines, TrustGuideline, FavouriteGuideline, Trust
from .forms import GuidelineForm, TrustForm
from .tables import CustomGuidelineTable, TrustGuidelineTable, FavouriteGuidelineTable
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from .filters import TrustGuidelineFilter
from rest_framework import viewsets, permissions, status, generics
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from .models import TrustGuideline
from .serializers import TrustGuidelineSerializer
from django.conf import settings
import boto3
from botocore.exceptions import ClientError
import logging



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def validate_password(request):
#     if request.method == "POST":
#         input_password = request.POST.get('password')
#         correct_password = "asdf"  # Replace with your actual password
#
#         if input_password == correct_password:
#             return JsonResponse({'valid': True})
#         else:
#             return JsonResponse({'valid': False})
#
#     return JsonResponse({'valid': False}, status=400)

# Configure logger
logger = logging.getLogger(__name__)

class TestAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"success": True})




class TrustGuidelineListAPIView(generics.ListAPIView):
    """
    API endpoint that allows TrustGuidelines to be viewed.
    """
    queryset = TrustGuideline.objects.all().order_by('-viewcount')  # Adjust ordering as needed
    serializer_class = TrustGuidelineSerializer
    permission_classes = [IsAuthenticated]

class TrustGuidelineViewSet(viewsets.ModelViewSet):
    queryset = TrustGuideline.objects.all()
    serializer_class = TrustGuidelineSerializer
    authentication_classes = [APIKeyAuthentication]
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['medical_speciality', 'locality']  # Add fields you want to filter by

    def perform_update(self, serializer):
        instance = self.get_object()
        new_pdf = self.request.FILES.get('pdf_file', None)

        if new_pdf and instance.pdf_file:
            # Initialize S3 client
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME,
            )

            # Get the old file's S3 key
            old_file_key = instance.pdf_file.name  # This includes the path

            try:
                # Delete the old file from S3
                s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=old_file_key)
                logger.debug(f"Deleted old PDF from S3: {old_file_key}")
            except ClientError as e:
                logger.error(f"Failed to delete old PDF from S3: {e}")
                # Optionally, you can choose to raise an exception or handle it as needed
                raise Exception("Failed to delete the old PDF from storage.")

        # Save the new PDF (this will upload it to S3 via the FileField)
        serializer.save()
        logger.debug(f"Updated TrustGuideline ID {instance.id} with new PDF.")


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


class TrustGuidelineListView(SingleTableView):
    model = TrustGuideline
    table_class = TrustGuidelineTable
    template_name = 'tableapp/trust_guidelines_table.html'
    filterset_class = TrustGuidelineFilter
    paginate_by = 25  # Sets pagination to 30 items per page

    def get_queryset(self):
        trust_id = self.request.GET.get('trust')
        if trust_id:
            return TrustGuideline.objects.filter(trust_id=trust_id)
        else:
            default_trust_name = 'UHD'
            default_trust = Trust.objects.filter(name=default_trust_name).first()
            if default_trust:
                return TrustGuideline.objects.filter(trust=default_trust)
            else:
                return TrustGuideline.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trusts'] = Trust.objects.all()
        context['selected_trust'] = self.request.GET.get('trust')
        context['filter'] = self.filterset

    paginate_by = 40  # You can adjust the number of items per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Getting the filtered queryset
        filtered_qs = self.filterset_class(self.request.GET, queryset=self.get_queryset())
        table = self.table_class(filtered_qs.qs)
        RequestConfig(self.request, paginate={"per_page": self.paginate_by}).configure(table)
        context['table'] = table  # Add the table to the context
        context['filter'] = filtered_qs  # Add the filter to the context
        return context

    def get_queryset(self):
        # This can be customized to return a more specific queryset if necessary
        return super().get_queryset()

    def render_to_response(self, context, **response_kwargs):
        if 'HX-Request' in self.request.headers:
            # HTMX ajax request; return only the table part
            return render(self.request, 'tableapp/partials/trust_guideline_table_partial.html', context)
        # Normal request; return the full page
        return super().render_to_response(context, **response_kwargs)


class RedirectAndCountView(View):
    def get(self, request, pk):
        guideline = get_object_or_404(TrustGuideline, pk=pk)
        # Use F() to prevent race conditions
        print(f"URL: {guideline.external_url}, View Count: {guideline.viewcount}")

        TrustGuideline.objects.filter(pk=pk).update(viewcount=F('viewcount') + 1)

        # Reload the object to get the updated viewcount
        guideline.refresh_from_db()
        # Print the URL and the current view count
        print(f"URL: {guideline.external_url}, View Count: {guideline.viewcount}")

        return redirect(guideline.external_url)


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

    table = CustomGuidelineTable(CustomGuidelines.objects.all())
    RequestConfig(request, paginate={"per_page": 50}).configure(table)

    context = {
        'form': form,
        'table': table,
        'is_authenticated': request.user.is_authenticated
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
    RequestConfig(request, paginate={"per_page": 20}).configure(table)
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
