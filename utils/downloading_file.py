import requests
from urllib.parse import urlencode
import docx2txt
import asyncio
import os
from aiogram.types import FSInputFile
from db import Database
from datetime import datetime
import aspose.words as aw
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

class SendScheduleImage:
    def __init__(self):
        self.page_mapping = {
            "5а": "image1.png",
            "5б": "image1.png",
            "5в": "image1.png",
            "5г": "image1.png",
            "5д": "image1.png",
            "5е": "image1.png",
            "5ж": "image1.png",
            "5з": "image1.png",
            "6а": "image1.png",
            "6б": "image1.png",
            "6в": "image2.png",
            "6г": "image2.png",
            "6д": "image2.png",
            "6е": "image2.png",
            "6ж": "image2.png",
            "6и": "image2.png",
            "7а": "image2.png",
            "7б": "image2.png",
            "7в": "image2.png",
            "7г": "image2.png",
            "7д": "image3.png",
            "7ж": "image3.png",
            "7з": "image3.png",
            "8а": "image3.png",
            "8б": "image3.png",
            "8в": "image3.png",
            "8г": "image3.png",
            "8д": "image3.png",
            "8е": "image3.png",
            "9а": "image3.png",
            "9б": "image4.png",
            "9в": "image4.png",
            "9г": "image4.png",
            "9д": "image4.png",
            "9е": "image4.png",
            "10а": "image4.png",
            "10б": "image4.png",
            "11а": "image4.png",
        }

        self.file_name = "schedule"
        self.folder_path = "temp"
        self.file_path = f"{self.folder_path}/{self.file_name}.docx"
        os.makedirs(self.folder_path, exist_ok=True)

    def download_file(self, output_file):
        """Скачивает файл с сайта с расписанием и сохраняет в директории

        Args:
            output_file (str): название файла, который нужно скачать

        Returns:
            str: folder_path/output_file.docx
        """
        base_url = "https://cloud-api.yandex.net/v1/disk/public/resources/download?"
        public_key = "https://yadi.sk/d/KFhrI27am7MG9g"

        final_url = base_url + urlencode({"public_key": public_key})
        response = requests.get(final_url)
        download_url = response.json()["href"]

        download_response = requests.get(download_url)
        with open((self.folder_path + "/" + output_file + ".docx"), "wb") as f:
            f.write(download_response.content)
        return self.folder_path + "/" + output_file + ".docx"

    def get_images_from_docx(self):
        """
        Достаёт фото из файла с расписанием.
        """
        
        docx2txt.process(self.file_path, self.folder_path)
    
    def compare_docx(self, file1, file2) -> bool:
        """
        Сравнивает два файла на наличие различий.
        Возвращает bool.
        """
        
        doc1 = aw.Document(file1)
        doc2 = aw.Document(file2)

        doc1.compare(doc2, "user", datetime.today())
        return doc1.revisions.count > 0

    async def check_new_schedule(self, bot, db):
        """Проверяет наличие нового расписания"""
        self.get_images_from_docx()

        while True:
            logging.info("Проверка нового расписания")
            
            if os.path.exists(self.file_path):
                file2 = self.download_file(self.file_name + '1')
                if os.path.exists(file2) and self.compare_docx(self.file_path, file2):
                    logging.info('Файлы не идентичны')
                    os.remove(self.file_path)
                    os.rename(file2, self.file_path)

                    for file_name in os.listdir(self.folder_path):
                        if "image" in file_name:
                            file_path = os.path.join(self.folder_path, file_name)
                            if os.path.isfile(file_path):
                                os.remove(file_path)
                    self.get_images_from_docx()

                    await self.send_schedule_images_for_all(bot, db)
                    logging.info("Расписание отправлено успешно!")
                    continue
                else:
                    logging.info('Файлы идентичны')
                    os.remove(file2)
            else:
                logging.warning("Нет файла с расписанием!")
            
            await asyncio.sleep(599) # Ждёт 10 минут
        
    def get_image_name(self, grade):
        return f"{self.folder_path}/{self.page_mapping.get(grade)}"

    async def send_schedule_images_for_all(self, bot, db):
        users = db.get_active_users()
        groups = db.get_groups()
        # groups = [(-1002129798501, 9, 'А'),]
        for _, user in enumerate(users):
            try:
                await bot.send_photo(
                    chat_id=user[0],
                    photo=FSInputFile(
                        self.get_image_name(str(user[1]) + str(user[2]).lower())
                    ),
                    caption="Доступно новое расписание!",
                )
            except Exception as e:
                logging.warning(e)
        logging.info("Расписание для пользователей успешно отправлено")
        for _, group in enumerate(groups):
            try:
                await bot.send_photo(
                    chat_id=group[0],
                    photo=FSInputFile(self.get_image_name(str(group[1]) + str(group[2]).lower())),
                    caption="Доступно новое расписание!"
                )
            except Exception as e:
                logging.warning(e)
        logging.info("Расписание для групп успешно отправлено")
    
    async def send_schedule_images_for_one(self, message, db, user_id):
        user = db.get_user_for_schedule(user_id)
        if user:
            try:
                await message.answer_photo(
                    photo=FSInputFile(
                        self.get_image_name(str(user[1]) + str(user[2]).lower())
                    )
                )
            except Exception as e:
                logging.warning(e)
        else:
            logging.error("User not found")
