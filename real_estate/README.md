Клонируй репозиторий на локальную машину:

git clone https://github.com/ZednB/real_estate_scrapy.git
cd real_estate

Создай виртуальное окружение (рекомендуется):
python3 -m venv venv
source venv/bin/activate

Установи зависимости:
pip install -r requirements.txt

Запуск
Чтобы начать сбор данных, используй Scrapy:
scrapy crawl estate #Либо scrapy crawl estate -o <название файла>