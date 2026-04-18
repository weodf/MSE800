class Student:
    def __init__(self, name, age, student_id):
        self.name = name
        self.age = age
        self.student_id = student_id


def collect_students(total_students):
    students = []

    for number in range(1, total_students + 1):
        print(f"Enter details for student {number}:")
        name = input("Name: ").strip()
        age = int(input("Age: ").strip())
        student_id = input("Student ID: ").strip()
        students.append(Student(name, age, student_id))
        print()

    return students


def print_student_names_and_ages(students):
    students = sorted(students, key=lambda student: student.age, reverse=False)
    print("Student names and ages in order:")
    for student in students:
        print(f"Name: {student.name}, Age: {student.age}")


if __name__ == "__main__":
    number_of_students = int(input("How many students do you want to collect? ").strip())
    student_list = collect_students(number_of_students)
    print_student_names_and_ages(student_list)
