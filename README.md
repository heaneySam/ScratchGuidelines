# USEFUL COMMANDS
python manage.py migrate

python manage.py makemigrations

python manage.py runserver

# ScratchGuidelines

A Django-based web application for managing and serving medical guidelines.

## Environment Variables

The following environment variables must be configured in both development (`.env`) and production (Render) environments:

### Required Environment Variables

```plaintext
# Django Settings
SECRET_KEY=your_secret_key
DEBUG=True  # Set to False in production
ALLOWED_HOSTS=localhost 127.0.0.1 your-domain.com
DATABASE_URL=your_database_url

# AWS S3 Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_S3_REGION_NAME=your_s3_region  # e.g., eu-west-2
AWS_STORAGE_BUCKET_NAME=your_bucket_name

# API Authentication
SIMPLE_API_KEY=your_api_key
```

### Important Notes

- Ensure all environment variables are set in both local `.env` file and Render's environment settings
- The `DEBUG` setting should be `False` in production
- `ALLOWED_HOSTS` should include your production domain in Render
- AWS S3 credentials must have proper permissions for file upload/download operations
- Keep your API keys and secrets secure and never commit them to version control

## Local Development

1. Create a `.env` file in the project root
2. Copy the above environment variables and set appropriate values
3. Run migrations: `python manage.py migrate`
4. Start the development server: `python manage.py runserver`

## Deployment on Render

1. Add all environment variables in Render's environment settings
2. Ensure production-specific values are set (DEBUG=False, proper ALLOWED_HOSTS)
3. Configure the build and start commands as specified in `build.sh`