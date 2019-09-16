from plone.app.testing import (
    PloneSandboxLayer,
    IntegrationTesting,
    TEST_USER_NAME,
    TEST_USER_ID,
    login,
    setRoles,
)

try:
    from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
except ImportError:
    from plone.app.testing import PLONE_FIXTURE


class SoupFixture(PloneSandboxLayer):

    try:
        defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)
    except:
        defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):

        try:
            import zopyx.txng3.core
            self.loadZCML(package=zopyx.txng3.core)
        except:
            pass
        import souper.plone
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
