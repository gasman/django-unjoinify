import os
from distutils.core import setup

root_dir = os.path.dirname(__file__)
if not root_dir:
    root_dir = '.'
long_desc = open(root_dir + '/README').read()

setup(
	name='django-unjoinify',
	version='0.1.0',
	description='A helper for efficiently retrieving deeply-nested data sets',
	url='https://github.com/gasman/django-unjoinify',
	author='Matt Westcott',
	author_email='matt@west.co.tt',
	packages=['unjoinify'],
	classifiers=[
		'Development Status :: 4 - Beta',
		'Environment :: Web Environment',
		'Framework :: Django',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: BSD License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Topic :: Software Development :: Libraries :: Python Modules',
	],
	license = 'BSD',
	long_description=long_desc
)