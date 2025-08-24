# 🔧 Correction Erreur d'Encodage Windows

## ❌ **Erreur rencontrée**
```
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 1228: character maps to <undefined>
```

## ✅ **Correction appliquée**

L'erreur était causée par les **émojis Unicode** (✅🚀📦🎉❌⚠️) dans les messages du script, incompatibles avec l'encodage Windows cp1252.

### **Solutions appliquées :**

1. **Remplacement des émojis** par des marqueurs ASCII :
   - ✅ → `[OK]`
   - ❌ → `[ERREUR]`  
   - 🚀 → supprimé
   - 📦 → supprimé
   - ⚠️ → `[!]`
   - 💡 → `[Info]`

2. **Correction de l'encodage des fichiers** :
   - Script batch : `encoding='utf-8'` + `chcp 65001`
   - Suppression des accents dans les commentaires batch

## 🔄 **Fichiers corrigés**

### **build_windows.py**
- ✅ Tous les émojis remplacés par des marqueurs ASCII
- ✅ Messages d'erreur compatibles Windows
- ✅ Encodage UTF-8 pour les fichiers générés

### **quick_build.py**  
- ✅ Messages sans émojis
- ✅ Compatible console Windows

### **install.bat**
- ✅ `chcp 65001` pour support UTF-8
- ✅ Caractères spéciaux supprimés

## 🚀 **Test de la correction**

### **1. Testez l'environnement :**
```cmd
python test_windows.py
```

### **2. Compilez maintenant :**
```cmd
python build_windows.py
```

### **3. Ou compilation rapide :**
```cmd
python quick_build.py
```

## 📋 **Vérifications**

Après compilation, vous devriez avoir :
```
dist/
├── MatelasProcessor.exe    # Exécutable Windows
└── install.bat            # Script d'installation
```

## ⚠️ **Notes importantes**

### **Console Windows**
- Les messages utilisent maintenant `[OK]`, `[ERREUR]`, `[!]` 
- Compatible avec toutes les versions de Windows
- Pas de problème d'affichage dans CMD/PowerShell

### **Encodage des fichiers**
- Scripts Python : UTF-8
- Batch Windows : UTF-8 avec `chcp 65001`
- Pas de caractères problématiques

### **Si l'erreur persiste**
1. Vérifiez votre console : `chcp 65001`
2. Ou utilisez PowerShell au lieu de CMD
3. Contactez-moi avec le message d'erreur exact

## ✅ **Résultat attendu**

Compilation sans erreur d'encodage, avec messages clairs :
```
=== CREATION D'EXECUTABLE WINDOWS ===
Application: Processeur de Devis Literie
==================================================
Verification des prerequis...
[OK] PyInstaller trouve: 6.x.x
[OK] PyQt6 disponible
...
[OK] COMPILATION REUSSIE!
```

---

🎯 **La correction est maintenant appliquée. Vous pouvez relancer la compilation !**