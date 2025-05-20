from setuptools import setup, find_packages

setup(
    name='myna',
    version='0.1.0',
    description='A customizable and alias-based translation Python shell interface',
    author='Alexis Bernard',
    author_email='alexisbrnad@gmail.com',
    url='https://github.com/itsal3xis/myna',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'myna = myna.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
)
