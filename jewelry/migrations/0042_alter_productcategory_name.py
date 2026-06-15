# Generated manually to remove choices from ProductCategory.name field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jewelry", "0041_remove_product_categories_product_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productcategory",
            name="name",
            field=models.CharField(
                max_length=100,
                unique=True,
                verbose_name="Category Name",
            ),
        ),
    ]
