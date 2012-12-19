from plone.dexterity.interfaces import IDexterityContent
import xmlrpclib

from DateTime import DateTime
from OFS.Image import File
from zope.component import adapts, getUtility
from zope.interface import implements
from zope.event import notify

from Products.ATContentTypes.interface.topic import IATTopic
from Products.Archetypes.BaseUnit import BaseUnit
from Products.Archetypes.interfaces import IBaseFolder, IBaseObject
from Products.Archetypes.event import ObjectInitializedEvent

# from interfaces import IService, IServiceContainer
from wsapi4plone.core.interfaces import IFormatQueryResults
from wsapi4plone.core.services import PloneService, PloneServiceContainer
from plone.dexterity.interfaces import IDexterityContent


class DexterityObjectService(PloneService):
    adapts(IDexterityContent)

    def set_properties(self, params):
        for par in params:
            if isinstance(params[par], xmlrpclib.DateTime):
                params[par] = DateTime(params[par].value)
            elif isinstance(params[par], xmlrpclib.Binary):
                params[par] = params[par].data
            # elif isinstance(self.context[attr], BaseUnit):
            #     self.context[par].update(params[par], self.context[par])
            #     del params[par]
        self.context.update(**params)
