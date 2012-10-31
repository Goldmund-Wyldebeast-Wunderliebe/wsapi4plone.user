import random

from zope.app.component.hooks import getSite
from zope.component import getUtility
from zope.interface import implements

from wsapi4plone.core.browser.interfaces import IApplicationAPI
from wsapi4plone.core.browser.wsapi import WSAPI
from wsapi4plone.core.interfaces import IScrubber, IService, IServiceContainer
from plone import api


class ApplicationAPI(WSAPI):
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

        api.user.grant_roles(
                username=username,
                roles=roles,
                obj=self.context
                )

        self.logger.info("- grant_user_roles - For user %s, context: %s, roles: %s " % (username, self.context.id, roles))
        return api.user.get_permissions(username=username,obj=self.context)



