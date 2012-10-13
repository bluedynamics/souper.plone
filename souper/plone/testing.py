from plone.testing import z2
from plone.app.testing import (
    PloneSandboxLayer,
    PLONE_INTEGRATION_TESTING,
    IntegrationTesting,
    TEST_USER_NAME,
    TEST_USER_ID,
    login,
    setRoles,
)


class SoupFixture(PloneSandboxLayer):
    defaultBases = (PLONE_INTEGRATION_TESTING,)

    def setUpZope(self, app, configurationContext):
        import zopyx.txng3.core
        import souper.plone
        self.loadZCML(package=zopyx.txng3.core)
        self.loadZCML(package=souper.plone)
        self.loadZCML(package=souper.plone.tests)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'souper.plone:default')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

    def tearDownZope(self, app):
        pass


SOUP_FIXTURE = SoupFixture()
SOUP_INTEGRATION_TESTING = IntegrationTesting(bases=(SOUP_FIXTURE,),
                                              name="SoupFixture:Integration")
