import setuptools
from reactive import __version__, __tag__

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ReactivePy",
    version="{}{}".format(__version__, __tag__) if __tag__ else __version__,
    author="Dan6erbond",
    author_email="moravrav@gmail.com",
    description="Reactive properties and owners for Python classes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dan6erbond/ReactivePy",
    packages=setuptools.find_packages(include=['reactive', 'reactive.*']),
    keywords="reactive python",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Education",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Typing :: Typed"
    ],
    license="GNU General Public License v3 (GPLv3)",
    python_requires='>=3.6',
)

# classifiers can be found here: https://pypi.org/classifiers/
