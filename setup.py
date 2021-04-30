import os
from setuptools import setup

this_directory = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

about = {}
with open(os.path.join(this_directory, 'ScanWatch/__init__.py'), encoding='utf-8') as f:
    exec(f.read(), about)

setup(
    name='ScanWatch',
    version=about['__version__'],
    packages=['ScanWatch', 'ScanWatch.storage', 'ScanWatch.utils'],
    url='https://github.com/EtWnn/ScanWatch',
    author='EtWnn',
    author_email='',
    license='MIT',
    description='Local tracker of an eth address for ETH and BSC scan',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    install_requires=['requests', 'appdirs'],
    keywords='eth bsc wallet save tracking history ethereum tracker binance smartchain smart chain',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
