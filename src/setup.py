from setuptools import setup, find_packages
import sys, os

version = ''

setup(name='feedvalidator',
      version=version,
      description="Validator for feeds",
      long_description= \
      """Feedvalidator validates feeds in a variety of syndication formats.
      """,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='syndication atom rdf rss feeds',
      author='Sam Ruby',
      url='http://feedvalidator.org/',
      license='MIT',
      packages=['feedvalidator', 'feedvalidator.i18n', 'feedvalidator.formatter'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'setuptools',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
