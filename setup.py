from setuptools import setup, find_packages

setup(
    name="recaptchav2solver",
    version="1.1.2",
    author="Lucas Soares",
    author_email="lucasjs.eng@gmail.com",
    description="A Python package to solve reCAPTCHA audio challenges using Selenium and SpeechRecognition",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/lucassoares-eng/python-recaptchav2solver",
    packages=find_packages(),
    install_requires=[
        "requests==2.31.0",
        "selenium==4.27.1",
        "speechrecognition==3.14.0",
        "pydub==0.25.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
