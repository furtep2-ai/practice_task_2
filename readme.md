* Сервис обновления заметки

### РОУТ
* GET /notes/{note_id}

### Описание 
* Цель: Вовзращает заметку

### Пармаетры пути 
* note_id = integer, id заметки

### Тело запроса
json
{
  "text": "Новый текст заметки",
  "version": 1
}

### Валидация NoteChange 

* text(str)
* Текст заметки
* Ограничения `min_length=1`, `max_length=200`.
* `strip_whitespace=True` убирает все пустые пробелы в начале и в конце

* version(int)
* Версия заметки
* gt=0 не позволяет version быть ниже нуля

### Ошибка 422
* Если тело запроса не соответствует схемам (например, передан пустой текст или версия меньше 1).
{
  "detail": [
    {
      "loc": ["body", "text"],
      "msg": "String should have at least 1 characters",
      "type": "string_too_short",
      "input": ""
    },
    {
      "loc": ["body", "version"],
      "msg": "Input should be greater than 0",
      "type": "greater_than",
      "input": 0
    }
  ]
}

### Кейсы
1. Успешная выдача заметки - 200 
* Возвращает текущую заметку с параметрами id, text и version.
{
    "id": 1
    "text": "Текст",
    "version": 1
}
2. Отсуствие заметки в бд - 404
Возвращает ошибку 404 с сообщение 
{
  "detail": "Not found note"
}

### РОУТ
* PATCH /notes/{note_id}

### Описание 
* Обновление заметки. Если версия заметки в базе данных отличается от отправленной, возвращает конфликт.

### Пармаетры пути 
* note_id = integer, id заметки

### Тело запроса
json
{
  "text": "Новый текст заметки",
  "version": 1
}

### Кейсы
1. Успешное обновление заметки - 200 
* Возвращает сохраненный результат
json
{
    "text": update_note.text, 
    "version": update_note.version
}
