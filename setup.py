from setuptools import setup, find_packages

PACKAGE_NAME = 'watched'

setup(
    name='watched',
    version='1.0.0',
    platforms='all',
    packages=find_packages(exclude=['tests']),
    package_data={
      f'{PACKAGE_NAME}.storage.db': ['alembic.ini', 'alembic/*',
                                     'alembic/versions/*']
    },
    entry_points={
        'console_scripts': [
            '{0}-api = {0}.app.__main__:main'.format(PACKAGE_NAME),
            '{0}-db = {0}.storage.db.__main__:main'.format(PACKAGE_NAME)
        ]
    },
    python_requires='>=3.10'
)
