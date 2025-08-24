#!/usr/bin/env python3
"""
Test HTTP: envoie un PDF généré en mémoire à l'endpoint /upload d'un backend en cours d'exécution.
Utilisation:
  HOST=http://localhost:8000 python3 scripts/test_upload_http.py
"""
import io
import os
import sys

import httpx

try:
    import fitz  # PyMuPDF
except Exception as e:
    raise SystemExit(f"PyMuPDF requis pour le test: {e}")

HOST = os.environ.get("HOST", "http://localhost:8000")


def make_pdf_bytes(text: str = "MATELAS 1 PIECE 140x190 TENCEL") -> bytes:
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), text)
    data = doc.tobytes()
    doc.close()
    return data


def main():
    pdf_bytes = make_pdf_bytes()

    files = [
        (
            "file",
            ("test.pdf", io.BytesIO(pdf_bytes), "application/pdf"),
        )
    ]

    # Champs de formulaire requis par l'endpoint
    data = [
        ("enrich_llm", "no"),
        ("llm_provider", "ollama"),
        ("openrouter_api_key", ""),
        ("semaine_prod", "32"),
        ("annee_prod", "2025"),
        ("commande_client", "TEST_CLIENT"),
    ]

    url = f"{HOST.rstrip('/')}/upload"
    print(f"POST {url}")
    with httpx.Client(timeout=60.0) as client:
        resp = client.post(url, files=files, data=data)
        print("Status:", resp.status_code)
        # Affiche début du HTML retourné (template)
        print(resp.text[:300])


if __name__ == "__main__":
    main()
