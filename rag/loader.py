import os
import re
from typing import List, Dict


class KnowledgeBaseLoader:
    def __init__(self, kb_path: str = "knowledge_base"):
        self.kb_path = kb_path

    def load(self) -> List[Dict]:
        all_chunks = []

        for filename in os.listdir(self.kb_path):
            if not filename.endswith(".txt"):
                continue

            file_path = os.path.join(self.kb_path, filename)

            with open(file_path, "r", encoding="utf-8") as f:
                raw_text = f.read()

            cleaned = self._clean_text(raw_text)
            chunks = self._chunk_text(cleaned)

            topic = self._extract_topic(raw_text, filename)

            for chunk in chunks:
                all_chunks.append({
                    "type": "KNOWLEDGE",
                    "topic": topic,
                    "text": chunk,
                    "source": "MedlinePlus",
                    "filename": filename
                })

        return all_chunks

    def _clean_text(self, text: str) -> str:
        # Remove share/navigation junk
        text = re.sub(r"Email this page.*?\n", "", text)
        text = re.sub(r"Print.*?\n", "", text)
        text = re.sub(r"Facebook.*?\n", "", text)
        text = re.sub(r"Pinterest.*?\n", "", text)

        # Normalize spacing
        text = re.sub(r"\n\s*\n", "\n\n", text)

        return text.strip()

    def _chunk_text(self, text: str, max_chars: int = 900):
        paragraphs = text.split("\n\n")

        chunks = []
        current_chunk = ""

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            # If paragraph itself is too large → split it
            if len(para) > max_chars:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""

                for i in range(0, len(para), max_chars):
                    chunks.append(para[i:i + max_chars].strip())
                continue

            # Normal accumulation
            if len(current_chunk) + len(para) < max_chars:
                current_chunk += "\n\n" + para
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = para

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks


    def _extract_topic(self, raw_text: str, filename: str) -> str:
        first_line = raw_text.split("\n")[0].strip()
        return first_line if first_line else filename.replace(".txt", "")
