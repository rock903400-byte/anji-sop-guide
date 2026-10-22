import os
import sys
import fitz

sys.stdout.reconfigure(encoding="utf-8")


def build_assets():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pdf_path = os.path.join(base_dir, "安基作業教學_20260819 (1).pdf")
    out_dir = os.path.join(base_dir, "assets", "slides")
    os.makedirs(out_dir, exist_ok=True)

    doc = fitz.open(pdf_path)
    total = len(doc)
    print(f"Exporting {total} pages from {pdf_path} to {out_dir}...")

    # 2880x1620 at 72 DPI -> scale 0.667 gives 1920x1080 Full HD crisp output
    mat = fitz.Matrix(1920 / 2880, 1080 / 1620)
    for i, page in enumerate(doc):
        page_num = i + 1
        out_path = os.path.join(out_dir, f"page_{page_num:03d}.jpg")
        if not os.path.exists(out_path):
            pix = page.get_pixmap(matrix=mat, alpha=False)
            pix.save(out_path, jpg_quality=85)
        if page_num % 25 == 0 or page_num == total:
            print(f"Processed {page_num}/{total} pages")

    print("All slide images exported successfully.")


if __name__ == "__main__":
    build_assets()
