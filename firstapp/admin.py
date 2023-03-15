from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Cart, Product, ProductInCart, Order, Deal, Customer, Seller, Contact, SellerAdditional
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from django.contrib.sessions.models import Session
import pprint


# Register your models here.


class SellerAdditionalInLine(admin.TabularInline):
    model = SellerAdditional


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'type')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'type', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)


class SellerAdmin(admin.ModelAdmin):
    inlines = (
        SellerAdditionalInLine,
    )


# admin.site.unregister(User)
admin.site.register(CustomUser, CustomUserAdmin)


class ProductInCartInline(admin.TabularInline):
    model = ProductInCart


class CartInline(admin.TabularInline):
    model = Cart


class DealInline(admin.TabularInline):
    model = Deal.user.through


# class UserAdmin(UserAdmin):
#     model = User
#     list_display = ('username', 'get_cart', 'is_staff', 'is_active',)
#     list_filter = ('username', 'is_staff', 'is_active')
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         ('Permissions', {'fields': ('is_staff', ('is_active', 'is_superuser'),)}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#         ('Advanced options', {
#             'classes': ('collapse',),
#             'fields': ('groups', 'user_permissions'),
#         }),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser', 'groups')}
#          ),
#     )
#     inlines = [
#         CartInline, DealInline
#     ]
#
#     def get_cart(self, obj):
#         return obj.cart
#
#     search_fields = ('username',)
#     ordering = ('username',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_display = ('staff', 'user', 'created_on',)
    list_filter = ('user', 'created_on',)
    fieldsets = (
        (None, {'fields': ('user', 'created_on',)}),

    )
    inlines = (
        ProductInCartInline,
    )

    def staff(self, obj):
        return obj.user.is_staff

    staff.admin_order_field = 'user__is_staff'
    staff.short_description = 'Staff User'

    list_filter = ['user__is_staff', 'created_on']
    search_fields = ['user__username']


class DealAdmin(admin.ModelAdmin):
    inlines = [
        DealInline,
    ]
    exclude = ('user',)


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return pprint.pformat(obj.get_decoded()).replace('\n', '<br>\n')

    _session_data.allow_tags = True
    list_display = ['session_key', '_session_data', 'expire_date']
    readonly_fields = ['_session_data']
    exclude = ['session_data']


admin.site.register(Session, SessionAdmin)

# admin.site.register(Cart)
admin.site.register(Product)
admin.site.register(ProductInCart)
admin.site.register(Order)
# admin.site.register(Deal, DealAdmin)
admin.site.register(Deal)
admin.site.register(Customer)
admin.site.register(Seller, SellerAdmin)
admin.site.register(Contact)
# admin.site.register(Session)
admin.site.register(SellerAdditional)
