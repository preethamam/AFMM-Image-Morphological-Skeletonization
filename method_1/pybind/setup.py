from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import platform
import pybind11
import numpy

class CustomBuildExt(build_ext):
    """Custom build extension for handling compiler flags"""
    def build_extensions(self):
        compiler_type = self.compiler.compiler_type

        for ext in self.extensions:
            if compiler_type == 'msvc':
                ext.extra_compile_args = [
                    '/O2', '/W3', '/GL', '/EHsc', '/std:c++17',
                ]
                ext.extra_link_args = ['/LTCG']
                ext.define_macros.append(('WIN32', '1'))
            else:  # gcc, mingw, clang
                ext.extra_compile_args = [
                    '-O3', '-Wall', '-Wextra', '-std=c++17',
                    '-fvisibility=hidden', '-fPIC',
                ]
                ext.extra_link_args = ['-lpthread', '-lm']
                if platform.system() == 'Darwin':
                    ext.extra_compile_args.append('-stdlib=libc++')
                    ext.extra_link_args.append('-stdlib=libc++')

        build_ext.build_extensions(self)

# Define source files
sources = [
    'pybind_skelgrad.cpp',  # Your PyBind11 wrapper (C++)
    'skeletongrad.c',             # Original AFMM implementation (C)
]

# Define include directories
include_dirs = [
    '.',
    pybind11.get_include(),
    pybind11.get_include(user=True),
    numpy.get_include(),
]

# Define macros
define_macros = [
    ('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION'),
]

# Extension module
ext_modules = [
    Extension(
        'pyskelgrad',
        sources=sources,
        include_dirs=include_dirs,
        define_macros=define_macros,
        language='c++',  # Still use c++ as the main language for pybind11
    ),
]

setup(
    name='pyskelgrad',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='Python bindings for AFMM Skeletonization',
    long_description='',
    ext_modules=ext_modules,
    cmdclass={'build_ext': CustomBuildExt},
    zip_safe=False,
    python_requires='>=3.6',
    setup_requires=['pybind11>=2.5.0'],
    install_requires=[
        'numpy>=1.13.0',
        'pillow',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Programming Language :: C++',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Image Processing',
    ],
)