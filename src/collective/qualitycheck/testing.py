# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.qualitycheck


class CollectiveQualitycheckLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.qualitycheck)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.qualitycheck:default')


COLLECTIVE_QUALITYCHECK_FIXTURE = CollectiveQualitycheckLayer()


COLLECTIVE_QUALITYCHECK_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_QUALITYCHECK_FIXTURE,),
    name='CollectiveQualitycheckLayer:IntegrationTesting',
)


COLLECTIVE_QUALITYCHECK_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_QUALITYCHECK_FIXTURE,),
    name='CollectiveQualitycheckLayer:FunctionalTesting',
)


COLLECTIVE_QUALITYCHECK_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_QUALITYCHECK_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CollectiveQualitycheckLayer:AcceptanceTesting',
)
