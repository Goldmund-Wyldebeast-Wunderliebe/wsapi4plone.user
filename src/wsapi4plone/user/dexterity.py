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
try:
    from wsapi4plone.core.services import PloneService, PloneServiceContainer
except ImportError:
    from wsapi4plone.core.application.services import PloneService, PloneServiceContainer
from plone.dexterity.interfaces import IDexterityContent
from zope.schema import getFieldsInOrder
from plone.behavior.interfaces import IBehaviorAssignable
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import getUtility
from datetime import datetime
from Products.ATContentTypes.utils import DT2dt
from z3c.relationfield.schema import RelationList, RelationChoice

class DexterityObjectService(PloneService):
    adapts(IDexterityContent)

    def set_properties(self, params):
        for par in params:
            if isinstance(params[par], xmlrpclib.DateTime):   
                params[par] = DT2dt(DateTime(params[par].value)).replace(tzinfo=None)                
            elif isinstance(params[par], xmlrpclib.Binary):
                # import pdb; pdb.set_trace()
                params[par] = params[par].data
            elif par == 'creators':
                params[par] = tuple(params[par])
            elif isinstance(params[par], str):
                params[par] = unicode(params[par])
            # elif isinstance(self.context[attr], BaseUnit):
            #     self.context[par].update(params[par], self.context[par])
            #     del params[par]

        context = self.context
        changed = []

        behavior_fields = []
        content_fields = []

        # Stap 1 metadata
        behavior_assignable = IBehaviorAssignable(context)
        if behavior_assignable:
            behaviors = behavior_assignable.enumerateBehaviors()
            for behavior in behaviors:
                behavior_fields += getFieldsInOrder(behavior.interface)

        # Stap 2 eigen velden
        fti = context.getTypeInfo()
        schema = fti.lookupSchema()
        content_fields = getFieldsInOrder(schema)


        fields = behavior_fields
        fields += content_fields

        for k,v in params.items():
            found = False

            for field_info in fields:
                field_name = field_info[0]
                field = field_info[1]
                field_schema = getattr(field, 'schema', None) 
                if field_name == k:
                    if field_schema and field_schema.getName() in ['INamedBlobImage', 'INamedImage']: 
                        found = True
                        setattr(context, field_name, field._type(v)) 
                        changed.append(k)

                    elif type(field) == RelationChoice:
                        context.set_relation(field_name, path=v)

                    elif type(field) == RelationList:
                        value = v
                        if type(value) in [str, unicode] :
                            value = [value,]
                        context.set_relation(field_name, paths=value)
                        
                    else:   
                        found = True
                        field.set(context, v)
                        changed.append(k)
                    # context.plone_log(u'Setting field "{0}"'.format(k))

            # if not found:
            #     context.plone_log(u'Cannot find field "{0}"'.format(k))

        if changed:
            context.reindexObject(idxs=changed)
