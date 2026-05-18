from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('core', '0004_expensa'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='Perfil',
                    fields=[
                    ],
                    options={},
                    bases=(),
                ),
            ],
            database_operations=[],
        ),
    ]
