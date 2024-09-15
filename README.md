# Number Plates Parking Management

Цей проєкт — це Система Управління Паркінгом, створена з використанням Django. Вона включає функціонал авторизації користувачів, управління тарифами на паркування та систему розпізнавання номерних знаків, інтегровану з моделлю машинного навчання для зчитування номерів з фотографій.

## Вміст

1. [Основні функції](#Основніфункції)
2. [Технологічний стек](#Технологічнийстек)
3. [Інсталяція](#Інсталяція)
4. [Використання](#використання)
5. [Data Science](#DataScience)
6. [Авторизація](#авторизація)
7. [Безпека](#безпека)
8. [Ліцензія](#ліцензія)

## Основні функції

- Авторизація користувачів:
  Реєстрація, вхід в систему, зміна пароля.
- Розпізнавання номерних знаків:
  Завантажте зображення автомобіля, і система автоматично розпізнає та зчитає номерний знак за допомогою машинного навчання.
- Управління тарифами та правилами паркування:
  Перегляд тарифів на паркування та правил для інформування користувачів.
- Меню для зареєстрованих користувачів:
  Після входу в систему користувачі можуть отримати доступ до персоналізованих опцій, таких як перевірка номерного знаку автомобіля тощо.

## Технологічний стек:

- python = "^3.12"
- django = "^5.1.1"
- psycopg2 = "^2.9.9"
- pydantic-settings = "^2.4.0"
- matplotlib = "^3.9.2"
- opencv-python = "^4.10.0.84"
- tensorflow = "^2.17.0"
- tensorflow-intel = "^2.17.0"
- keras = "^3.5.0"

## Інсталяція

1. Клонуйте репозиторій:

   ```bash
   git clone https://github.com/Alex-Tsyb/Number_plates_project
   cd number_paltes/

2. Instalation in consol: 
    create .env
    poetry install.
    docker run --name number_plates_prohect -p 5532:5432 -e POSTGRES_PASSWORD=changeme -d postgres
    poetry shell

3. Navigate to the project directory:
cd Number_plates_project/number_plates

4. Run the application:
python manage.py migrate
python manage.py runserver

5. Run in localhost:8000/:


## Використання
Після встановлення та запуску проекту ви зможете:

Відвідайте головну сторінку, увійдіть або зареєструйтесь.
Завантажте зображення автомобіля для автоматичного розпізнавання номерного знака.
Огляньте доступні варіанти паркування, перегляньте тарифи та дотримуйтесь правил для безпечного паркування.

## Data Science

Система використовує OpenCV та Tesseract для розпізнавання номерних знаків автомобілів на зображеннях. Ця функція дозволяє обробляти зображення автомобілів, зчитувати номерний знак та пов'язувати його з обліковими записами користувачів.

## Авторизація
Для доступу до функціоналу потрібно авторизуватись. Користувачі можуть створювати облікові записи та відновлювати паролі через email.

## Безпека
Всі критичні дані, такі як налаштування бази даних та інші конфіденційні дані, зберігаються у змінних середовищах і не зберігаються в репозиторії проекту.

## Ліцензія
This project is licensed under the BSD 2-Clause License.