# Generated by Django 3.2 on 2021-05-01 10:18
from django.conf import settings
from django.db import migrations
from django.contrib.auth.models import User, Group, Permission, ContentType

from paymobApp.api.models import Product

class Migration(migrations.Migration):

    dependencies = [
    ('paymobApp', '0001_initial'),
    migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    
    
    def makeGroupsPermissions(apps, schema_editor):

        content_type = ContentType.objects.get_for_model(Product, for_concrete_model=True)

        payProductPermission = Permission(codename='can_pay', name='Can pay product', content_type=content_type)
        addProductPermission = Permission(codename='can_add_product', name= 'Can add product', content_type=content_type)
        payProductPermission.save()
        addProductPermission.save()

       # adminGroup = Group('admin', [addProductPermission])
       # adminGroup.save()
       # normalGroup = Group('normal', [payProductPermission])
       # normalGroup.save()

    operations = [
        migrations.RunPython(makeGroupsPermissions,reverse_code=lambda *args,**kwargs: True)

    ]
