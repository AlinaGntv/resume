from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).parent
OUT = ROOT / "output" / "pdf"
OUT.mkdir(parents=True, exist_ok=True)
PDF = OUT / "alina_resume.pdf"

FONT_DIR = Path(r"C:\Windows\Fonts")
pdfmetrics.registerFont(TTFont("Arial", str(FONT_DIR / "arial.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Bold", str(FONT_DIR / "arialbd.ttf")))

INK = colors.HexColor("#111111")
GREY = colors.HexColor("#6B7280")
LINE = colors.HexColor("#E5E7EB")
SOFT = colors.HexColor("#F7F7F7")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="Kicker", fontName="Arial-Bold", fontSize=7.5, leading=10,
    textColor=GREY, spaceAfter=5, tracking=1.2,
))
styles.add(ParagraphStyle(
    name="Name", fontName="Arial-Bold", fontSize=33, leading=35,
    textColor=INK, spaceAfter=4,
))
styles.add(ParagraphStyle(
    name="Role", fontName="Arial-Bold", fontSize=13, leading=17,
    textColor=INK, spaceAfter=9,
))
styles.add(ParagraphStyle(
    name="Body", fontName="Arial", fontSize=9.2, leading=14,
    textColor=GREY, spaceAfter=7,
))
styles.add(ParagraphStyle(
    name="Section", fontName="Arial-Bold", fontSize=13, leading=16,
    textColor=INK, spaceBefore=7, spaceAfter=9,
))
styles.add(ParagraphStyle(
    name="Project", fontName="Arial-Bold", fontSize=10, leading=13,
    textColor=INK, spaceAfter=3,
))
styles.add(ParagraphStyle(
    name="Small", fontName="Arial", fontSize=8, leading=11,
    textColor=GREY,
))
styles.add(ParagraphStyle(
    name="Stat", fontName="Arial-Bold", fontSize=16, leading=18,
    textColor=INK, alignment=TA_LEFT,
))
styles.add(ParagraphStyle(
    name="StatLabel", fontName="Arial", fontSize=7.3, leading=9,
    textColor=GREY,
))
styles.add(ParagraphStyle(
    name="Contact", fontName="Arial", fontSize=8.5, leading=13,
    textColor=INK,
))


def p(text, style="Body"):
    return Paragraph(text, styles[style])


def section(title):
    return [Spacer(1, 5), p(title.upper(), "Section")]


def footer(canvas, doc):
    canvas.saveState()
    width, _ = A4
    canvas.setStrokeColor(LINE)
    canvas.line(18 * mm, 13 * mm, width - 18 * mm, 13 * mm)
    canvas.setFillColor(GREY)
    canvas.setFont("Arial", 7.5)
    canvas.drawString(18 * mm, 8 * mm, "ALINA - AI & FULL-STACK DEVELOPER")
    canvas.drawRightString(width - 18 * mm, 8 * mm, f"{doc.page}")
    canvas.restoreState()


def project(title, description, stack, link=None):
    parts = [p(title, "Project"), p(description, "Small"), p(stack, "Small")]
    if link:
        parts.append(p(link, "Small"))
    return KeepTogether(parts + [Spacer(1, 8)])


def build():
    doc = BaseDocTemplate(
        str(PDF), pagesize=A4,
        leftMargin=18 * mm, rightMargin=18 * mm,
        topMargin=15 * mm, bottomMargin=18 * mm,
        title="Алина - AI & Full-Stack Developer",
        author="Алина",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates([PageTemplate(id="resume", frames=[frame], onPage=footer)])
    story = []

    story += [
        p("DEVOPIX / РЕЗЮМЕ", "Kicker"),
        p("Алина", "Name"),
        p("AI &amp; Full-Stack Developer", "Role"),
        p("После окончания колледжа по специальности «Разработчик веб- и мультимедийных приложений» ушла во фриланс, где создаю веб-приложения, AI-сервисы и автоматизацию для клиентов."),
    ]

    contact = Table([
        [p("Telegram", "Small"), p("@ave6atan", "Contact"), p("Email", "Small"), p("gntv.surname@gmail.com", "Contact")],
        [p("GitHub", "Small"), p("github.com/AlinaGntv", "Contact"), p("Сайт", "Small"), p("alinagntv.github.io/resume", "Contact")],
    ], colWidths=[18 * mm, 57 * mm, 15 * mm, 68 * mm])
    contact.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SOFT),
        ("BOX", (0, 0), (-1, -1), 0.4, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story += [contact]

    story += section("Ключевые цифры")
    stats = Table([
        [p("10+", "Stat"), p("2 000+", "Stat"), p("400", "Stat"), p("20 000 ₽", "Stat")],
        [p("завершённых проектов", "StatLabel"), p("запусков бота", "StatLabel"), p("зарегистрированных в веб-приложении", "StatLabel"), p("за 1 месяц со своего проекта", "StatLabel")],
    ], colWidths=[39.5 * mm] * 4)
    stats.setStyle(TableStyle([
        ("LINEABOVE", (0, 0), (-1, 0), 1.2, INK),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story += [stats]

    story += section("Направления и стек")
    story += [p("AI и LLM-интеграции  |  Web Development  |  Telegram Bots и Web Apps  |  Automation  |  UI/UX  |  DevOps", "Body")]
    stack = "Python, Aiogram, Node.js, TypeScript, PHP, Laravel, React, Next.js, JavaScript, PostgreSQL, MySQL, Prisma, WebSockets, Make, REST API, Webhooks, Docker, Nginx, Linux, Telegram API, LLM."
    story += [p(stack, "Small")]

    story += section("Опыт")
    story += [
        p("2025-2026  |  Фриланс-разработчик", "Project"),
        p("Разрабатываю продукты с нуля, Telegram-боты и веб-сервисы. Настраиваю интеграции, автоматизации, серверную часть и деплой."),
    ]

    story += section("Лучшие проекты")
    story += [
        project("AI-сервис анализа внешности", "Telegram-бот с анализом фото через LLM, который вырос в веб-приложение с серверной логикой и потенциалом масштабирования.", "Python, Aiogram, React, Next.js, LLM", "chadmetrix.ru"),
        project("Драфт-система для строительной бригады", "Real-time распределение рабочих между прорабами: квоты, 45-секундные таймауты, планирование по часовому поясу Sacramento, уведомления в Telegram и история драфтов.", "Node.js, TypeScript, React, Fastify, Prisma, PostgreSQL, WebSockets, Docker", "github.com/AlinaGntv/dm-draft"),
        project("Сервис заказа одежды по меркам", "Веб-приложение с личным кабинетом, системой заказов, базой данных и административной панелью - полноценный прототип сервиса.", "Laravel, PHP, MySQL, Docker", "github.com/AlinaGntv/merkaru"),
    ]

    story.append(PageBreak())
    story += [p("ПРОЕКТЫ И ИНТЕРЕСЫ", "Kicker"), p("Дополнительные кейсы", "Name")]
    story += [
        project("Доработка интернет-магазина", "Разобралась в PHP + MySQL архитектуре CMS и доработала алгоритм формирования путей к изображениям товаров на основе ID.", "PHP, MySQL, Moguta CMS, HTML", "izs-pro.ru"),
        project("Настройка VPS-сервера", "Настройка удалённого сервера для размещения проектов, веб-сервера Nginx, запуска приложений и SSH-доступа.", "VPS, Nginx, Linux, SSH"),
        project("Автоматизация маркетинга", "Передача UTM-меток с сайта в Telegram, автоматизация через Make и кастомный JavaScript для сбора данных.", "JavaScript, Make, Tilda, Webhooks", "double-move.com"),
        project("Telegram Web App для расписания команды", "Внутренний инструмент для команды из 10 человек: еженедельная рассылка, выбор доступных дней и запись в Google Sheets.", "JavaScript, Make, Telegram API, Google Sheets, Webhooks"),
        project("CRM, телефония и Telegram", "Настройка API-синхронизации и сценария RingCentral -> Telegram: пропущенные звонки и транскрипции voicemail попадают в рабочий чат.", "REST API, RingCentral API, Gmail API, Make, Telegram Bot API"),
        project("Боты, платежи и аналитика", "Доработка Telegram-бота с подпиской и интеграцией Robokassa; сбор дашборда с несколькими источниками данных.", "Python, Robokassa, Klipfolio, Google Ads API"),
    ]

    story += section("Что ищу")
    story += [p("Ищу команду, где смогу развивать AI-продукты, веб-сервисы и автоматизацию. Особенно интересны продуктовые компании и стартапы.")]
    story += section("Сильные стороны")
    story += [p("Быстро осваиваю новые технологии. Люблю запускать проекты с нуля, собирать MVP и автоматизировать процессы. Веду YouTube и участвую в pet-проектах.")]
    story += section("Контакты")
    story += [p("Telegram: @ave6atan  |  Email: gntv.surname@gmail.com  |  GitHub: github.com/AlinaGntv  |  TikTok: @ave6atan  |  Instagram: @ave6atan", "Contact")]

    doc.build(story)
    print(PDF)


if __name__ == "__main__":
    build()
