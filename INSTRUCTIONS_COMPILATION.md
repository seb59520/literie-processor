# 🎯 Instructions Compilation Exécutable Windows

## 🚀 Méthode Rapide (Recommandée)

### Étape 1 : Installation de PyInstaller
```bash
pip install pyinstaller
```

### Étape 2 : Compilation
```bash
python build_windows.py
```

**C'est tout !** L'exécutable sera créé dans le dossier `dist/`

## 📦 Résultat

Après compilation, vous obtiendrez :
```
dist/
├── MatelasProcessor.exe    # Exécutable Windows (~150-200 MB)
└── install.bat            # Script d'installation Windows
```

## 🎯 Distribution sur Windows

### Option 1 : Installation système
1. Copiez le dossier `dist/` sur la machine Windows
2. Exécutez `install.bat` **en tant qu'administrateur**
3. L'application s'installe dans `C:\Program Files\MatelasProcessor\`
4. Un raccourci est créé sur le bureau

### Option 2 : Mode portable  
1. Copiez simplement `MatelasProcessor.exe` où vous voulez
2. Double-cliquez pour lancer (aucune installation requise)

## ⚠️ Notes Importantes

### Premier lancement
- Le premier démarrage peut prendre **10-30 secondes** (extraction des fichiers)
- Les lancements suivants sont rapides

### Configuration automatique
L'application crée automatiquement ses dossiers :
- Configuration : `%USERPROFILE%\MatelasProcessor\`
- Fichiers Excel : `Documents\MatelasProcessor\`
- Logs : `AppData\Local\MatelasProcessor\logs\`

### Sécurité Windows
- Windows peut afficher un avertissement "Éditeur inconnu"
- Solution : Clic droit → "Exécuter quand même"
- Ou ajoutez une exception dans l'antivirus

## 🛠️ Résolution de Problèmes

### "L'application ne se lance pas"
1. **Antivirus** : Ajoutez MatelasProcessor.exe aux exceptions
2. **Permissions** : Clic droit sur l'exe → Propriétés → Débloquer
3. **Dépendances** : Installez Visual C++ Redistributable Microsoft

### "Module non trouvé"
- Recompilez en ajoutant le module manquant dans `matelas_processor.spec`

### Compilation échoue
```bash
# Nettoyer et recommencer
rm -rf build/ dist/ *.spec
python build_windows.py
```

## 🎨 Personnalisation

### Icône personnalisée
1. Ajoutez votre icône : `assets/icon.ico`
2. Recompilez : `python build_windows.py`

### Réduire la taille
1. Ouvrez `matelas_processor.spec`
2. Ajoutez des modules à exclure dans `excludes=[]`
3. Activez la compression UPX : `upx=True`

## ✅ Test de Validation

Testez ces fonctionnalités sur Windows :
- [ ] L'application se lance
- [ ] Interface graphique complète
- [ ] Bouton "Ouvrir Dossier Excel" fonctionne
- [ ] Génération de rapport HTML
- [ ] Tous les onglets accessibles
- [ ] Fermeture propre

## 📞 Support

En cas de problème :
1. Vérifiez `README_Windows_Build.md` pour plus de détails
2. Testez d'abord `python app_gui.py` (version développement)
3. Consultez les logs dans `AppData\Local\MatelasProcessor\logs\`

---

🎉 **Votre application est maintenant prête pour Windows !**