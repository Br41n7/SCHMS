"""
Wagtail CMS models for content pages.
Extensible for future features like timetables, online learning, etc.
"""
from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index


class HomePage(Page):
    """
    Home page model for the school portal.
    Can be extended with additional fields as needed.
    """
    
    body = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
    
    class Meta:
        verbose_name = "Home Page"


class ContentPage(Page):
    """
    Generic content page for information pages.
    Can be used for About, Contact, Policies, etc.
    """
    
    body = RichTextField(blank=True)
    
    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]
    
    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
    
    class Meta:
        verbose_name = "Content Page"


class TimetablePage(Page):
    """
    Placeholder for future timetable functionality.
    Can be extended to display class schedules, exam timetables, etc.
    """
    
    introduction = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
    ]
    
    class Meta:
        verbose_name = "Timetable Page"


class OnlineLearningPage(Page):
    """
    Placeholder for future online learning functionality.
    Can be extended to integrate with LMS, course materials, etc.
    """
    
    introduction = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
    ]
    
    class Meta:
        verbose_name = "Online Learning Page"