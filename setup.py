from setuptools import setup, find_packages

setup(
    name="dbt-wap-addon",
    version="0.1.0",
    packages=find_packages(),  # This finds all packages with __init__.py
    include_package_data=True,
    install_requires=[
        "dbt-core>=1.5.0",
        "dbt-duckdb>=1.5.0",
    ],
    entry_points={
        "console_scripts": [
            "dbta=addons.cli.cli:main",
        ],
    },
    python_requires=">=3.8",
)
