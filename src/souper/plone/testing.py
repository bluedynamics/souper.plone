from plone.testing import z2
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting

class SoupFixture(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import zopyx.txng3.core
        import souper.plone
        self.loadZCML(package=zopyx.txng3.core)
        self.loadZCML(package=souper.plone)
        self.loadZCML(package=souper.plone.tests)
        z2.installProduct(app, 'souper.plone')

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'souper.plone:default')

    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'souper.plone')


SOUP_FIXTURE = SoupFixture()
SOUP_INTEGRATION_TESTING = IntegrationTesting(bases=(SOUP_FIXTURE,),
                                              name="SoupFixture:Integration")
