from setuptools import setup, find_packages

setup(
    name="dbt-addons",
    version="0.0.2",
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
