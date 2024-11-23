from PIL import Image, ImageDraw, ImageFont
import textwrap

class ScheduleImage:
    def __init__(self, schedule):
        self.schedule = schedule

    def generate_image(self, grade: str, date: str, weekday: str):
        block_height = 80
        header_height = 100      
        width, height = 650, (header_height + len(self.schedule[grade]) * block_height)

        for lesson in self.schedule[grade]:
            if len(lesson["lesson"]) > 15:
                height += 35
            if len(lesson["lesson"]) > 30:
                height += 70

        background_color = (30, 30, 30)
        img = Image.new('RGB', (width, height), color=background_color)
        draw = ImageDraw.Draw(img)

        font_title = ImageFont.truetype("./fonts/Montserrat ExtraBold 800.ttf", 40)
        font_lesson = ImageFont.truetype("./fonts/Montserrat Regular 400.ttf", 28)
        font_time = ImageFont.truetype("./fonts/Montserrat SemiBold 600.ttf", 25)
        font_room = ImageFont.truetype("./fonts/Montserrat Regular 400.ttf", 20)

        draw.text((50, 15), f"{date}, {weekday}", font=font_title, fill=(244, 244, 244))
        draw.line((0, 80, width, 80), fill=(244, 244, 244), width=3)

        y_text = 100
        line_offset = block_height // 16

        for index, item in enumerate(self.schedule[grade]):
            draw.text((50, y_text), str(index + 1), font=font_lesson, fill=(200, 200, 200))

            lesson_text = textwrap.fill(item["lesson"], width=15)

            if lesson_text.count('\n') != 0:
                draw.multiline_text((100, y_text), lesson_text, font=font_lesson, fill=(200, 200, 200), spacing=5)
                y_text += 35 * lesson_text.count('\n')
            else:
                draw.text((100, y_text), item["lesson"], font=font_lesson, fill=(200, 200, 200))

            draw.text((100, y_text + 35), item["time"], font=font_time, fill=(255, 255, 255))

            if item["room"] != "":
                draw.text((400, y_text + 35), f"Кабинет: {item['room']}", font=font_room, fill=(255, 255, 255))

            y_text += block_height

            if index < len(self.schedule[grade]) - 1: 
                draw.line((40, y_text - line_offset, 560, y_text - line_offset), fill=(80, 80, 80), width=1)

        image_path = f"./temp/{date}-{grade}.png"
        img.save(image_path)

        return image_path