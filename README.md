# Kaspersky Security Center database tables parser
Скрипт предназаначен для парсинга результирующих файлов (all_tables_sizes)

## Использование
### Скрипт и результирующие файлы должны быть в едином каталоге, пример структуры каталога:
- alts_parser.exe
- result.xml
- result-1.xml
- result-2.xml
- ...
- result-11.xml

### При запуске парсера данные предоставляются в формате (консольный вывод):
<details>
  <summary>Нажмите, чтобы раскрыть</summary>
  
- СУБД
- Обновления/версия
- Наименование БД
- Владелец
- Дата создания БД

- Максимальный размер БД
- Текущий размер БД

- Топ-10 таблиц по размеру (единица: МБ)
- Топ-10 событий хранимых в базе данных
</details>

## Как получить результирующие файлы
### Результирующие файлы - это выгрузка из базы данных Kaspersky Security Center, предоставляются .xml-файлы с выгрузкой таблиц
### Для получения файлов необходимо:
- Загрузить .sql-файлы [all_tables_sizes](https://media.kaspersky.com/utilities/CorporateUtilities/all_tables_sizes.zip) для создания запроса к базе данных
- При помощи утилиты [klsql2](https://support.kaspersky.ru/ksc/15.1/151343?page=help) создать запрос к базе данных KSC


### Пример запроса к базе данных KSC (MSSQL) через klsql2:
cd "C:\Program Files (x86)\Kaspersky Lab\Kaspersky Security Center"

.\klsql2 -i all_tables_sizes_mssqlsrv.sql -o result.xml

### Проверено со следующими СУБД KSC:
- Microsoft SQL (MSSQL)
- PostgreSQL
- MariaDB
- MySQL
