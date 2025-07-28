# Adobe Hackathon Round 1A - Heading Extractor

## Goal
Extracts structured outlines from PDFs (title, H1, H2, H3) in JSON format.

## Tech Stack
- Python 3.10
- PyMuPDF (fitz)
- Docker

## Directory
- `/app/input`: PDF files (≤ 50 pages)
- `/app/output`: JSON output for each PDF

## Run

```bash
docker build --platform linux/amd64 -t heading-extractor:demo .
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  heading-extractor:demo
