# Generated by Django 3.0.5 on 2020-05-25 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_accounting_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounting',
            name='consultation_price',
            field=models.DecimalField(decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AddField(
            model_name='accounting',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Doctor'),
        ),
        migrations.AddField(
            model_name='accounting',
            name='item_price',
            field=models.DecimalField(decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name='accounting',
            name='item',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.DeleteModel(
            name='Item',
        ),
    ]
