from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os

def draw_header(c, width, height, logo_path):
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2.0, height - 40, "CONTROLE DE BAGAGEM")

    if os.path.exists(logo_path):
        try:
            logo = ImageReader(logo_path)
            # Put logo top left
            c.drawImage(logo, 30, height - 70, width=80, height=50, preserveAspectRatio=True, mask='auto')
        except Exception as e:
            print(f"Error loading logo: {e}")

def create_baggage_pdf(filename, passengers, copies=20, logo_path="app/assets/logo.png"):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    margin_x = 30
    margin_y = 80
    box_width = width - 2 * margin_x
    box_height = 80
    gap = 10

    # Check if we should render blank pages or filled pages
    if not passengers:
        # Default empty boxes for blank print
        passengers = [{"nome": "", "cidade": "", "poltrona": ""}] * 7

    boxes_per_page = 7 # Fits nicely on A4

    for copy_idx in range(copies):
        passenger_idx = 0
        while passenger_idx < len(passengers):
            draw_header(c, width, height, logo_path)

            y_pos = height - margin_y - box_height

            count_on_page = 0
            while count_on_page < boxes_per_page and passenger_idx < len(passengers):
                p = passengers[passenger_idx]

                # Draw the main box
                c.rect(margin_x, y_pos, box_width, box_height)

                # Draw a vertical line to separate info from sticker area
                c.line(margin_x + box_width * 0.6, y_pos, margin_x + box_width * 0.6, y_pos + box_height)

                # Write text inside the box
                text_x = margin_x + 10
                text_y = y_pos + box_height - 20
                c.setFont("Helvetica", 12)

                c.drawString(text_x, text_y, f"NOME: {p['nome']}")
                c.drawString(text_x, text_y - 25, f"CIDADE: {p['cidade']}")
                c.drawString(text_x, text_y - 50, f"POLT: {p['poltrona']}")

                y_pos -= (box_height + gap)
                passenger_idx += 1
                count_on_page += 1

            c.showPage()

    c.save()

if __name__ == "__main__":
    create_baggage_pdf("test.pdf", [], copies=1)
