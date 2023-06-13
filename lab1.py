import mysql.connector

cnx = mysql.connector.connect(
    host='localhost',
    user='root',
    password='admin',
    database='lab1Db'
)

try: 
    cursor = cnx.cursor()

    # створюємо бд
    cursor.execute('CREATE DATABASE IF NOT EXISTS lab1Db')

    # світчимось на неї
    cursor.execute('USE lab1Db')

    # створюємо таблицю зі студентами
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255),
            age INT,
            email VARCHAR(255)
        )
    ''')

    # Додаємо 5 студентів
    students = [
        ('John Doe', 20, 'john@example.com'),
        ('Jane Smith', 22, 'jane@example.com'),
        ('Mike Johnson', 21, 'mike@example.com'),
        ('Sarah Brown', 19, 'sarah@example.com'),
        ('David Wilson', 23, 'david@example.com')
    ]
    cursor.executemany('INSERT INTO students (name, age, email) VALUES (%s, %s, %s)', students)

    # Коммітимо зміни 
    cnx.commit()

    # Вибираємо усії студентів
    cursor.execute('SELECT * FROM students')

    rows = cursor.fetchall()

    # Виводимо дані в консоль
    for row in rows:
        print(row)

    # Запит на вибірку студенту за іменем
    query = "SELECT * FROM students WHERE name = %s"
    name = "John Doe"
    cursor.execute(query, (name,))

    row = cursor.fetchone()

    if row:
        print("Student found:")
        print("ID:", row[0])
        print("Name:", row[1])
        print("Age:", row[2])
        print("Email:", row[3])
    else:
        print("Student not found.")

    # Запит на оновлення віку студента за іменем
    query = "UPDATE students SET age = %s WHERE name = %s"
    new_age = 25 
    name = "John Doe"
    cursor.execute(query, (new_age, name))

    cnx.commit()

    # Перевірка на кількість оновлених документів
    if cursor.rowcount > 0:
        print("Age updated successfully.")
    else:
        print("No student found with the specified name.")

    # Execute a DELETE query to remove a student by ID
    query = "DELETE FROM students WHERE id = %s"
    student_id = 3
    cursor.execute(query, (student_id,))

    cnx.commit()

    # Перевірка на кількість оновлених документів
    if cursor.rowcount > 0:
        print("Student deleted successfully.")
    else:
        print("No student found with the specified ID.")

    try:
        cnx.start_transaction()
        query = "INSERT INTO students (name, age, email) VALUES (%s, %s, %s)"
        student1 = ('Alex Johnson', 20, 'alex@example.com')
        cursor.execute(query, student1)

        student2 = ('Emily Brown', 21, 'emily@example.com')
        cursor.execute(query, student2)
        cnx.commit()

        print("Students added successfully.")

    except mysql.connector.Error as error:
        print("An error occurred. Changes canceled.")
        print("Error message:", error.msg)
        cnx.rollback()


    courses = [
        ('Mathematics', 'Advanced calculus', 4),
        ('Computer Science', 'Introduction to programming', 3),
        ('Physics', 'Quantum mechanics', 5)
    ]

    query = "INSERT INTO courses (name, description, credits) VALUES (%s, %s, %s)"
    cursor.executemany(query, courses)

    cnx.commit()

    print("Courses added successfully.")

    student_courses = [
        (1, 1),  # Student with ID 1 chose Course with ID 1
        (1, 2),  # Student with ID 1 chose Course with ID 2
        (2, 2),  # Student with ID 2 chose Course with ID 2
        (3, 3),  # Student with ID 3 chose Course with ID 3
        (3, 1)   # Student with ID 3 chose Course with ID 1
    ]

    query = "INSERT INTO student_courses (student_id, course_id) VALUES (%s, %s)"
    cursor.executemany(query, student_courses)

    cnx.commit()

    print("Data added to student_courses table successfully.")

    # Запит для виведення усіх студентів, які записані на даний курс
    course_id = 2
    query = '''
        SELECT s.id, s.name
        FROM students s
        JOIN student_courses sc ON s.id = sc.student_id
        WHERE sc.course_id = %s
    '''
    cursor.execute(query, (course_id,))

    students = cursor.fetchall()

    if students:
        print(f"Students enrolled in course with ID {course_id}:")
        for student in students:
            student_id, student_name = student
            print(f"ID: {student_id}, Name: {student_name}")
    else:
        print("No students found for the specified course.")

    #Запит для введення усіх курсів певного студента
    student_name = 'John Smith'
    query = '''
        SELECT c.id, c.name, c.description, c.credits
        FROM courses c
        JOIN student_courses sc ON c.id = sc.course_id
        JOIN students s ON s.id = sc.student_id
        WHERE s.name = %s
    '''
    cursor.execute(query, (student_name,))

    courses = cursor.fetchall()

    if courses:
        print(f"Courses chosen by student '{student_name}':")
        for course in courses:
            course_id, course_name, course_description, course_credits = course
            print(f"ID: {course_id}, Name: {course_name}")
            print(f"Description: {course_description}")
            print(f"Credits: {course_credits}")
            print()
    else:
        print("No courses found for the specified student.")


    # Запит для виведення усіх студентів і всіх курсів, на які вони записані
    query = '''
        SELECT s.id, s.name AS student_name, c.id AS course_id, c.name AS course_name
        FROM students s
        JOIN student_courses sc ON s.id = sc.student_id
        JOIN courses c ON c.id = sc.course_id
    '''
    cursor.execute(query)

    records = cursor.fetchall()

    if records:
        print("Students and their enrolled courses:")
        current_student_id = None
        for record in records:
            student_id, student_name, course_id, course_name = record
            if student_id != current_student_id:
                print(f"Student ID: {student_id}, Name: {student_name}")
                print(f"Enrolled Courses:")
                current_student_id = student_id
            print(f"Course ID: {course_id}, Course Name: {course_name}")
            print()
    else:
        print("No records found.")

finally:
    cnx.close()
    returnText = input ("Enter any symbol to stop execution of programm: ")