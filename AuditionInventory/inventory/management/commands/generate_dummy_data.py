import os
import random
from pathlib import Path
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.files import File
from django.core.management import BaseCommand
from datetime import datetime, timedelta
from django.db.models import DateTimeField, CharField, ForeignKey, DecimalField, IntegerField, FileField


def generate_random_words():
    words = ['apple','tyre','oil','gas','banana','lychee']
    return random.choice(words)


def generate_random_datetime(start_date, end_date):
    # Convert start_date and end_date to datetime objects if they are not already
    if not isinstance(start_date, datetime):
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    if not isinstance(end_date, datetime):
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

    # Calculate the time difference between start_date and end_date
    delta = end_date - start_date

    # Generate a random number of seconds within the time difference
    random_seconds = random.randint(0, 60)

    # Add the random number of seconds to the start_date to get the random datetime
    random_datetime = start_date + timedelta(seconds=random_seconds)

    return random_datetime


def get_random_user():
    user_model = get_user_model()
    total_user_count = user_model.objects.all().count()
    random_id = random.randint(1, total_user_count)
    return user_model.objects.get(pk=random_id)


def get_random_fk(model):
    record_ids_list =  model.objects.all().values_list('id',flat=True)
    random_id = random.choice(record_ids_list)
    return model.objects.get(pk=random_id)


def generate_random_decimal(min_value=0, max_value=100, precision=2):
    return round(random.uniform(min_value, max_value), precision)


def generate_random_integer(min_value=1, max_value=1000):
    return random.randint(min_value, max_value)


def get_random_image(directory='stock_images'):
    files = os.listdir(directory)
    images_files = [file for file in files if file.endswith(('.jpg','png','jpeg'))]
    random_image = random.choice(images_files)
    image_path = os.path.join(directory, random_image)
    return image_path


class Command(BaseCommand):
    def handle(self, *args, **options):
        model_name = input("Enter model name: ")
        try:
            start_date = datetime.now().replace(month=1, day=1)
            end_date = datetime.now()
            content_type = ContentType.objects.get(model__iexact=model_name)
            model = content_type.model_class()
            no_of_records = int(input("Enter number of records: "))
            print(f"Generating {no_of_records} records for the model {content_type.model}")
            records_to_create = []
            user_model = get_user_model()
            default_user, created = user_model.objects.get_or_create(username='System')
            model_fields = model._meta.get_fields()
            file_fields = [field for field in model_fields if isinstance(field, FileField)]
            for count in range(no_of_records):
                record = {}
                new_record = model()
                for field in model_fields:
                    field_name = field.name
                    if field_name == 'id':
                        continue
                    if isinstance(field, DateTimeField):
                        record[field] = generate_random_datetime(start_date, end_date)
                        setattr(new_record, field_name, generate_random_datetime(start_date, end_date))
                    if isinstance(field, CharField):
                        record[field] = generate_random_words()
                        setattr(new_record, field_name, generate_random_words())
                    if isinstance(field, ForeignKey):
                        field_model = field.related_model
                        record[field] = get_random_fk(field_model)
                        setattr(new_record, field_name, get_random_fk(field_model))
                    if isinstance(field, DecimalField):
                        setattr(new_record, field_name, generate_random_decimal())
                    if isinstance(field, IntegerField):
                        setattr(new_record, field_name, generate_random_integer())
                    # if isinstance(field, FileField):
                    #     image_path = get_random_image()
                    #     with open(image_path, mode='rb') as f:
                    #         setattr(new_record, field_name, File(f))
                    #
                records_to_create.append(new_record)
            # bulk create using django queryset bulk create
            queryset = model.objects.bulk_create(
                records_to_create
            )
            for file_field in file_fields:
                for record in queryset:
                    image_path = get_random_image()
                    path = Path(image_path)
                    with path.open(mode='rb') as f:
                        setattr(record, file_field.name, File(f, name=path.name))
                        # record.image=File(f, name=path.name)
                        record.save()
        except ContentType.DoesNotExist as e:
            print(f'Model with that name {model_name} cannot be found')