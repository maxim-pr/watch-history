from setuptools import setup, find_packages

PACKAGE_NAME = 'watched'

setup(
    name='watched-main-service',
    version='1.0.0',
    platforms='all',
    packages=find_packages(include=['watched']),
    entry_points={
        'console_scripts': [
            '{0}-api = {0}.app.app:main'.format(PACKAGE_NAME),
            '{0}-db = {0}.storage.db.__main__:main'.format(PACKAGE_NAME)
        ]
    }
)
