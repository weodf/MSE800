student1 = {
    "name": "Alex",
    "age": 42,
    "course": "Data Analytics",
    "city": "Auckland",
    "status": "Lecturer"
}

student2 = {
    "name": "Sophia",
    "age": 29,
    "course": "Software Engineering",
    "city": "Wellington",
    "status": "Student"
}

student3 = {
    "name": "Michaela",
    "age": 35,
    "course": "Cyber Security",
    "city": "Christchurch",
    "status": "Researcher"
}

def main():
    students = [student1, student2, student3]
    merged_students = []

    for student in students:
        if "azw" in student["name"].lower():
            merged_students.append(student)

    print("Students with name containing 'azw':")
    print(merged_students)



if __name__ == "__main__":
    main()