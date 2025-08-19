from django.contrib import admin
from .models import BlogPost
from .models import Project, Feature, SampleImage

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    search_fields = ('title', 'author')
    list_filter = ('published_date',)

class FeatureInline(admin.TabularInline):
    model = Feature
    extra = 1

class SampleImageInline(admin.TabularInline):
    model = SampleImage
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    inlines = [FeatureInline, SampleImageInline]

admin.site.register(Feature)
admin.site.register(SampleImage)
admin.site.register(BlogPost, BlogPostAdmin)

