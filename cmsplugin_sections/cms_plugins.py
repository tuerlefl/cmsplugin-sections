# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from cms.models import CMSPlugin
from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase

from .models import SectionBasePluginModel


class SectionContainerPlugin(CMSPluginBase):
    """
    This is the container for all sections.
    """

    allow_children = True
    cache = True
    # TODO: Complete this, or set it in settings.
    # child_classes = ['...']
    model = CMSPlugin
    module = 'Sections'
    name = 'Section Container'
    render_template = 'cmsplugin_sections/section-container.html'
    text_enabled = False

    def get_children(self, instance):
        """
        This builds a dict for each child, containing the child, the next
        child and the previous child. This provides convenient linking between
        the sections.
        """

        children = []

        if instance.child_plugin_instances:
	        for i, child in enumerate(instance.child_plugin_instances):
	            prev_child = None
	            next_child = None

	            if i > 0:
	                prev_child = instance.child_plugin_instances[i-1]

	            if i < len(instance.child_plugin_instances) - 1:
	                next_child = instance.child_plugin_instances[i+1]

	            children.append({
	                'prev': prev_child,
	                'child': child,
	                'next': next_child,
	            })

        return children

    def render(self, context, instance, placeholder):

        section_menu_items = []
        
        if instance.child_plugin_instances:
	        for child in instance.child_plugin_instances:
	            if child.show_in_menu:
	                section_menu_items.append(child)

	        context['children'] = self.get_children(instance)
	        context['sections'] = section_menu_items

        return context

plugin_pool.register_plugin(SectionContainerPlugin)


class BaseSectionPlugin(CMSPluginBase):
    """
    This is a base class for the plugins that make up the sections of the
    front page. It provides common configuration and behavior.
    """

    class Meta:
        abstract = True

    # These properties should NOT be overridden
    parent_classes = ['SectionContainerPlugin', ]
    text_enabled = False

    # These properties CAN be overridden
    cache = True
    model = SectionBasePluginModel
    module = 'Sections'
    render_template = "cmsplugin_sections/section-base.html"

    # These properties MUST be overridden
    name = 'Unnamed Section'


    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['placeholder'] = placeholder
        return context

# NOTE: Don't register this, its abstract and only used for subclassing.


class SectionPlugin(BaseSectionPlugin):
    """
    This is a generic implementation of the BaseSectionPlugin and is more-or-
    less a section-compatible placeholder for generic content.
    """

    cache = True
    allow_children = True
    model = SectionBasePluginModel
    name = 'Section'
    render_template = "cmsplugin_sections/section.html"
    text_enabled = False

plugin_pool.register_plugin(SectionPlugin)
