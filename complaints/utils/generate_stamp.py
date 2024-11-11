from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import mm
from complaints.utils.utils import file_name_generator


def add_newline_every_n_chars(text, n=90):
    words = text.split()  # Split the text into words
    result = []
    line = ""

    for word in words:
        # If adding the next word exceeds the limit, append the line and start a new one
        if len(line) + len(word) + 1 > n:  # +1 for the space
            result.append(line.strip())  # Append the current line and strip trailing spaces
            line = word + " "  # Start the next line with the current word
        else:
            line += word + " "  # Add word to the current line

    # Append the final line
    if line:
        result.append(line.strip())

    # Join all the lines with a newline character
    return '\n'.join(result)
def generate_stamp(report):
    if report.date_purchase:
        purchased_date = report.date_purchase.strftime("%d.%m.%Y")
    else:
        purchased_date = ""
    report_date = report.created_at.strftime("%d.%m.%Y")

    if report.date_return:
        return_date = report.date_return.strftime("%d.%m.%Y")
    else:
        return_date = ""

    # Register Cyrillic-supporting font (like DejaVu)
    pdfmetrics.registerFont(TTFont('DejaVu', 'assets/gothampro.ttf'))

    # Create a PDF document
    file_name = f"{file_name_generator()}-report.pdf"
    pdf = canvas.Canvas(file_name, pagesize=A4)

    # Set the font for the entire document
    pdf.setFont("DejaVu", 8)

    # A4 dimensions: width = 595.27 points, height = 841.89 points
    pdf.drawCentredString(500, 740, f"№ {report.id} от {report_date}")
    # Insert an image (e.g., logo) at the top of the page
    image_path = 'assets/output-onlinepngtools.png'  # Replace with your image path
    image_x = 70  # X position of the image
    image_y = 740  # Y position of the image
    image_width = 70  # Desired width of the image
    image_height = 40  # Desired height of the image
    pdf.drawImage(image_path, image_x, image_y, width=image_width, height=image_height)

    # Example: Place the title at a specific position (centered)



    # Data for the table
    data = [
        ['Наименование изделия:', report.complaint_product[0].product.name if report.complaint_product else report.product_name],
        ['Наименование филиала, где куплено:', report.branch.name],
        ['Дата покупки:', purchased_date ],
        ['Дата поступления образца в лабораторию:', return_date],
        ['Причина обращения:', report.comment],
    ]

    # Create the table
    table = Table(data, colWidths=[100 * mm, 80 * mm])

    # Set the table style (for borders, alignment, etc.)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Header background color
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),      # Text color
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),                # Text alignment
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVu'),           # Font for Cyrillic
        ('FONTSIZE', (0, 0), (-1, -1), 8),                 # Font size
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),      # Grid lines
    ]))

    # Define table position (x, y) - here starting at 200 points from bottom-left corner
    table.wrapOn(pdf, 400, 600)   # Width and height to wrap content (table size)
    table.drawOn(pdf, 50, 640)    # Position (x=50, y=600) to place the table

    # Add a paragraph of text below the table
    pdf.setFont("DejaVu", 12)

    pdf.drawCentredString(297.63, 550, "ЗАКЛЮЧЕНИЕ ЛАБОРАТОРИИ")


    text = report.second_response
    text = add_newline_every_n_chars(text, 100)
    # Set font again for the following text
    pdf.setFont("DejaVu", 8)
    # Text position (x=50, y=550), just below the table
    text_lines = text.split('\n')  # Split text into lines
    y_position = 510
    for line in text_lines:
        pdf.drawString(50, y_position, line.strip())
        y_position -= 20  # Move to the next line

    role_y_start_position = 300
    role_x_start_position = 50
    name_x_start_position = 430
    name_y_start_position = 300
    stamp_y_start_position = 280
    stamp_x_start_position = 340
    signeture_y_start_position = 265
    signeture_x_start_position = 300
    for user in report.complaint_stamp:
        pdf.drawString(role_x_start_position, role_y_start_position-60, user.user.role.name)
        pdf.drawString(name_x_start_position, name_y_start_position-60, user.user.name)


          # Replace with your image path
        if user.user.stamp:
            image_path = user.user.stamp
            image_x = stamp_x_start_position  # X position of the image
            image_y = stamp_y_start_position-60  # Y position of the image
            image_width = 70  # Desired width of the image
            image_height = 60  # Desired height of the image
            pdf.drawImage(image_path, image_x, image_y, width=image_width, height=image_height)

        if user.user.signeture:
            image_path = user.user.signeture
            image_x = signeture_x_start_position  # X position of the image
            image_y = signeture_y_start_position-60  # Y position of the image
            image_width = 90  # Desired width of the image
            image_height = 90  # Desired height of the image
            pdf.drawImage(image_path, image_x, image_y, width=image_width, height=image_height, mask='auto')

    # Save the PDF document
    pdf.save()

    return file_name
