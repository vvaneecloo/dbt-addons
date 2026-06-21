from pathlib import Path
from setuptools import setup, find_packages

long_description = (Path(__file__).parent / "README.md").read_text(encoding="utf-8")

setup(
    name="dbt-addons",
    version="0.0.6",
    description="Write-Audit-Publish and other missing dbt patterns",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Victor Vaneecloo",
    author_email="victor.vaneecloo3@gmail.com",
    url="https://github.com/vvaneecloo/dbt-addons",
    project_urls={
        "Documentation": "https://vvaneecloo.github.io/dbt-addons/",
        "Source": "https://github.com/vvaneecloo/dbt-addons",
        "Issues": "https://github.com/vvaneecloo/dbt-addons/issues",
    },
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries",
    ],
    packages=find_packages(),
    package_data={
        "addons": [
            "wap/macros/**/*.sql",
            "wap/macros/*.sql",
            "wap/root_macros/*.sql",
        ],
    },
    install_requires=[
        "dbt-core>=1.5.0",
        "pyyaml>=6.0",
    ],
    extras_require={
        "dev": [
            "dbt-duckdb>=1.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "dbta=addons.cli.cli:main",
        ],
    },
    python_requires=">=3.10",
)
