from setuptools import setup, find_packages
import os

packages=find_packages()
print packages

setup(
    name='djangospider',
    version='0.11',
    author='alex shu',
    author_email='daxia4444@qq.com',
    description='three ways for spider by python',
    include_package_data=True,
    packages=find_packages(),
    #packages=['monitor','mycrawl'],
    install_requires=[
        'django',
        'tornado>=3.2',
        'Twisted>=10.0.0',
        'beautifulsoup4',
    ],
    
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
    ],


    entry_points={
        'console_scripts': ['djangospider = djangospider.management:execute_from_command_line']
    },
)
