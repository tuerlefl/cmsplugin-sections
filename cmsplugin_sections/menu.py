from menus.base import NavigationNode
from menus.base import Modifier
from menus.menu_pool import menu_pool
from django.utils.translation import ugettext_lazy as _
from cms.menu_bases import CMSAttachMenu

from .models import *

class SectionMenu(CMSAttachMenu):

    name = _("section_menu")

    def get_nodes(self, request):
        nodes = []
        i=0

        for child in SectionBasePluginModel.objects.filter(show_in_menu=True):

            i=i+1

            if child.page.id == self.instance.children.instance.id:
                n = NavigationNode(_(child.section_menu_label), '%s#%s' %(child.page.get_absolute_url(), child.section_menu_slug), i)

                nodes.append(n)


        return nodes

menu_pool.register_menu(SectionMenu)


class Level(Modifier):
    """
    marks all node levels
    """
    post_cut = True

    def modify(self, request, nodes, namespace, root_id, post_cut, breadcrumb):
        if breadcrumb:
            return nodes
        for node in nodes:
            if not node.parent:
                if post_cut:
                    node.menu_level = 0
                else:
                    node.level = 0
                self.mark_levels(node, post_cut)
        return nodes

    def mark_levels(self, node, post_cut):
        for child in node.children:
            if post_cut:
                child.menu_level = node.menu_level + 1
            else:
                child.level = node.level + 1
            self.mark_levels(child, post_cut)

menu_pool.register_modifier(Level)