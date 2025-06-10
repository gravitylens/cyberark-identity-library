from setuptools import setup, find_packages

setup(
    name='cyberark-identity-library',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A library for managing identities in CyberArk.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/cyberark-identity-library',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'python-dotenv',  # Add other dependencies as needed
    ],
)