from setuptools import setup

setup_args = dict(
    name='GameMaster',
    install_requires=[
    # web framework
    'Flask>=0.9',
    'Flask-Login>=0.2.7',
    "flask-mongoengine>=0.7.0",
    # database
    'pymongo>=2.6.3',
    'mongoengine>=0.8.6',
    'Flask-WTF>=0.9.4',
    'flask-debugtoolbar>=0.0.0',
    # 'gevent>=0.13.8',

    # timezone
    'pytz>=0.0.0',

    # tool
    'sphinx>=1.1.3',
    'pep8>=1.5.6',
    'pinyin>=0.1.2',

    # 'termcolor>=1.1.0',
    'requests>=2.1.0',

    'fake-factory>=0.4.0',
    'python-dateutil<2.0.0',
    'recordtype>=0.0.0',
    'bpython>=0.0.0',
    'passlib>=0.0.0',
    'py-bcrypt>=0.0.0',

    'Flask-Mobility>=0.0.0',
    'functools32>=0.0.0',

    'IPython>=0.0.0'
    ],
    entry_points=dict(
        console_scripts=[
            ],
    ),
)

if __name__ == '__main__':
    setup(**setup_args)
