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
        return user


    def post_user(self, params):
        pass
