from setuptools import setup, find_packages
import sys, os

version = '1.2.1'
shortdesc = \
"Plone Souper Integration: Container for many lightweight queryable Records"
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'CHANGES.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'LICENSE.rst')).read()

setup(name='souper.plone',
      version=version,
      description=shortdesc,
      long_description=longdesc,
      classifiers=[
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
            'Framework :: Zope2',
            'Framework :: Plone :: 4.1',
            'Framework :: Plone :: 4.2',
            'Framework :: Plone :: 4.3',
            'Framework :: Plone :: 5.0',
            'Framework :: Plone :: 5.1',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries :: Python Modules'
      ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='container data record catalog',
      author='BlueDynamics Alliance',
      author_email='dev@bluedynamics.com',
      url='http://pypi.python.org/pypi/souper.plone',
      license='BSD',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['souper'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.CMFPlone',
          'souper',
      ],
      extras_require={
          'test': [
              'plone.app.testing',
              'interlude',
              'zopyx.txng3.core',
          ],
      },
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
