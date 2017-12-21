# Generated by Django 2.0 on 2017-12-15 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edc_action_item', '0002_auto_20171212_0130'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='actionitemupdate',
            options={'get_latest_by': 'modified', 'ordering': ('-modified', '-created')},
        ),
        migrations.RemoveField(
            model_name='actiontype',
            name='prn_form_action',
        ),
        migrations.RemoveField(
            model_name='historicalactionitem',
            name='display_name',
        ),
        migrations.RemoveField(
            model_name='historicalactionitem',
            name='name',
        ),
        migrations.AddField(
            model_name='actiontype',
            name='create_by_action',
            field=models.BooleanField(default=True, help_text='This action may be created by another action'),
        ),
        migrations.AddField(
            model_name='actiontype',
            name='create_by_user',
            field=models.BooleanField(default=True, help_text='This action may be created by the user'),
        ),
        migrations.AddField(
            model_name='actiontype',
            name='show_link_to_changelist',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='actionitem',
            name='instructions',
            field=models.TextField(blank=True, help_text='populated by action class', null=True),
        ),
        migrations.AlterField(
            model_name='actiontype',
            name='display_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='historicalactionitem',
            name='instructions',
            field=models.TextField(blank=True, help_text='populated by action class', null=True),
        ),
        migrations.RemoveField(
            model_name='actionitem',
            name='display_name',
        ),
        migrations.RemoveField(
            model_name='actionitem',
            name='name',
        ),
        migrations.AlterUniqueTogether(
            name='actionitem',
            unique_together={('subject_identifier', 'action_type', 'reference_identifier')},
        ),
        migrations.AlterUniqueTogether(
            name='actionitemupdate',
            unique_together=set(),
        ),
    ]