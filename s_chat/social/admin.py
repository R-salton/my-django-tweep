from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Tweep #UserToken

# Unregister user

admin.site.unregister(Group)

class ProfileInline(admin.StackedInline):
    model = Profile
# extends USer MOdel

# Combine User and Profile
class UserAdmin(admin.ModelAdmin):
    model = User

    # Display USer Fields
    fields = ["username"]
    inlines = [ProfileInline]


# Register User Tokens in Admin pannel

# class UserTokensAdmin(admin.ModelAdmin):
#     model : UserToken
#     fields : ["usser","access_token","refresh_token"]

# admin.site.register(UserToken,UserTokensAdmin)
# unregister user Initial User
admin.site.unregister(User)
# Register user and pr eofile

admin.site.register(User, UserAdmin)
# admin.site.register(Profile)

# Register post( tweeps)


admin.site.register(Tweep)
