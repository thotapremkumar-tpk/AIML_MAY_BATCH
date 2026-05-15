def analyze_result(name, roll, marks):
    total = sum(marks)
    average = total / len(marks)

    if average >= 90:
        grade = "A"
    elif average >= 75:
        grade = "B"
    elif average >= 60:
        grade = "C"
    elif average >= 40:
        grade = "D"
    else:
        grade = "Fail"

    print(f"Student: {name} (Roll: {roll})")
    print(f"Total: {total}, Average: {average}")
    print(f"Grade: {grade}")

    failed_subjects = []

    for i in range(len(marks)):
        if marks[i] < 40:
            failed_subjects.append(f"Subject {i + 1}")

    if failed_subjects:
        print("Subjects below 40:", ", ".join(failed_subjects))
    else:
        print("No subjects below 40")


name = "Aarav"
roll = 101
marks = [88.5, 35.0, 76.0, 92.5, 48.0]

analyze_result(name, roll, marks)