# Generated by Django 3.2.25 on 2024-11-02 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polybook', '0003_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='pdf_file',
            field=models.FileField(upload_to='media/pdfs'),
        ),
    ]
