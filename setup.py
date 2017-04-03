import codecs
import os
import sys
from setuptools import setup, find_packages

# cx_Freeze: dependencies are automatically detected, but it might need
# fine tuning.
kwargs = {}
try:
    from cx_Freeze import setup, Executable
except:
    pass
else:
    build_options = {
        'include_files': [],
        'packages': ['os'],
        'excludes': ['tkinter', 'redis', 'lxml'],
        'optimize': 1,
    }
    base = 'Win32GUI' if sys.platform == 'win32' else None

    kwargs['executables'] = [
        Executable(
            'src/qturtle_app/__main__.py',
            base=base,
            targetName='QTurtle.exe' if sys.platform == 'win32' else 'qturtle',
            shortcutName='QTurtle',
            shortcutDir='DesktopFolder',
        )
    ]
    kwargs['options'] = {'build_exe': build_options}

# Save version and author to __meta__.py
version = open('VERSION').read().strip()
dirname = os.path.dirname(__file__)
path = os.path.join(dirname, 'src', 'qturtle', '__meta__.py')
meta = '''# Automatically created. Please do not edit.
__version__ = '%s'
__author__ = 'F\\xe1bio Mac\\xeado Mendes'
''' % version
with open(path, 'w') as F:
    F.write(meta)

setup(
    # Basic info
    name='qturtle',
    version=version,
    author='Fábio Macêdo Mendes',
    author_email='fabiomacedomendes@gmail.com',
    url='',
    description='Python turtle graphics in Qt.',
    long_description=codecs.open('README.rst', 'rb', 'utf8').read(),

    # Classifiers (see https://pypi.python.org/pypi?%3Aaction=list_classifiers)
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
    ],

    # Packages and dependencies
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        # 'pyqt5',
        # 'pyqode.python',
        'transpyler',
    ],
    extras_require={
        'dev': [
            'python-boilerplate[dev]',
            'pytest',
            'pytest-qt',
        ],
    },

    # Entry points
    entry_points={
        'console_scripts': [
            'qturtle = qturtle_app.__main__:start_application',
        ]
    },

    # Other configurations
    zip_safe=False,
    platforms='any',
    **kwargs
)
