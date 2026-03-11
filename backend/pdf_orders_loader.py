import json
import logging
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional

from PyPDF2 import PdfReader

logger = logging.getLogger(__name__)


@dataclass
class OrderArticle:
    raw_text: str


@dataclass
class OrderDocument:
    file_path: str
    client_raw: Optional[str]
    client_normalized: Optional[str]
    city: Optional[str]
    order_number: Optional[str]
    order_code: Optional[str]
    order_type: str
    logistics: Dict[str, bool]
    articles: List[OrderArticle]
    raw_text: str


class PDFOrderLoader:
    CLIENT_PATTERN = re.compile(r"^(M(?:r|me|e)\b.*)$", re.IGNORECASE | re.MULTILINE)
    CITY_PATTERN = re.compile(r"\b(\d{5})\s+([A-Za-zÀÂÇÉÈÊËÎÏÔÙÛÜàâçéèêëîïôùûü'\- ]+)")
    ORDER_CODE_PATTERN = re.compile(r"CM\d{5,}")
    NAME_STOPWORDS = {"MR", "MME", "ME", "ET", "M", "MRS"}

    def __init__(self, directory: Path):
        self.directory = Path(directory)

    def extract_orders(self) -> List[OrderDocument]:
        orders: List[OrderDocument] = []
        for pdf_path in sorted(self.directory.glob("*.pdf")):
            if not pdf_path.name.lower().startswith("commandes"):
                continue
            try:
                text = self._read_pdf(pdf_path)
            except Exception as exc:
                logger.exception("Impossible de lire %s: %s", pdf_path, exc)
                continue

            client_raw = self._extract_client(text)
            normalized = self._normalize_client_name(client_raw, pdf_path.stem)
            city = self._extract_city(text)
            order_number = self._extract_order_number(pdf_path)
            order_code = self._extract_order_code(text)
            order_type = self._detect_order_type(text, normalized)
            logistics = self._detect_logistics(text)
            articles = self._extract_articles(text)

            order = OrderDocument(
                file_path=str(pdf_path),
                client_raw=client_raw,
                client_normalized=normalized,
                city=city,
                order_number=order_number,
                order_code=order_code,
                order_type=order_type,
                logistics=logistics,
                articles=articles,
                raw_text=text,
            )
            logger.info(
                "Commande détectée: client=%s, numéro=%s, type=%s, articles=%d",
                order.client_normalized,
                order.order_number,
                order.order_type,
                len(order.articles),
            )
            orders.append(order)
        return orders

    @staticmethod
    def _read_pdf(path: Path) -> str:
        reader = PdfReader(str(path))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages)

    def _extract_client(self, text: str) -> Optional[str]:
        match = self.CLIENT_PATTERN.search(text)
        return match.group(1).strip() if match else None

    def _normalize_client_name(self, client_raw: Optional[str], fallback: str) -> Optional[str]:
        if not client_raw:
            return self._normalize_from_filename(fallback)
        cleaned = (
            client_raw.replace("Mr et Me", "")
            .replace("Mr et Mme", "")
            .replace("Me ", "")
            .replace("Mr ", "")
            .replace("Mme ", "")
            .strip()
        )
        parts = [word for word in re.split(r"[\s/&]+", cleaned) if word]
        for part in reversed(parts):
            candidate = part.strip().upper()
            if candidate and candidate not in self.NAME_STOPWORDS:
                return candidate
        return self._normalize_from_filename(fallback)

    def _normalize_from_filename(self, stem: str) -> Optional[str]:
        match = re.search(r"Commandes\s+(.*?)_", stem, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            return name.upper()
        return None

    def _extract_city(self, text: str) -> Optional[str]:
        for match in self.CITY_PATTERN.finditer(text):
            postal_code = match.group(1)
            city = match.group(2).strip().upper()
            # Exclure l'adresse société (BORRE), les codes APE (00015), et les villes commençant par tiret
            if (city and city != "BORRE" and "BORRE" not in city
                    and not postal_code.startswith("000")
                    and not city.startswith("-")):
                return city
        return None

    def _extract_order_number(self, path: Path) -> Optional[str]:
        match = re.search(r"_(.+)\.pdf$", path.name, re.IGNORECASE)
        if match:
            return match.group(1)
        return None

    def _extract_order_code(self, text: str) -> Optional[str]:
        match = self.ORDER_CODE_PATTERN.search(text)
        return match.group(0) if match else None

    def _detect_order_type(self, text: str, normalized_client: Optional[str]) -> str:
        upper_text = text.upper()
        if normalized_client and normalized_client.startswith("MAGASIN"):
            return "magasin"
        if ("MAGASIN" in upper_text or "STOCK" in upper_text) and "SOMMIER" not in upper_text:
            return "magasin"
        if "SOMMIER" in upper_text or "LITERIE" in upper_text:
            return "sommier"
        if any(keyword in upper_text for keyword in ["TÊTE", "PIED", "DOS", "CHEVET"]):
            return "accessoires"
        return "inconnu"

    def _detect_logistics(self, text: str) -> Dict[str, bool]:
        upper = text.upper()
        return {
            "pickup": bool(re.search(r"ENLÈVEMENT|ENLEVEMENT|EMPORT", upper)),
            "delivery": bool(re.search(r"LIVRAISON|INSTALLATION", upper)),
            "transporteur": bool(re.search(r"TRANSPORTEUR", upper)),
        }

    # Pattern for article line start: "AMOUNT AMOUNT QUANTITY DESCRIPTION"
    # e.g. "2 001,50 2 001,50 1,00 SOMMIER..." or "0,00 0,00 0,00 LITERIE..."
    ARTICLE_LINE_PATTERN = re.compile(
        r"^([\d\s]+[,\.]\d{2})\s+([\d\s]+[,\.]\d{2})\s+([\d\s]+[,\.]\d{2})\s+(.+)",
        re.MULTILINE
    )

    def _extract_articles(self, text: str) -> List[OrderArticle]:
        if "Description" not in text:
            return []
        _, after_description = text.split("Description", 1)
        before_totals = after_description.split("Taux", 1)[0]

        # Split on article boundaries (price lines)
        matches = list(self.ARTICLE_LINE_PATTERN.finditer(before_totals))
        if not matches:
            # Fallback to old behavior
            chunks = re.split(r"\n\s*\n", before_totals)
            articles: List[OrderArticle] = []
            for chunk in chunks:
                stripped = chunk.strip()
                if not stripped or stripped.lower().startswith("qté"):
                    continue
                articles.append(OrderArticle(raw_text=stripped))
            return articles

        articles: List[OrderArticle] = []
        for i, match in enumerate(matches):
            start = match.start()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(before_totals)
            raw = before_totals[start:end].strip()
            # Skip "Dont Eco-Part" lines that may trail
            # Remove trailing "Dont Eco-Part..." lines from the article text
            raw = re.sub(r"\nDont Eco\s*-?\s*Part\..*$", "", raw, flags=re.DOTALL | re.MULTILINE)
            raw = raw.strip()
            if not raw:
                continue
            articles.append(OrderArticle(raw_text=raw))
        return articles


def dump_orders_to_json(input_dir: str, output_file: str) -> None:
    loader = PDFOrderLoader(Path(input_dir))
    orders = loader.extract_orders()
    data = [asdict(order) for order in orders]
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    logger.info("Export PDF → JSON terminé (%s)", output_path)


if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    parser = argparse.ArgumentParser(description="Extraction des commandes PDF.")
    parser.add_argument("input_dir", help="Dossier contenant les PDF (ex: /path/to/1103)")
    parser.add_argument(
        "--output",
        "-o",
        default="logs/pdf_orders_snapshot.json",
        help="Fichier JSON de sortie",
    )
    args = parser.parse_args()
    dump_orders_to_json(args.input_dir, args.output)
