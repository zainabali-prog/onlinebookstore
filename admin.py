from django.contrib import admin
from .models import *


class BookInline(admin.TabularInline):
    model=Book

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('author_id','last_name', 'first_name', 'bio_data')
    fields = ['first_name', 'last_name', 'bio_data']
    inlines=[BookInline]
admin.site.register(Author, AuthorAdmin)

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'PublYear' )
    inlines = [BooksInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'book_id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book','imprint', 'book_id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )




admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Ratings)
admin.site.register(Purchase)
admin.site.register(CompletedOrders)
admin.site.register(ActiveOrders)
admin.site.register(HardBookOrders)
admin.site.register(Orders)
admin.site.register(SoldOut)
admin.site.register(InStock)
admin.site.register(Likes)

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(ShippingAddress)
admin.site.register(OrderItem)