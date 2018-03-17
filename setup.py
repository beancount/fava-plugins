from os import path
from setuptools import find_packages, setup


with open(path.join(path.dirname(__file__), 'README.md')) as readme:
    LONG_DESCRIPTION = readme.read()


setup(
    name='fava-plugins',
    version='1.0',
    description='A collection of Beancount plugins.',
    long_description=LONG_DESCRIPTION,
    url='https://github.com/beancount/fava-plugins',
    author='Jakob Schnitzer',
    author_email='mail@jakobschnitzer.de',
    license='MIT',
    keywords='fava beancount accounting',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=[
        'beancount>=2.0rc1',
    ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: JavaScript',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Office/Business :: Financial :: Accounting',
        'Topic :: Office/Business :: Financial :: Investment',
    ],
)
