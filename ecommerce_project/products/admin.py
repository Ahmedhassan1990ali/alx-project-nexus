from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.exceptions import ValidationError
from django import forms
from products.models import Product, Product_Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "updated_by", "updated_at")

    def save_model(self, request, obj, form, change):
        if change:  # if it's an update
            obj.updated_by = request.user
        obj.save()

admin.site.register(Product_Category)



class SafeUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"

    def clean_is_superuser(self):
        # Prevent user from removing their own superuser status
        if not self.instance.is_superuser:
            return self.cleaned_data["is_superuser"]
        if (
            self.instance == self.initial.get("instance")  # editing yourself
            and not self.cleaned_data["is_superuser"]
        ):
            raise ValidationError("You cannot remove your own superuser status.")
        return self.cleaned_data["is_superuser"]

class UserAdmin(BaseUserAdmin):
    form = SafeUserChangeForm

    def delete_model(self, request, obj):
        if obj == request.user and obj.is_superuser:
            raise ValidationError("You cannot delete your own superuser account.")
        return super().delete_model(request, obj)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

