from pathlib import Path
from html import escape

from PIL import Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output' / 'pdf' / 'student_profile_assignment.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)
TMP = ROOT / 'tmp' / 'pdfs'
TMP.mkdir(parents=True, exist_ok=True)
FONT_DIR = Path('C:/Windows/Fonts')
pdfmetrics.registerFont(TTFont('Segoe', str(FONT_DIR / 'segoeui.ttf')))
pdfmetrics.registerFont(TTFont('SegoeBold', str(FONT_DIR / 'segoeuib.ttf')))
W, H = landscape(A4)
INK = colors.HexColor('#203b36')
GREEN = colors.HexColor('#245642')
MUTED = colors.HexColor('#68786f')
PALE = colors.HexColor('#f0f3e9')
RULE = colors.HexColor('#dce3d7')
M = 42
CONTENT = W - 2 * M
REPO = 'https://github.com/Ahmed-you/ahmed_younis_django_templates'
c = canvas.Canvas(str(OUT), pagesize=(W, H))
c.setTitle('Student Profile - Home Page and Model Assignment')
c.setAuthor('Ahmed Wael Younis')
c.setSubject('Django model, migrations, admin entry and Home Page')
style = ParagraphStyle('body', fontName='Segoe', fontSize=10, leading=15, textColor=INK)
small = ParagraphStyle('small', parent=style, fontSize=9, leading=13)


def paragraph(text, x, top, width=CONTENT, text_style=style):
    p = Paragraph(text, text_style)
    _, height = p.wrap(width, 1000)
    p.drawOn(c, x, top-height)
    return top-height


def page(number, title, subtitle):
    c.setFillColor(colors.white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont('SegoeBold', 21)
    c.drawString(M, H-58, title)
    paragraph(subtitle, M, H-72, text_style=small)


def table(rows, widths, top, font_size=9):
    ps = ParagraphStyle('cell', parent=small, fontSize=font_size, leading=font_size+4)
    data = [[Paragraph(escape(str(cell)), ps) for cell in row] for row in rows]
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PALE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7f9f4')]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 9),
        ('LINEBELOW', (0, 0), (-1, 0), .6, RULE),
    ]))
    _, height = t.wrap(CONTENT, H)
    t.drawOn(c, M, top-height)
    return top-height


def screenshot(name, top, max_width=CONTENT, crop_height=None):
    source = ROOT / 'docs' / 'evidence' / name
    im = Image.open(source)
    if crop_height:
        im = im.crop((0, 0, im.width, min(crop_height, im.height)))
    target = TMP / name
    im.save(target)
    width = max_width
    height = width * im.height / im.width
    c.drawImage(str(target), (W-width)/2, top-height, width, height)
    return top-height


page(1, 'Home Page & model assignment', 'StudentProfile model in the existing pages application. The Home Page reads saved records from the database.')
paragraph('<b>Page:</b> http://127.0.0.1:8000/ &nbsp;&nbsp; <b>Admin:</b> http://127.0.0.1:8000/admin/', M, 455)
rows = [
    ['Field name', 'Django data type', 'Reason for the choice'],
    ['full_name', 'CharField(max_length=150)', 'A name is short text with a practical maximum length.'],
    ['university_id', 'CharField(max_length=20, unique=True)', 'An identifier is text, even when it contains only digits. Text preserves leading zeros; uniqueness prevents duplicate IDs.'],
    ['age', 'PositiveSmallIntegerField', 'Age is a small whole number. Validators restrict it to 1-120 years.'],
    ['date_of_birth', 'DateField', 'Stores a calendar date without an unnecessary time. Model validation rejects future dates.'],
    ['address', 'TextField', 'An address can contain several lines and vary in length.'],
    ['salary', 'DecimalField(max_digits=10, decimal_places=2)', 'Stores monetary amounts with two decimal places, avoiding floating-point rounding. Salary must be nonnegative.'],
    ['photo', 'ImageField(upload_to="profiles/")', 'Accepts image uploads. The database stores the file path; the image file is stored in media/profiles/. Pillow provides image validation.'],
]
bottom = table(rows, [115, 228, CONTENT-343], 423)
paragraph(f'<b>GitHub:</b> <link href="{REPO}" color="#245642">{REPO}</link>', M, bottom-15, text_style=small)
paragraph('Field reference: <link href="https://docs.djangoproject.com/en/5.2/ref/models/fields/" color="#245642">Django 5.2 model field documentation</link>', M, bottom-37, text_style=small)
c.showPage()

page(2, 'Database migrations', 'Commands run from the project folder after activating the virtual environment.')
commands = [
    'python manage.py makemigrations pages',
    'python manage.py migrate',
    'python manage.py showmigrations pages',
]
c.setFillColor(INK)
c.setFont('Courier', 10)
for i, line in enumerate(commands):
    c.drawString(M, 459-i*20, line)
c.setFillColor(INK)
c.setFont('SegoeBold', 11)
c.drawString(M, 358, 'Migration output')
output = (ROOT / 'docs/evidence/migrate.txt').read_text(encoding='utf-8-sig').splitlines()
c.setFont('Courier', 8)
y = 337
for line in output:
    c.drawString(M, y, line)
    y -= 11
right = M+468
c.setFont('SegoeBold', 11)
c.drawString(right, 358, 'Model migration')
paragraph('0001_initial.py<br/>Create model StudentProfile', right, 337, CONTENT-468, small)
c.setFont('SegoeBold', 11)
c.drawString(right, 266, 'Applied status')
status = (ROOT / 'docs/evidence/showmigrations.txt').read_text(encoding='utf-8-sig').strip()
paragraph(escape(status).replace('\n', '<br/>'), right, 247, CONTENT-468, small)
paragraph('The [X] confirms that pages.0001_initial has been applied. The original command logs are included in docs/evidence/.', right, 195, CONTENT-468, small)
paragraph('<b>Verification</b><br/>Django system check: no issues.<br/>Six tests passed.<br/>No pending model changes.', right, 120, CONTENT-468, small)
c.showPage()

page(3, 'Enter values in admin', 'Admin > Pages > Student profiles > Add student profile. All seven fields are completed, including the image upload.')
screenshot('admin-entry.png', 465, crop_height=800)
c.showPage()

page(4, 'Saved student record', 'Selecting Save creates the record. The confirmation and the row below show that the admin submission succeeded.')
screenshot('admin-saved.png', 465, crop_height=440)
paragraph('The salary is a sample value. The uploaded image is an illustrated avatar. Age 22 is the entered age on 28 October 2026.', M, 211, text_style=small)
c.showPage()

page(5, 'Home Page', 'http://127.0.0.1:8000/  |  The saved database record and uploaded image appear in the page template.')
screenshot('home-desktop.png', 483, max_width=710, crop_height=890)
c.setFillColor(INK)
c.setFont('Segoe', 11)
c.drawRightString(W-M, 22, 'Ahmed Wael Younis')
c.showPage()
c.save()
print(OUT)
