class Student:
    def __init__(self, name, subject, year_group, gpa):
        self.name = name
        self.subject = subject
        self.year_group = year_group
        self.gpa = gpa



    def on_scholarship_roll(self):
        if self.gpa >= 3.5:
            return True
        else:
            return False
        



