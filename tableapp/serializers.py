# tableapp/serializers.py

from rest_framework import serializers
from .models import TrustGuideline, Trust

class TrustSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trust
        fields = ['id', 'name']  # Include other Trust fields if necessary


class TrustGuidelineMinimalSerializer(serializers.ModelSerializer):
    # trust = TrustSerializer(read_only=True)

    class Meta:
        model = TrustGuideline
        fields = [
            'id',
            # 'trust',
            'name',
            'external_url',
            'description',

        ]


class TrustGuidelineSerializer(serializers.ModelSerializer):
    trust = TrustSerializer(read_only=True)
    # pdf_file_url = serializers.SerializerMethodField()

    class Meta:
        model = TrustGuideline
        fields = [
            'id',
            'trust',
            'name',
            'description',
            'external_url',
            'metadata',
            'medical_speciality',
            'locality',
            'original_filename',
            'viewcount',
            'version_number',
            'authors',
            'creation_date',
            'review_date',
            # 'pdf_file',
            # 'pdf_file_url',
        ]
        read_only_fields = ['viewcount']  # If viewcount is managed server-side