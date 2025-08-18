from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resume', to='auth.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resume',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='resume',
            name='full_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='resume',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='resume',
            name='phone',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
