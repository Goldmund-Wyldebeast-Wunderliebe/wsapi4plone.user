import random

from zope.app.component.hooks import getSite
from zope.component import getUtility
from zope.interface import implements

from wsapi4plone.core.browser.interfaces import IApplicationAPI
from wsapi4plone.core.browser.wsapi import WSAPI
from wsapi4plone.core.browser.app import ApplicationAPI as BaseApplicationAPI
from wsapi4plone.core.interfaces import IScrubber, IService, IServiceContainer
from plone import api


class ApplicationAPI(BaseApplicationAPI):
    implements(IApplicationAPI)


    def get_user(self, username):
        user = api.user.get(username=username)
        roles = api.user.get_roles(username=username)
        results = {}


        results['username'] = user.id
        results['fullname'] = user.getProperty('fullname')
        results['email'] = user.getProperty('email')
        results['roles'] = roles
        return results


    def post_user(self, params):


        assert type(params) == dict, "The first agument must be a dictionary."


        properties = {}
        roles=('Member', )
        if params.has_key('fullname'):
            properties['fullname'] = params.get('fullname')
        if params.has_key('location'):
            properties['location'] = params.get('location')
        if params.has_key('roles'):
            roles = params.get('roles')

        assert params.has_key('username'), "Missing username"
        assert params.has_key('email'), "Missing e-mail"

        membercreation = {
                'username':params.get('username'),
                'email':params.get('email'),
                'roles': roles,
                'properties':properties
                }
        try:
            api.user.create(**membercreation)
            self.logger.info("- post_user- Creating user %s " % (params))

            return self.get_user(params.get('username'))
        except Exception, e:
            return e

    def grant_user_roles(self, params):
        assert type(params) == dict, "The first agument must be a dictionary."
        assert params.has_key('roles'), "No roles given to grant"
        assert params.has_key('username'), "No users given to grant to"

        username = params.get('username')
        roles = params.get('roles')
        try:
            api.user.grant_roles(
                    username=username,
                    roles=roles,
                    obj=self.context
                    )

            self.logger.info("- grant_user_roles - For user %s, context: %s, roles: %s " % (username, self.context.id, roles))
            return api.user.get_permissions(username=username,obj=self.context)
        except:
            return 0


class DexterityApplicationAPI(BaseApplicationAPI):
    implements(IApplicationAPI)

    # def get_object(path='', attrs=[]):
    #     """get the raw data from an object (GET)"""

    # def get_file_object(path='', attr=''):
    #     """ """

    # def post_object(params, type_name, path=''):
    #     """
    #     Post or create an object with the name given in path of type.
    #     An 'id' must be given to create an object. The id can either be given
    #     via params or an extention of path (e.g. {'id': 'newid'} or
    #     /folder/subfolder/newid).
    #     The params keys can be made available via a call to get_schema(type="the type").
    #     The type_name parameter is a valid type that can be verified with the
    #     get_types method."""

    # def put_object(params, path=''):
    #     """
    #     Put or set the given params on an object of path or context. The params
    #     keys should map to the values associated with it from the get_object or
    #     get_schema methods. """

    # def delete_object(path=''):
    #     """
    #     Delete the given path or context.
    #     """

    # def get_schema(path='', type=False):
    #     """
    #     Delivers a schema in a dictionary format, where keys are attribute names
    #     and there values are a dictionary of required, type and value information.
    #     e.g.:
        
    #     {'attribute_name':
    #         {'required': (True or False) or (1 or 0)
    #          'type': lines, text, boolean, etc.
    #          'value': ... }, ... }
        
    #     If type is 'True', then no object exists to get a schema from. path in
    #     this case is the type_name. This indicates two functionalities in one method.
    #     """

