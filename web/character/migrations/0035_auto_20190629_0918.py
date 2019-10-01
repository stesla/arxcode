# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-06-29 16:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


def add_involvements_and_permissions(apps, schema_editor):
    """Bulk-create through models for the fields we've placed on death raw."""
    Flashback = apps.get_model('character', 'Flashback')
    FlashbackInvolvement = apps.get_model('character', 'FlashbackInvolvement')
    FlashbackPostPermission = apps.get_model('character', 'FlashbackPostPermission')
    involvements = []
    permissions = []
    for fb in Flashback.objects.all():
        owner = fb.owner
        participants = set([owner] + [ob for ob in fb.allowed.all()])
        involvements.append(FlashbackInvolvement(flashback=fb, participant=owner, status=2))
        for friend in fb.allowed.all():
            if friend != owner:
                involvements.append(FlashbackInvolvement(flashback=fb, participant=friend, status=1))
        for post in fb.posts.all():
            poster = post.poster
            for reader in participants:
                if reader != poster:
                    permissions.append(FlashbackPostPermission(post=post, reader=reader, is_read=False))
    FlashbackInvolvement.objects.bulk_create(involvements)
    FlashbackPostPermission.objects.bulk_create(permissions)


class Migration(migrations.Migration):

    dependencies = [
        ('character', '0034_auto_20190526_1345'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlashbackInvolvement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveSmallIntegerField(blank=True, choices=[(0, b'Retired'), (1, b'Contributor'),
                                                                                 (2, b'Owner')], default=1)),
                ('roll', models.CharField(blank=True, max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='FlashbackPostPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='flashback',
            name='allowed',
        ),
        migrations.RemoveField(
            model_name='flashback',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='flashbackpost',
            name='read_by',
        ),
        migrations.AddField(
            model_name='flashback',
            name='concluded',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='flashbackpost',
            name='roll',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='flashbackpost',
            name='poster',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='flashback_posts', to='character.RosterEntry'),
        ),
        migrations.AddField(
            model_name='flashbackpostpermission',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flashback_post_permissions', to='character.FlashbackPost'),
        ),
        migrations.AddField(
            model_name='flashbackpostpermission',
            name='reader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flashback_post_permissions', to='character.RosterEntry'),
        ),
        migrations.AddField(
            model_name='flashbackinvolvement',
            name='flashback',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flashback_involvements', to='character.Flashback'),
        ),
        migrations.AddField(
            model_name='flashbackinvolvement',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flashback_involvements', to='character.RosterEntry'),
        ),
        migrations.AddField(
            model_name='flashback',
            name='participants',
            field=models.ManyToManyField(related_name='flashbacks', through='character.FlashbackInvolvement', to='character.RosterEntry'),
        ),
        migrations.AddField(
            model_name='flashbackpost',
            name='readable_by',
            field=models.ManyToManyField(blank=True, related_name='readable_flashback_posts', through='character.FlashbackPostPermission', to='character.RosterEntry'),
        ),
        migrations.AlterUniqueTogether(
            name='flashbackpostpermission',
            unique_together=set([('post', 'reader')]),
        ),
        migrations.AlterUniqueTogether(
            name='flashbackinvolvement',
            unique_together=set([('flashback', 'participant')]),
        ),
    ]