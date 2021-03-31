import os
from setuptools import setup

this_directory = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

about = {}
with open(os.path.join(this_directory, 'ETHWatch/__init__.py'), encoding='utf-8') as f:
    exec(f.read(), about)

setup(
    name='ETHWatch',
    version=about['__version__'],
    packages=['ETHWatch'],
    url='https://github.com/EtWnn/ETHWatch',
    author='EtWnn',
    author_email='',
    license='MIT',
    description='Local tracker of an address',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    install_requires=['requests'],
    keywords='eth wallet save tracking history ethereum tracker',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)