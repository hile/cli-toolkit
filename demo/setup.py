
from setuptools import setup, find_packages
from cli_toolkit_demo import __version__

setup(
    name='cli-toolkit-demo',
    keywords='shell cli toolkit demo',
    description='Demo python app for cli-toolkit shell commands',
    author='Ilkka Tuohela',
    author_email='hile@iki.fi',
    version=__version__,
    license='PSF',
    python_requires='>3.6.0',
    packages=find_packages(),
    install_requires=(
        'cli-toolkit>=1.0.0',
    ),
    entry_points={
        'console_scripts': [
            'cli-demo=cli_toolkit_demo.bin.cli_demo.main:main',
        ],
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
        'Topic :: System :: Systems Administration',
    ],
)
