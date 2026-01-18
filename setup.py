from setuptools import setup, find_packages

setup(
    name="data-ingestion-item-taluithai",
    version="0.1.0",
    description="Data ingestion system for TAT (Tourism Authority of Thailand) item tower data",
    author="Taluithai Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "pydantic>=2.0.0",
        "pandas>=2.0.0",
        "python-dotenv>=1.0.0",
        "pyarrow>=14.0.0",
        "aiohttp>=3.9.0",
    ],
)
