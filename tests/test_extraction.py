import os
from dotenv import load_dotenv
from ingestion.pipeline import run_extraction_pipeline
from models.factory import get_llm

load_dotenv()

llm = get_llm()


class FakeFile:
    def __init__(self, text):
        self.type = "text/plain"
        self._text = text

    def read(self):
        return self._text.encode("utf-8")


sample_report = """
Complete Blood Count

WBC 7.5 4.5-11.0 x10^3/uL
RBC 4.3 4.2-5.9 x10^6/uL
Hemoglobin 10.2 13.5-17.5 g/dL L
Hematocrit 30.1 41-53 %
MCV 80 80-100 fL
Platelets 200 150-400 x10^3/uL
Vitamin D 28 30-100 ng/mL
"""

fake_file = FakeFile(sample_report)

result = run_extraction_pipeline(fake_file, llm)

print("\n=== RAW TEXT ===\n")
print(result["raw_text"])

print("\n=== STRUCTURED DATA ===\n")
for test in result["structured_data"]["tests"]:
    print(test)

print("\nTotal tests extracted:", len(result["structured_data"]["tests"]))
