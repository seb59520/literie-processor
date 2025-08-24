#!/usr/bin/env python3
"""
Test rapide: simule un upload via l'endpoint /upload sans dépendre d'un serveur en cours.
- Appelle directement la coroutine upload_pdf de backend.main avec un faux fichier.
- Génère un petit PDF en mémoire pour l'extraction PyMuPDF.
"""
import asyncio
import io
import json
import os
import sys
from typing import List

from fastapi import UploadFile
from starlette.datastructures import UploadFile as StarletteUploadFile

# Créer un PDF minimal en mémoire
try:
    import fitz  # PyMuPDF
except Exception as e:
    raise SystemExit(f"PyMuPDF requis pour le test: {e}")

def make_pdf_bytes(text: str = "MATELAS 1 PIECE 140x190 TENCEL") -> bytes:
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), text)
    data = doc.tobytes()
    doc.close()
    return data

async def main():
    # Ajouter la racine du projet au PYTHONPATH
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    if ROOT_DIR not in sys.path:
        sys.path.insert(0, ROOT_DIR)

    from backend.main import upload_pdf
    from fastapi import Request
    from starlette.requests import Request as StarletteRequest
    from starlette.datastructures import FormData

    # Préparer un faux fichier PDF
    pdf_bytes = make_pdf_bytes()
    fake_file = StarletteUploadFile(filename="test.pdf", file=io.BytesIO(pdf_bytes))

    # Construire un faux Request minimal
    scope = {"type": "http", "method": "POST"}
    request = StarletteRequest(scope)

    # Appeler la coroutine FastAPI directement
    result = await upload_pdf(
        request=request,
        file=[fake_file],
        enrich_llm="no",
        llm_provider="ollama",
        openrouter_api_key=None,
        semaine_prod=32,
        annee_prod=2025,
        commande_client=["TEST_CLIENT"],
    )

    # Vérifier que la réponse est un TemplateResponse et imprimer quelques champs
    from starlette.templating import _TemplateResponse
    if isinstance(result, _TemplateResponse):
        ctx = result.context
        print("status:", ctx.get("error") or "ok")
        results = ctx.get("results") or []
        if results:
            print("filename:", results[0].get("filename"))
            print("nb_mots:", results[0].get("extraction_stats", {}).get("nb_mots"))
            print("contient_dosseret_ou_tete:", results[0].get("contient_dosseret_ou_tete"))
    else:
        print("Unexpected result type:", type(result))

if __name__ == "__main__":
    asyncio.run(main())
