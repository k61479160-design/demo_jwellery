# Generated manually to replace categories ManyToManyField with category CharField

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jewelry", "0040_alter_diamondproduct_certification_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="categories",
        ),
        migrations.AddField(
            model_name="product",
            name="category",
            field=models.CharField(
                default="",
                help_text="Enter the category name manually",
                max_length=255,
                verbose_name="Product Category",
            ),
            preserve_default=False,
        ),
    ]
