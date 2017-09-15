import codecs
import os
import sys
from setuptools import setup, find_packages


# cx_Freeze: we added a undocumented option to enable building frozen versions
# of our packages. This should be refactored for a more safe approach in the
# future.
setup_kwargs = {}
if '--cx-freeze' in sys.argv:
    from cx_Freeze import setup, Executable

    build_options = {
        'include_files': [],
        'packages': ['os', 'pygments', 'PyQt5', 'PyQt5.Qsci'],
        'excludes': [
            'tkinter', 'redis', 'lxml',
            'qturtle.qsci.widgets',
            'nltk', 'textblob',
            'matplotlib', 'scipy', 'numpy', 'sklearn',
            'notebook',
            'java',
            'sphinx', 'PIL', 'PyQt4'
        ],
        'optimize': 1,
    }
    base = 'Win32GUI' if sys.platform == 'win32' else None

    setup_kwargs['executables'] = [
        Executable(
            'src/qturtle_app/__main__.py',
            base=base,
            targetName='QTurtle.exe' if sys.platform == 'win32' else 'qturtle',
            shortcutName='QTurtle',
            shortcutDir='DesktopFolder',
        )
    ]
    setup_kwargs['options'] = {'build_exe': build_options}
    sys.argv.remove('--cx-freeze')


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


# Check if Qt packages need to be installed
qt_packages = []
try:
    import PyQt5
except ImportError:
    qt_packages.append('PyQt5')
try:
    import PyQt5.Qsci
except ImportError:
    print('please install python3-pyqt5.qsci package')
    qt_packages.append('QScintilla')


setup(
    # Basic info
    name='qturtle',
    version=version,
    author='Fábio Macêdo Mendes',
    author_email='fabiomacedomendes@gmail.com',
    url='https://github.com/transpyler/qturtle',
    description='Python turtle graphics in Qt.',
    long_description=codecs.open('README.rst', 'rb', 'utf8').read(),

    # Classifiers (see https://pypi.python.org/pypi?%3Aaction=list_classifiers)
    classifiers=[
        'Development Status :: 4 - Beta',
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

    # Package data
    package_data={
        'qturtle': [
            'data/*.*',
            'data/examples/*.*',
            'doc/*.*'
        ],
    },

    # Packages and dependencies
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=qt_packages + [
        'transpyler>=0.4.0',
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
            'qturtle = qturtle.__main__:start_application',
        ]
    },

    # Other configurations
    zip_safe=False,
    platforms='any',
    **setup_kwargs
)
