from setuptools import setup

setup_args = dict(
    name='GameMaster',
    install_requires=[
        # web framework
        'Flask>=0.9',
        "Flask-PyMongo==0.2.0",
        'Flask-Login>=0.2.7',
        'flask-mongoengine==0.7.0',
        'pymongo==2.8.0',
        'mongoengine==0.8.6',
        'blinker>=0.0.0',
        'bcrypt>=0.0.0',
        # timezone
        'pytz>=0.0.0',
        'functools32>=0.0.0',
        'fake-factory>=0.4.0',
        'passlib>=1.6.1',
        'Flask-HTTPAuth>=2.2.0',
        # Oauth
        'itsdangerous>=0.23',
        # For test
        'requests>=1.1.0',
        # Image Storage
        'qiniu>=0.0.0',
    ],
    entry_points=dict(
        console_scripts=[
            ],
    ),
)

if __name__ == '__main__':
    setup(**setup_args)
