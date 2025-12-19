from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ObjectDoesNotExist
from django.utils.html import format_html

from .models import (DiamondProduct, DiscountCode, Payment, Product,
                     ProductCategory, UserDiscount, UserProfile)


class ProductCategoryAdmin(admin.ModelAdmin):


    list_display = [
        "display_name",
        "name",
        "icon",
        "is_active",
        "sort_order",
        "product_count",
    ]

    list_filter = ["is_active"]

    search_fields = ["display_name", "description"]

    list_editable = ["is_active", "sort_order", "icon"]

    fieldsets = (
        ("Basic Information", {"fields": ("name", "display_name", "description")}),
        ("Display Settings", {"fields": ("icon", "is_active", "sort_order")}),
    )

    def product_count(self, obj):
        # Count products that have this category name in their category field
        from .models import Product
        count = Product.objects.filter(category__icontains=obj.display_name, status="active").count()
        # Add diamond products count
        diamond_count = obj.diamond_products.filter(status="available").count()
        total_count = count + diamond_count
        return format_html(
            '<span style="background: #e3f2fd; padding: 4px 8px; border-radius: 12px; font-weight: bold;">{}</span>',
            total_count,
        )

    product_count.short_description = "Products"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):


    list_display = [
        "id",
        "name",
        "category",
        "metal_type",
        "carat",
        "weight",
        "diamond_weight",
        "net_weight",
        "gold_clarity",
        "status",
        "badge",
        "created_at",
        "image_preview",
        "hover_video_preview",
    ]

    list_filter = [
        "category",
        "metal_type",
        "status",
        "badge",
        "gold_clarity",
        "created_at",
    ]

    search_fields = ["name", "description", "metal_purity"]

    list_editable = ["status", "badge"]

    readonly_fields = [
        "created_at",
        "updated_at",
        "image_preview",
        "hover_video_preview",
        "materials_summary",
    ]


    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "name",
                    "description",
                    "image",
                    "hover_video",
                    "image_preview",
                    "hover_video_preview",
                    "category",
                )
            },
        ),
        (
            "Product Specifications",
            {"fields": ("carat", "weight", "metal_type", "metal_purity")},
        ),
        (
            "Gold Product Specifications",
            {"fields": ("diamond_weight", "net_weight", "gold_clarity")},
        ),

        ("Product Status & Badges", {"fields": ("status", "badge")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    actions = ["mark_as_active", "mark_as_inactive"]


    def image_preview(self, obj):

        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px;" />',
                obj.image.url,
            )
        return "No Image"

    image_preview.short_description = "Image Preview"

    def hover_video_preview(self, obj):
        if obj.hover_video:
            return format_html(
                '<video src="{}" style="max-height: 50px; max-width: 50px;" autoplay muted loop playsinline></video>',
                obj.hover_video.url,
            )
        return "No Hover Video"

    hover_video_preview.short_description = "Hover Video Preview"

    def materials_summary(self, obj):

        materials = obj.get_materials_list()
        if materials:
            return format_html(
                '<div style="background: #f8f9fa; padding: 8px; border-radius: 4px;">'
                "<strong>Materials:</strong><br>{}"
                "</div>",
                "<br>".join([f"• {material}" for material in materials]),
            )
        return "No materials specified"

    materials_summary.short_description = "Materials Summary"

    def mark_as_active(self, request, queryset):

        updated = queryset.update(status="active")
        self.message_user(request, f"{updated} products marked as active.")

    mark_as_active.short_description = "Mark selected products as active"

    def mark_as_inactive(self, request, queryset):

        updated = queryset.update(status="inactive")
        self.message_user(request, f"{updated} products marked as inactive.")

    mark_as_inactive.short_description = "Mark selected products as inactive"

    class Media:
        css = {"all": ("admin/css/custom_admin.css",)}
        js = ("admin/js/custom_admin.js",)



admin.site.register(ProductCategory, ProductCategoryAdmin)


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):


    list_display = ["code", "percentage", "created_at"]
    search_fields = ["code"]
    list_filter = ["created_at", "percentage"]
    ordering = ["-created_at"]

    fieldsets = (
        ("Code Information", {"fields": ("code", "percentage")}),
        ("Timestamps", {"fields": ("created_at",), "classes": ("collapse",)}),
    )

    readonly_fields = ["created_at"]


class UserProfileAdmin(admin.ModelAdmin):


    list_display = ["user", "phone_number", "created_at"]

    list_filter = ["created_at", "country"]

    search_fields = [
        "user__email",
        "user__username",
        "user__first_name",
        "user__last_name",
        "phone_number",
    ]

    ordering = ["-created_at"]

    fieldsets = (
        ("User Information", {"fields": ("user",)}),
        ("Personal Information", {"fields": ("phone_number", "birth_date")}),
        (
            "Address Information",
            {
                "fields": (
                    "street_number",
                    "street_name",
                    "city",
                    "state",
                    "zip_code",
                    "country",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    readonly_fields = ["created_at", "updated_at"]

    def get_full_address(self, obj):
        return obj.get_full_address()

    get_full_address.short_description = "Full Address"

    def delete_model(self, request, obj):
        """When deleting a profile, also delete the associated user"""
        try:
            user = obj.user
            # Delete the user completely (this will cascade to profile)
            user.delete()
            self.message_user(request, f"User {user.email} and their profile have been completely deleted.")
        except Exception as e:
            self.message_user(request, f"Error deleting user: {str(e)}", level=40)

    def delete_queryset(self, request, queryset):
        """When deleting multiple profiles, also delete the associated users"""
        deleted_count = 0
        for profile in queryset:
            try:
                user = profile.user
                user.delete()  # This will cascade to profile
                deleted_count += 1
            except Exception as e:
                self.message_user(request, f"Error deleting user {profile.user.email}: {str(e)}", level=40)
        
        self.message_user(request, f"{deleted_count} users and their profiles have been completely deleted.")



admin.site.register(UserProfile, UserProfileAdmin)


            
class CustomUserAdmin(UserAdmin):


    actions = ["delete_users_completely"]

    def delete_users_completely(self, request, queryset):

        deleted_count = 0
        for user in queryset:
            try:

                try:
                    profile = user.profile
                    profile.delete()
                except ObjectDoesNotExist:
                    pass


                user.delete()
                deleted_count += 1
            except Exception as e:
                self.message_user(
                    request, f"Error deleting user {user.email}: {str(e)}", level=40
                )

        self.message_user(request, f"{deleted_count} users deleted completely.")

    delete_users_completely.short_description = "Delete selected users completely"

    def delete_model(self, request, obj):

        try:

            try:
                profile = obj.profile
                profile.delete()
            except ObjectDoesNotExist:
                pass


            obj.delete()
        except Exception as e:
            self.message_user(request, f"Error deleting user: {str(e)}", level=40)

    def delete_queryset(self, request, queryset):

        for obj in queryset:
            try:

                try:
                    profile = obj.profile
                    profile.delete()
                except ObjectDoesNotExist:
                    pass


                obj.delete()
            except Exception as e:
                self.message_user(
                    request, f"Error deleting user {obj.email}: {str(e)}", level=40
                )



from django.contrib.auth.models import User

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)



admin.site.site_header = "Raivat Stones Admin"
admin.site.site_title = "Raivat Stones Admin Portal"
admin.site.index_title = "Welcome to Raivat Stones Administration"


@admin.register(UserDiscount)
class UserDiscountAdmin(admin.ModelAdmin):


    list_display = ["user", "discount_code", "percentage", "is_used", "created_at"]
    list_filter = ["is_used", "created_at", "percentage"]
    search_fields = ["user__username", "user__email", "discount_code__code"]
    ordering = ["-created_at"]

    fieldsets = (
        ("User Information", {"fields": ("user",)}),
        ("Discount Information", {"fields": ("discount_code", "percentage")}),
        ("Usage Status", {"fields": ("is_used", "used_at")}),
        ("Timestamps", {"fields": ("created_at",), "classes": ("collapse",)}),
    )

    readonly_fields = ["created_at", "used_at"]

    actions = ["mark_as_used", "mark_as_unused"]

    def mark_as_used(self, request, queryset):

        from django.utils import timezone

        updated = queryset.update(is_used=True, used_at=timezone.now())
        self.message_user(request, f"{updated} discounts marked as used.")

    mark_as_used.short_description = "Mark selected discounts as used"

    def mark_as_unused(self, request, queryset):

        updated = queryset.update(is_used=False, used_at=None)
        self.message_user(request, f"{updated} discounts marked as unused.")

    mark_as_unused.short_description = "Mark selected discounts as unused"


class DiamondProductAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "carat",
        "shape",
        "color",
        "clarity",
        "certification",
        "status",
        "badge",
        "created_at",
        "image_preview",
    ]
    list_filter = ["shape", "color", "clarity", "certification", "status", "badge", "created_at"]
    search_fields = ["name", "description"]
    readonly_fields = ["created_at", "updated_at", "image_preview"]

    fieldsets = (
        (None, {"fields": ("name", "carat", "shape", "color", "clarity", "certification", "image")}),
        ("Status & Badges", {"fields": ("status", "badge")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def image_preview(self, obj):

        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px;" />',
                obj.image.url,
            )
        return "No Image"

    image_preview.short_description = "Image Preview"


admin.site.register(DiamondProduct, DiamondProductAdmin)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "email",
        "amount",
        "payment_id",
        "order_id",
        "status",
        "created_at",
    )
    search_fields = ("user__username", "email", "payment_id", "order_id")
    list_filter = ("status", "created_at")
    ordering = ("-created_at",)
