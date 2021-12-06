
from setuptools import setup, find_packages
from cli_toolkit import __version__

setup(
    name='cli-toolkit',
    keywords='shell command utility cli config tools',
    description='Classes to implement CLI commands in python',
    author='Ilkka Tuohela',
    author_email='hile@iki.fi',
    url='https://github.com/hile/cli-toolkit',
    version=__version__,
    license='PSF',
    python_requires='>3.6.0',
    packages=find_packages(),
    install_requires=(
        'setproctitle>=1.2.2',
        'sys-toolkit==1.1.1',
    ),
    entry_points={
        'pytest11': [
            'cli_toolkit_fixtures=cli_toolkit.fixtures',
        ]
    },
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3',
        'Topic :: System',
    ],
)
