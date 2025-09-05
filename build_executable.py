#!/usr/bin/env python3
"""
Script de création d'exécutable optimisé avec PyInstaller
"""

import PyInstaller.__main__
import sys
import os

def build_executable():
    """Crée l'exécutable avec PyInstaller"""
    
    PyInstaller.__main__.run([
        'app_gui.py',
        '--name=MatelasApp',
        '--onefile',
        '--windowed',  # Pas de console
        '--icon=assets/lit-double.ico',
        '--add-data=backend;backend',
        '--add-data=config;config', 
        '--add-data=template;template',
        '--add-data=assets;assets',
        '--add-data=matelas_config.json;.',
        '--exclude-module=matplotlib',
        '--exclude-module=pandas',
        '--exclude-module=numpy',
        '--exclude-module=scipy',
        '--exclude-module=PIL',
        '--clean',
        '--noconfirm',
    ])
    
    print("\n🚀 Exécutable créé dans le dossier dist/")

if __name__ == "__main__":
    build_executable()
