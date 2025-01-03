# serializers.py

from rest_framework import serializers
from .models import TrustGuideline

class TrustGuidelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrustGuideline
        fields = '__all__'

    def validate_pdf_file(self, value):
        """
        Validate that the uploaded file does not exceed the maximum allowed size.
        """
        if value:
            # Remove file type validation by commenting out or deleting the following lines:
            # if not value.name.lower().endswith('.pdf'):
            #     raise serializers.ValidationError("Only PDF files are allowed.")

            # Increase file size limit (e.g., to 50MB)
            max_size = 50 * 1024 * 1024  # 50MB
            if value.size > max_size:
                raise serializers.ValidationError("File size must be under 50MB.")

        return value
