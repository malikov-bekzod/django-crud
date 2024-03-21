from django.contrib import admin
from .models import Book,Customer,Booking
from import_export.admin import ImportExportModelAdmin


@admin.register(Book)
class BookAdmin(ImportExportModelAdmin):
    list_display = ["title", "description", "price", "count"]
    list_display_links = ["title", "description", "price", "count"]
    ordering = ["title"]
    search_fields = ["title","description"]

@admin.register(Customer)
class CustomerAdmin(ImportExportModelAdmin):
    list_display = ["first_name","last_name"]
    list_display_links = ["first_name","last_name"]
    ordering = ["first_name"]
    search_fields = ["first_name","last_name"]


@admin.register(Booking)
class BookingAdmin(ImportExportModelAdmin):
    list_display = ["book", "customer", "create_date"]
    list_display_links = ["book", "customer", "create_date"]
    ordering = ["book"]
    search_fields = ["book", "customer"]
