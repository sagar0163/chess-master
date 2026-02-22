from setuptools import setup, find_packages

setup(
    name='chess-master',
    version='1.0.0',
    description='Expert-level chess game with AI opponent',
    author='Sagar',
    packages=find_packages(),
    install_requires=[
        'chess>=1.0.0',
    ],
    entry_points={
        'console_scripts': [
            'chess=main:main',
        ],
    },
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Games/Entertainment :: Board Games',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
