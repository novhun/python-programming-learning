from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(help_text="The title of the curriculum course", max_length=150)),
                ("instructor", models.CharField(help_text="Lead instructor full name", max_length=100)),
                ("price", models.DecimalField(decimal_places=2, help_text="Tuition in USD", max_digits=7)),
                ("category", models.CharField(default="Software Engineering", max_length=50)),
                ("is_published", models.BooleanField(default=True, help_text="Check to make visible in the public catalog")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Course",
                "verbose_name_plural": "Courses",
                "ordering": ["-created_at"],
            },
        ),
    ]
