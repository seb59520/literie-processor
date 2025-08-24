#!/usr/bin/env python3
"""
Setup script pour créer un package Python installable
Application Matelas Processor - Traitement automatisé de commandes matelas
"""

from setuptools import setup, find_packages
import os

# Lire le README
def read_readme():
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return "Application de traitement automatisé de commandes matelas"

# Lire les requirements
def read_requirements():
    try:
        with open("requirements_gui.txt", "r", encoding="utf-8") as fh:
            return [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        return [
            "PyQt6>=6.4.0",
            "PyMuPDF>=1.23.0", 
            "openpyxl>=3.1.0",
            "httpx>=0.24.0",
            "psutil>=5.9.0",
            "cryptography>=41.0.0",
            "requests>=2.31.0",
            "pandas>=2.0.0",
            "numpy>=1.24.0",
            "Pillow>=10.0.0"
        ]

setup(
    name="matelas-processor",
    version="1.0.0",
    author="Matelas Processor Team",
    author_email="contact@matelas-processor.com",
    description="Application professionnelle de traitement automatisé de commandes matelas",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/matelas-processor/matelas-processor",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Manufacturing",
        "Topic :: Office/Business :: Financial :: Accounting",
        "Topic :: Office/Business :: Scheduling",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Environment :: X11 Applications :: Qt",
        "Environment :: Win32 (MS Windows)",
        "Framework :: PyQt",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-benchmark>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "gui": [
            "PyQt6>=6.4.0",
            "Pillow>=10.0.0",
        ],
        "security": [
            "cryptography>=41.0.0",
        ],
        "full": [
            "pandas>=2.0.0",
            "numpy>=1.24.0",
            "requests>=2.31.0",
            "httpx>=0.24.0",
            "colorlog>=6.7.0",
            "jsonschema>=4.17.0",
            "pydantic>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "matelas-processor=run_gui:main",
            "matelas-cli=backend_interface:main",
        ],
        "gui_scripts": [
            "matelas-processor-gui=run_gui:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": [
            "template/*.xlsx",
            "backend/*.py",
            "backend/Référentiels/*.json",
            "backend/Référentiels/*.csv",
            "config.py",
            "*.md",
            "*.txt",
            "*.html",
        ],
    },
    data_files=[
        ("template", [
            "template/template_matelas.xlsx", 
            "template/template_sommier.xlsx"
        ]),
        ("backend/Référentiels", [
            "backend/Référentiels/7z_dimensions_matelas.json",
            "backend/Référentiels/7z_longueurs_matelas.json",
            "backend/Référentiels/dimensions_matelas.csv",
            "backend/Référentiels/dimensions_matelas.json",
            "backend/Référentiels/latex_mixte7zones_longueur_housse.json",
            "backend/Référentiels/latex_mixte7zones_tencel_luxe3d_tencel_polyester.json",
            "backend/Référentiels/latex_naturel_longueur_housse.json",
            "backend/Référentiels/latex_naturel_tencel_luxe3d_tencel_polyester.json",
            "backend/Référentiels/latex_renforce_longueur_housse.json",
            "backend/Référentiels/latex_renforce_tencel_luxe3d_tencel_polyester.json",
            "backend/Référentiels/longueurs_matelas.csv",
            "backend/Référentiels/longueurs_matelas.json",
            "backend/Référentiels/mousse_rainuree7zones_longueur_housse.json",
            "backend/Référentiels/mousse_rainuree7zones_tencel_luxe3d_tencel_polyester.json",
            "backend/Référentiels/mousse_visco_dimensions_matelas_longueur.json",
            "backend/Référentiels/mousse_visco_dimensions_matelas.json",
            "backend/Référentiels/mousse_visco_longueur_tencel.json",
            "backend/Référentiels/mousse_visco_tencel.json",
            "backend/Référentiels/regles_matelas.csv",
            "backend/Référentiels/s43_dimensions_matelas.json",
            "backend/Référentiels/s43_longueurs_matelas.json",
            "backend/Référentiels/select43_longueur_housse.json",
            "backend/Référentiels/select43_tencel_luxe3d_tencel_polyester.json",
        ]),
        ("", [
            "config.py", 
            "README.md",
            "EULA.txt",
            "GUIDE_INSTALLATION.md",
            "STOCKAGE_SECURISE_API.md",
            "CENTRAGE_EXCEL.md",
        ]),
        ("tests", [
            "tests/__init__.py",
            "tests/test_*.py",
            "tests/requirements.txt",
            "tests/run_tests.py",
        ]),
    ],
    keywords=[
        "matelas", "commandes", "excel", "pdf", "traitement", "automatisation",
        "manufacturing", "business", "accounting", "scheduling", "analysis",
        "latex", "mousse", "viscoelastique", "literie", "meubles"
    ],
    project_urls={
        "Bug Reports": "https://github.com/matelas-processor/matelas-processor/issues",
        "Source": "https://github.com/matelas-processor/matelas-processor",
        "Documentation": "https://github.com/matelas-processor/matelas-processor/wiki",
        "Changelog": "https://github.com/matelas-processor/matelas-processor/blob/main/CHANGELOG.md",
    },
    zip_safe=False,
) 