from setuptools import setup

setup(
    name='python-bot-utils',
    version='0.0.2',
    author='vero4ka',
    packages=['python_bot_utils'],
    description='Helper methods to build python bots for Telegram and Facebook.',
    long_description=open('README.md').read(),
    install_requires=[
        "requests >= 2.13.0",
        "emoji >= 0.4.5",
    ],
)
