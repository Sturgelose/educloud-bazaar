# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmbeddedMedia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(max_length=4000)),
                ('product', models.ForeignKey(to='catalogue.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('hasLanguage', models.ManyToManyField(to='catalogue.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductFormat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', models.SlugField(unique=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('lastModified', models.DateTimeField(auto_now_add=True)),
                ('hasTags', models.ManyToManyField(to='catalogue.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='product',
            name='attributionText',
            field=models.TextField(max_length=4000, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='attributionURL',
            field=models.CharField(max_length=4000, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='contentLicense',
            field=models.CharField(max_length=4000, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='contributionDate',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='copyrightNotice',
            field=models.CharField(max_length=4000, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='dataLicense',
            field=models.CharField(max_length=4000, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='icon',
            field=models.ImageField(null=True, upload_to=b'/media/icons', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='iconUrl',
            field=models.URLField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='materialUrl',
            field=models.URLField(blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='maximumAge',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='minimumAge',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='moreInfoUrl',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='product_format',
            field=models.ForeignKey(related_name='products', on_delete=django.db.models.deletion.PROTECT, verbose_name='Product Format', to='catalogue.ProductFormat', help_text='Choose what is product format', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='uuid',
            field=models.CharField(max_length=50, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='version',
            field=models.CharField(max_length=50, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='visible',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
