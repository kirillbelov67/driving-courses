from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# Загрузка данных из файла при запуске сервера
try:
    with open('schedules.json', 'r') as f:
        schedules_data = json.load(f)
except FileNotFoundError:
    schedules_data = {"schedules": []}

try:
    with open('students.json', 'r') as f:
        students_data = json.load(f)
except FileNotFoundError:
    students_data = {"students": []}

@app.route('/schedule', methods=['POST'])
def add_schedule():
    data = request.get_json()
    
    # Проверяем наличие обязательных полей
    required_fields = ['instructor', 'date', 'start_time', 'end_time', 'max_students']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Не все обязательные поля заполнены'}), 400
    
    # Проверяем формат даты
    try:
        date = datetime.strptime(data['date'], '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Неверный формат даты. Должен быть YYYY-MM-DD.'}), 400
    
    # Проверяем формат времени
    try:
        start_time = datetime.strptime(data['start_time'], '%H:%M').time()
        end_time = datetime.strptime(data['end_time'], '%H:%M').time()
    except ValueError:
        return jsonify({'error': 'Неверный формат времени. Должен быть HH:MM.'}), 400
    
    # Проверяем, чтобы начало было раньше конца
    if start_time >= end_time:
        return jsonify({'error': 'Время начала должно быть раньше времени окончания.'}), 400
    
    # Проверяем максимальное количество студентов
    if not isinstance(data['max_students'], int) or data['max_students'] <= 0:
        return jsonify({'error': 'Максимальное количество студентов должно быть положительным числом.'}), 400
    
    # Все проверки пройдены, добавляем новое расписание
    schedule_id = len(schedules_data['schedules']) + 1
    data['id'] = schedule_id
    schedules_data['schedules'].append(data)
    
    # Сохраняем изменения в файл
    with open('schedules.json', 'w') as f:
        json.dump(schedules_data, f, indent=2)
    
    return jsonify({"message": "Расписание добавлено успешно."}), 201

@app.route('/student', methods=['POST'])
def register_student():
    data = request.get_json()
    
    # Проверяем наличие обязательных полей
    required_fields = ['first_name', 'last_name', 'email', 'phone_number']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Не все обязательные поля заполнены'}), 400
    
    # Проверяем формат email
    if '@' not in data['email']:
        return jsonify({'error': 'Некорректный формат email.'}), 400
    
    # Проверяем формат телефона
    if not data['phone_number'].isdigit() or len(data['phone_number']) != 10:
        return jsonify({'error': 'Некорректный формат номера телефона. Должны быть 10 цифр.'}), 400
    
    # Все проверки пройдены, регистрируем студента
    student_id = len(students_data['students']) + 1
    data['id'] = student_id
    students_data['students'].append(data)
    
    # Сохраняем изменения в файл
    with open('students.json', 'w') as f:
        json.dump(students_data, f, indent=2)
    
    return jsonify({"message": "Ученик зарегистрирован успешно."}), 201

if __name__ == '__main__':
    app.run(debug=True)
    
