import django_tables2 as tables
from django.utils.html import format_html
from .models import Guideline
from django_tables2.utils import A  # Alias for Accessor

class GuidelineTable(tables.Table):
    name = tables.Column(orderable=True, verbose_name='Name')
    description = tables.Column(orderable=True, verbose_name='Description')
    selection = tables.CheckBoxColumn(accessor="pk", attrs={"th__input": {"onclick": "toggleAll(this)"}})
    delete = tables.LinkColumn('guideline_delete', args=[A('pk')], orderable=False, text='Delete', attrs={"a": {"class": "btn btn-danger btn-sm"}})

    def render_name(self, record):
        if record.external_url:
            return format_html('<a href="{}" target="_blank">{}</a>', record.external_url, record.name)
        return record.name  # Return just the name if there is no URL

    class Meta:
        model = Guideline
        template_name = "django_tables2/bootstrap.html"
        fields = ("selection", "name", "description", "delete")  # Specify which fields to display
        attrs = {"class": "table table-striped table-hover"}
