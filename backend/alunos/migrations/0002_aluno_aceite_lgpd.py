from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alunos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='aluno',
            name='aceite_lgpd',
            field=models.BooleanField(default=False, verbose_name='Aceitou a LGPD'),
        ),
        migrations.AddField(
            model_name='aluno',
            name='data_aceite_lgpd',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Data do aceite LGPD'),
        ),
    ]
