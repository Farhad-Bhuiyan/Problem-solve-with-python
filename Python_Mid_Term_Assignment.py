class StudentDatabase:
    student_list=[]
    
    @classmethod
    def add_student(cls,student):
        cls.student_list.append(student)
        
    
class Student():
    
    def __init__(self,student_id,name,department,is_enrolled):
        self._student_id=student_id
        self._name=name
        self._department=department
        self._is_enrolled=is_enrolled
        StudentDatabase.add_student(self)
    
    def enroll_student(self):
        if self._is_enrolled:
            print(f"Error: The student {self._name} is already enrolled.")
        else:
            self._is_enrolled=True
            print(f"The student {self._name} is successfully enrolled now.")
            
    def drop_student(self):
        if not self._is_enrolled:
            print(f"Error: The student {self._name} is currently not enrolled.")
        else:
            self._is_enrolled=False
            print(f"The student {self._name} is dropped Successfully.")
            
    
    def view_student_info(self):
        print("The Student Information:- ")
        print("Student ID: ",self._student_id)
        print("Student Name: ",self._name)
        print("Student Department: ",self._department)
        if self._is_enrolled:
            print("Enrollment Status: Enrolled")
        else:
            print("Enrollment Status: Not Enrolled")
        
        print("----------------------------")
        
         
Farhad = Student(241002017,"Farhad Bhuiyan","CSE",True)
Sowmik = Student(241002002,"MD. Jawadul Hassan Sowmik","CSE",False)
Maheer = Student(241002003,"Maheer Jabin Priya","CSE",True)
Shakil = Student(241002006,"Nur Mohammad Shakil","CSE",False)
Ziham = Student(241002007,"Ziham Mahamud","CSE",True)



while True:
    print("------------------------------")
    print("Using the Student Database: - ")
    print("1. View All Students")
    print("2. Enroll Student")
    print("3. Drop Student")
    print("4. Exit")
    
    chose=input("Chose an Option:- ")
    
    if chose=="1":
        
        if len(StudentDatabase.student_list)==0:
            print("There is no student information.")
        else:
            for student in StudentDatabase.student_list:
                student.view_student_info()
    elif chose=="2":
        try:
            id = int(input("Enter the ID: ")) 
        except ValueError:
            print("Please Enter a valid numeric ID.")
            continue
            
        found=False
        for student in StudentDatabase.student_list:
            if student._student_id==id:
                found=True
                student.enroll_student()
                break
        
        if not found:
            print("Invalid Student ID.")
    elif chose=="3":
        try:
            id = int(input("Enter the ID: ")) 
        except ValueError:
           print("Please Enter a valid numeric ID.")
           continue
        found=False
        for student in StudentDatabase.student_list:
            if student._student_id==id:
                found=True
                student.drop_student()
                break
                
        if not found:
            print("Invalid Student ID.")
    elif chose=="4":
        print("Thanks for using, the system is closed now.")
        break
    else:
        print("Invalid input, please give something in between (1-4).")
                