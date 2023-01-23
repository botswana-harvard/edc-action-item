# -*- coding: utf-8 -*-
import os
from setuptools import setup
from setuptools import find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='edc-action-item',
    version='0.1.6',
    author=u'Software Engineering & Data Management',
    author_email='se-dmc@bhp.org.bw',
    packages=find_packages(),
    url='http://github.com/botswana-harvard/edc-action-item',
    license='GPL licence, see LICENCE',
    description='Add subject-related action items to the Edc',
    long_description=README,
    include_package_data=True,
    zip_safe=False,
    keywords='django Edc action items reminders',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
