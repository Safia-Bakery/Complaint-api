from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import mm
from complaints.utils.utils import file_name_generator


def add_newline_every_n_chars(text, n=90):
    words = text.split()
    result = []
    line = ""

    for word in words:
        if len(line) + len(word) + 1 > n:
            result.append(line.strip())
            line = word + " "
        else:
            line += word + " "

    if line:
        result.append(line.strip())

    return '\n'.join(result)


def generate_stamp(report):
    def check_page_break(pdf, y_position, threshold=50):
        """
        Check if the current y_position is below the threshold,
        and if so, start a new page.
        """
        if y_position < threshold:
            pdf.showPage()
            pdf.setFont("DejaVu", 8)
            return 740  # Reset y_position for a new page
        return y_position

    if report.date_purchase:
        purchased_date = report.date_purchase.strftime("%d.%m.%Y")
    else:
        purchased_date = ""
    report_date = report.created_at.strftime("%d.%m.%Y")

    if report.date_return:
        return_date = report.date_return.strftime("%d.%m.%Y")
    else:
        return_date = ""

    pdfmetrics.registerFont(TTFont('DejaVu', '/var/www/Complaint-api/assets/gothampro.ttf'))

    file_name = f"/var/www/Complaint-api/files/{file_name_generator()}-report.pdf"
    return_name = f"files/{file_name_generator()}-report.pdf"

    pdf = canvas.Canvas(file_name, pagesize=A4)
    pdf.setFont("DejaVu", 8)

    y_position = 740  # Start position

    # Header
    pdf.drawCentredString(500, y_position, f"№ {report.id} от {report_date}")
    y_position -= 20

    # Insert logo
    image_path = '/var/www/Complaint-api/assets/output-onlinepngtools.png'
    pdf.drawImage(image_path, 70, y_position, width=70, height=40)
    y_position -= 50

    # Quality control image
    quality_path = '/var/www/Complaint-api/assets/control.png'
    pdf.drawImage(quality_path, 260, y_position + 10, width=105, height=60)
    y_position -= 60

    # Data Table
    data = [
        ['Наименование изделия:', report.complaint_product_name],
        ['Наименование филиала, где куплено:', report.branch_name],
        ['Дата покупки:', purchased_date],
        ['Дата поступления образца в лабораторию:', return_date],
        ['Причина обращения:', report.category_name],
    ]
    table = Table(data, colWidths=[100 * mm, 80 * mm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVu'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    table.wrapOn(pdf, 400, y_position)
    table.drawOn(pdf, 50, y_position - 80)
    y_position -= 120

    y_position = check_page_break(pdf, y_position)

    # Conclusion
    pdf.setFont("DejaVu", 12)
    pdf.drawCentredString(297.63, y_position, "ЗАКЛЮЧЕНИЕ ЛАБОРАТОРИИ")
    y_position -= 40

    if report.second_response:
        text = add_newline_every_n_chars(report.second_response, 100)
        pdf.setFont("DejaVu", 8)
        for line in text.split('\n'):
            pdf.drawString(50, y_position, line.strip())
            y_position -= 20
            y_position = check_page_break(pdf, y_position)

    match_standard = "Предоставленный образец соответствует стандартам компании." if report.match_standard == 1 else "Предоставленный образец несоответствует стандартам компании."
    pdf.drawString(50, y_position, match_standard)
    y_position -= 40
    y_position = check_page_break(pdf, y_position)

    # Stamps and roles
    for user in report.complaint_stamp:
        pdf.drawString(50, y_position, user.user.role.name)
        pdf.drawString(430, y_position, user.user.name)
        y_position -= 20

        if user.user.stamp:
            image_path = f"/var/www/Complaint-api/{user.user.stamp}"
            pdf.drawImage(image_path, 340, y_position, width=70, height=60)
            y_position -= 60

        y_position = check_page_break(pdf, y_position)

    pdf.save()
    return return_name
