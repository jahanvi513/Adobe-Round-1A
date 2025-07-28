import fitz  # PyMuPDF
import os
import json

def extract_headings(doc):
    """
    Extracts headings from the PDF using font size heuristics.
    Returns title and a list of outline elements.
    """
    font_stats = {}
    outlines = []
    
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]

        for b in blocks:
            if "lines" not in b:
                continue
            for line in b["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text or len(text) < 3:
                        continue
                    size = round(span["size"], 1)
                    font_stats[size] = font_stats.get(size, 0) + 1
                    outlines.append({
                        "text": text,
                        "size": size,
                        "page": page_num + 1
                    })

    # Determine heading levels by font size ranking
    size_to_level = {}
    sizes_sorted = sorted(font_stats.items(), key=lambda x: -x[0])
    if len(sizes_sorted) >= 1: size_to_level[sizes_sorted[0][0]] = "H1"
    if len(sizes_sorted) >= 2: size_to_level[sizes_sorted[1][0]] = "H2"
    if len(sizes_sorted) >= 3: size_to_level[sizes_sorted[2][0]] = "H3"

    headings = []
    title = None
    for item in outlines:
        level = size_to_level.get(item["size"])
        if level:
            if not title:
                title = item["text"]
            headings.append({
                "level": level,
                "text": item["text"],
                "page": item["page"]
            })

    return title or "Untitled Document", headings


def process_pdf(input_path, output_path):
    try:
        doc = fitz.open(input_path)
        title, outline = extract_headings(doc)
        doc.close()

        result = {
            "title": title,
            "outline": outline
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"✅ Processed {os.path.basename(input_path)}")

    except Exception as e:
        print(f"❌ Failed to process {input_path}: {e}")


def batch_process(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename.replace(".pdf", ".json"))
            process_pdf(input_path, output_path)


if __name__ == "__main__":
    INPUT_DIR = "app/input"
    OUTPUT_DIR = "app/output"
    batch_process(INPUT_DIR, OUTPUT_DIR)