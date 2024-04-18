from django.shortcuts import render, redirect
from django_tables2 import RequestConfig
from .models import Guideline
from .forms import GuidelineForm
from .tables import GuidelineTable

def delete_guideline(request, pk):
    guideline = Guideline.objects.get(pk=pk)
    guideline.delete()
    return redirect('guideline_view')

def bulk_delete_guidelines(request):
    if request.method == 'POST':
        ids_to_delete = request.POST.getlist('selection')
        Guideline.objects.filter(id__in=ids_to_delete).delete()
    return redirect('guideline_view')

def guideline_view(request):
    if request.method == 'POST':
        form = GuidelineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('guideline_view')
    else:
        form = GuidelineForm()

    table = GuidelineTable(Guideline.objects.all())
    RequestConfig(request, paginate={"per_page": 10}).configure(table)

    context = {
        'form': form,
        'table': table
    }
    return render(request, 'tableapp/customTable.html', context)


# Create your views here.
def customTable(request):
    return render(request, 'tableapp/customTable.html')