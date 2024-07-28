import setuptools
from pip._internal.network.session import PipSession
from pip._internal.req import parse_requirements
from os import path

__version__ = '0.0.1'
here = path.abspath(path.dirname(__file__))

# get the dependencies and installs
# parse_requirements() returns generator of pip._internal.req.req_file.ParsedRequirement objects
session = PipSession()
install_reqs = parse_requirements('requirements.txt', session=session)

# reqs is a list of requirement
try:
    reqs = [str(ir.req) for ir in install_reqs]
except:
    reqs = [str(ir.requirement) for ir in install_reqs]


reqs.append('LSCDetection @ git+https://git@github.com/pierluigic/LSCDetection.git')
reqs.append('WordTransformer @ git+https://git@github.com/pierluigic/xl-lexeme.git')
reqs.append('dload')
reqs.append('scipy==1.11.4')
reqs.append('scikit-learn==1.3.2')

setuptools.setup(
    name="languagechange",
    version=__version__,
    author="Change is Key!",
    description="Python Library for Language Change",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/pierluigic/languagechange",
    packages=setuptools.find_packages(),
    platforms=['all'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=reqs
)