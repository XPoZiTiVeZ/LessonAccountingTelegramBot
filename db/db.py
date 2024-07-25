from enum import Enum
from sqlalchemy import create_engine, Column, Integer, String, Text, Date, ForeignKey, Enum, text, BLOB
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.exc import IntegrityError
from datetime import date

URL = "sqlite:///db.db"
engine = create_engine(url=URL)

Base = declarative_base()
Session = sessionmaker(engine, expire_on_commit=False)

class SameUserException(Exception):
    "You're trying to add user to the same user"

class TeacherNotExist(Exception):
    "Teacher does not exits"
    
class StudentNotExist(Exception):
    "Student does not exist"

class EntryAlreadyExists(Exception):
    "The entry already exists"
    
class EntryNotExist(Exception):
    "The entry does not exist"

class Association(Base):
    __tablename__ = 'teacher_student'
    association_id = Column(String(21), primary_key=True)
    teacher_id = Column(Integer, ForeignKey('User.user_id', ondelete='RESTRICT'))
    student_id = Column(Integer, ForeignKey('User.user_id', ondelete='RESTRICT'))
    
    @staticmethod
    def get(association_id: str):
        association_id = str(association_id)
        with Session.begin() as session:
            association = session.get(Association, association_id)
            
            return association
    
    @staticmethod
    def exists(association_id) -> bool:
        association_id = str(association_id)
        if Association.get(association_id) is None:
            return False
        return True
    
    @staticmethod
    def get_all(user_id):
        with Session.begin() as session:
            return session.query(Association).filter(text(f'teacher_student.teacher_id == {user_id} or teacher_student.student_id == {user_id}')).all()
    
    def delete(self):
        with Session.begin() as session:
            users = session.query(User).filter(User.association_id == self.association_id).all()
            for user in users:
                user.association_id = None
                session.add(user)
            session.delete(self)
    
    def __repr__(self):
        return "Association(teacher={}, student={})".format(self.teacher_id, self.student_id)

class User(Base):   
    __tablename__ = "User"
    user_id = Column(Integer, primary_key=True)
    username = Column(String(32))
    first_name = Column(String(64))
    last_name = Column(String(64))
    
    association_id = Column(String(21), ForeignKey('teacher_student.association_id', ondelete="SET NULL"), nullable=True)
    
    @staticmethod
    def add(user_id, username, first_name, last_name):
        with Session.begin() as session:
            user = User(user_id=user_id, username=username, first_name=first_name, last_name=last_name)
            session.add(user)
            return user
    
    @staticmethod
    def get(user_id):
        with Session.begin() as session:
            return session.query(User).get(user_id)
    
    @staticmethod
    def change_association(user, association_id):
        with Session.begin() as session:
            association = Association.get(association_id)
            if association is None:
                raise EntryNotExist
            
            if User.get(association.teacher_id) is None:
                raise TeacherNotExist
            
            if User.get(association.student_id) is None:
                raise StudentNotExist
            
            user.association_id = association_id
            session.add(user)

    @staticmethod
    def update(user, username, first_name, last_name):
        with Session.begin() as session:
            if user.username != username:
                user.username = username
            if user.first_name != first_name:
                user.first_name = first_name
            if user.last_name != last_name:
                user.last_name = last_name
            session.add(user)
    
    
    def add_teacher(self, other):
        if self.user_id == other.user_id:
            raise SameUserException
        
        with Session.begin() as session:
            association = session.query(Association).filter(Association.teacher_id == other.user_id, Association.student_id == self.user_id).first()
            if association is not None:
                raise EntryAlreadyExists
            
            session.add(
                Association(teacher_id=other.user_id, student_id=self.user_id)
            )
    
    def delete_teacher(self, other):
        if self.user_id == other.user_id:
            raise SameUserException
        
        with Session.begin() as session:
            association = session.query(Association).filter(Association.teacher_id == other.user_id, Association.student_id == self.user_id).first()
            if association is None:
                raise EntryNotExist

            session.delete(association)
    
    def teachers(self):
        with Session.begin() as session:
            teachers = session.query(Association).filter(Association.student_id==self.user_id).all()
            return list(map(lambda assoc: session.get(User, assoc.teacher_id), teachers))

    def add_student(self, other):  
        if self.user_id == other.user_id:
            raise SameUserException
        
        with Session.begin() as session:
            association = session.query(Association).filter(Association.teacher_id == self.user_id, Association.student_id == other.user_id).first()
            if association is not None:
                raise EntryAlreadyExists
            
            session.add(
                Association(association_id=f"{self.user_id}<>{other.user_id}", teacher_id=self.user_id, student_id=other.user_id)
            )
    
    def delete_student(self, other):
        if self.user_id == other.user_id:
            raise SameUserException
        
        with Session.begin() as session:
            assoc = session.get(Association, (self.user_id, other.user_id))
            if assoc is None:
                raise EntryNotExist

            session.delete(assoc)
    
    def students(self):
        with Session.begin() as session:
            students = session.query(Association).filter(Association.teacher_id==self.user_id).all()
            return list(map(lambda assoc: session.get(User, assoc.student_id), students))
    
    def lessons(self, month: int | None = date.today().month, year: int = date.today().year):
        if self.association_id is None:
            return []
        
        if month is None:
            return Lesson.get_range(date(year, 1, 1), date(year, 1, 1), self.association_id)

        next_month = 1 if month >= 12 else month + 1
        next_year = year if month < 12 else year + 1
        return Lesson.get_range(date(year, month, 1), date(next_year, next_month, 1), self.association_id)
    
    
    def __repr__(self):
        return "\nUser(id={}, name=\"{}\",\nteachers={},\nstudents={},\nassociation={})".format(
            self.user_id, self.username, 
            list(map(lambda user: user.username, self.teachers())),
            list(map(lambda user: user.username, self.students())),
            self.association_id)

statuses = ["Не состоялось", "Запланировано", "Состоялось"]
class Lesson(Base):
    __tablename__ = "Lesson"
    lesson_id   = Column(Integer, primary_key=True)
    date        = Column(Date)
    description = Column(Text, nullable=True)
    status      = Column(Enum("Не состоялось", "Запланировано", "Состоялось"))

    association_id = Column(String(21), ForeignKey('teacher_student.association_id', ondelete="CASCADE"))
    
    @staticmethod
    def add(date, description, status, association_id):
        with Session.begin() as session:
            lesson = Lesson(date=date, description=description, status=status, association_id=association_id)
            
            session.add(lesson)
            return lesson
    
    @staticmethod
    def get(date, association_id):
        with Session.begin() as session:
            lesson = session.query(Lesson).filter(Lesson.date == date, Lesson.association_id == association_id).first()
            
            return lesson
    
    @staticmethod
    def get_range(start_date, end_date, association_id):
        with Session.begin() as session:
            lessons = session.query(Lesson).filter(Lesson.date >= start_date, Lesson.date < end_date, Lesson.association_id == association_id, Lesson.status == "Состоялось").all()

            return lessons
    
    def change_status(self):
        with Session.begin() as session:
            index = statuses.index(self.status)
            
            if index >= len(statuses)-1:
                self.status = statuses[0]
            else:
                self.status = statuses[index + 1]        
            session.add(self)
    
    def change_description(self, text):
        with Session.begin() as session:
            self.description = text  
            session.add(self)
    
    def add_file(self, file_id, file_name):
        File.add(self.lesson_id, file_id, file_name)
    
    def delete_file(self, file_id):
        File.delete(file_id)
    
    def files(self):
        return File.get_all_files(self.lesson_id)
    
    def __repr__(self):
        association: Association | None = Association.get(self.association_id)
        return "\nLesson(id={}, date={}\n, teacher={}, student={})".format(
            self.lesson_id, self.date,
            None if association is None else association.teacher_id,
            None if association is None else association.student_id,
        )

class File(Base):
    __tablename__ = "File"
    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey('Lesson.lesson_id'))
    file_id = Column(String)
    file_name = Column(String)
    
    @staticmethod
    def get(lesson_id, file_id):
        with Session.begin() as session:
            return session.query(File).filter(File.lesson_id==lesson_id, File.file_id==file_id).first()
    
    @staticmethod
    def get_all_files(lesson_id):
        with Session.begin() as session:
            return session.query(File).filter(File.lesson_id==lesson_id).all()
    
    @staticmethod
    def get_all_lessons(file_id):
        with Session.begin() as session:
            association = session.query(File).filter(File.file_id==file_id)

            return association.all()
    
    @staticmethod
    def add(lesson_id, file_id, file_name):
        if File.get(lesson_id, file_id) is None:
            with Session.begin() as session:
                session.add(File(lesson_id=lesson_id, file_id=file_id, file_name=file_name))
            
    @staticmethod
    def delete(file_id):
        with Session.begin() as session:
            file = session.get(File, file_id)
            if file is not None:
                session.delete(file)
            
def flush():
    Base.metadata.drop_all(bind=engine)

def create_db():
    Base.metadata.create_all(bind=engine)

def main():
    # flush()
    create_db()
    
    # users = [
    #     (randint(1000000000, 9999999999), "BenjaminHunter", "Benjamin", "Hunter"),
    #     (randint(1000000000, 9999999999), "IanMiller", "Ian", "Miller"),
    #     (randint(1000000000, 9999999999), "GabriellePayne", "Gabrielle", "Payne"),
    #     (randint(1000000000, 9999999999), "OwenColeman", "Owen", "Coleman"),
    #     (randint(1000000000, 9999999999), "GabrielleOliver", "Gabrielle", "Oliver"),
    #     (randint(1000000000, 9999999999), "CharlesLewis", "Charles", "Lewis"),
    #     (randint(1000000000, 9999999999), "MollyVance", "Molly", "Vance"),
    #     (randint(1000000000, 9999999999), "PenelopeQuinn", "Penelope", "Quinn"),
    #     (randint(1000000000, 9999999999), "StevenMcLean", "Steven", "McLean"),
    #     (randint(1000000000, 9999999999), "CarolynKing", "Carolyn", "King"),
    # ]

    # ids = list(map(lambda user: user[0], users))
    
    # with Session.begin() as session:
    #     for user in users:
    #         user = User(user_id=user[0], username=user[1], first_name=user[2], last_name=user[3])
    #         session.add(user)
        
    #     association = Association(association_id="123", teacher_id=users[3][0], student_id=users[7][0])
    #     session.add(association)
    
    # with Session.begin() as session:
    #     user1 = session.query(User).get(ids[3])
    #     user2 = session.query(User).get(ids[5])
    #     user3 = session.query(User).get(ids[7])
    #     user4 = session.query(User).get(ids[9])
        
    #     User.change_association(user1, "123")
    # print(User.get(user1.user_id))
    #     user2.add_teacher(user1)
    #     user3.add_student(user4)
    #     user1.add_teacher(user2)
    #     user4.add_teacher(user1)

    # with Session.begin() as session:
    #     print(list(session.query(Association)))

    # Association.get_all()
    
    # with Session.begin() as session:
    #     user1 = session.query(User).get(ids[3])

    #     print(user1)
    #     user1.update("lukashevda", "Дмитрий", "Лукашев")
    #     print(user1)
    pass

if __name__ == "__main__":
    create_db()