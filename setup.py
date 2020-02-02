from setuptools import setup

setup(
    name="cooar-cli",
    version="0.0.1",
    description="",
    url="https://github.com/chrisWhyTea/cooar-cli",
    author="Christopher Schmitt",
    author_email="cooar@chris.yt",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD 3-Clause License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.7,<4",
    install_requires=["click", "arrow", "jinja2", "colorama"],
    py_modules=["cooar_cli"],
    # entry_points={"console_scripts": ["cooar=cooar_cli:cli",],},
)
