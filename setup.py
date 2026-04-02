from setuptools import setup, find_packages

setup(
    name='ltfeditor',
    version='0.1.0',
    description='A tool for editing LTF files',
    author='Gubir34',
    author_email='your_email@example.com',  # Replace with your email
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    entry_points={
        'console_scripts': [
            'ltfeditor=ltfeditor.__main__:main',
        ],
    },
    install_requires=[
        # List your project's dependencies here
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)