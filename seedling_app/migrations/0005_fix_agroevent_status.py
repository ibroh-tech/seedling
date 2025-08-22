from django.db import migrations, models
import django.db.models.deletion

def set_default_status(apps, schema_editor):
    StatusTypes = apps.get_model('seedling_app', 'StatusTypes')
    AgroEvent = apps.get_model('seedling_app', 'AgroEvent')
    
    # Get or create a default status if it doesn't exist
    default_status, created = StatusTypes.objects.get_or_create(
        name='Default Status',
        defaults={'status_for': 'AGRO_EVENT'}
    )
    
    # Update all existing AgroEvent records to use the default status
    AgroEvent.objects.filter(status__isnull=True).update(status=default_status)

class Migration(migrations.Migration):
    dependencies = [
        ('seedling_app', '0004_add_status_to_agroevent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agroevent',
            name='status',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='agro_events',
                to='seedling_app.statustypes',
                default=1
            ),
        ),
        migrations.RunPython(set_default_status, reverse_code=migrations.RunPython.noop),
    ]
