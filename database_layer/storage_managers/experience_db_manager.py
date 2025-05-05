from application_layer.classes.experience import Experience
from database_layer.db_setup import DatabaseManager
class ExperienceDBManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def add_experience(self, experience: Experience):
        db_connection = self.db_manager.get_db_connection()
        cursor = db_connection.cursor()

        query = (
            "INSERT INTO experiences "
            "(employee_id, company_name, position, joining_date, ending_date, location) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )

        experience_data = self.experience_object_to_tuple(experience, "add")

        try:
            cursor.execute(query, experience_data)
            degree_id = cursor.lastrowid
            db_connection.commit()
            cursor.close()
            db_connection.close()
            return degree_id
        
        except db_connection.Error as err:
            print(err.msg)
            cursor.close()
            db_connection.close()
            return None

    def search_experiences_of_an_employee(self, employee_id):
        db_connection = self.db_manager.get_db_connection()
        cursor = db_connection.cursor(dictionary=True)
        
        query = (
            "SELECT * FROM experiences "
            "WHERE employee_id = %s"
        )

        try:
            cursor.execute(query, (employee_id,))
            result = cursor.fetchall()   
            experiences = self.db_data_to_experience_list(result)

            cursor.close()
            db_connection.close()
            return experiences
        
        except db_connection.Error as err:
            print(err.msg)
            cursor.close()
            db_connection.close()
            return None

    def delete_an_experience_of_an_employee(self, experience_id):
        db_connection = self.db_manager.get_db_connection()
        cursor = db_connection.cursor()

        query = (
            "DELETE FROM experiences "
            "WHERE experience_id=%s"
        )

        try:
            cursor.execute(query, (experience_id,))
            db_connection.commit()
            result = cursor.rowcount
            cursor.close()
            db_connection.close()
            return result
        
        except db_connection.Error as err:
            print(err.msg)
            cursor.close()
            db_connection.close()
            return None

    def update_an_experience_of_an_employee(self, experience: Experience):
        db_connection = self.db_manager.get_db_connection()
        cursor = db_connection.cursor()

        query = (
            "UPDATE experiences SET " 
            "employee_id=%s, " 
            "company_name=%s, " 
            "position=%s, " 
            "joining_date=%s, " 
            "ending_date=%s, " 
            "location=%s " 
            "WHERE experience_id=%s"
        )

        updated_experience_data = self.experience_object_to_tuple(experience, "update")

        try:
            cursor.execute(query, updated_experience_data)
            db_connection.commit()
            result = cursor.rowcount
            
            cursor.close()
            db_connection.close()
            return result
        
        except db_connection.Error as err:
            print(err.msg)
            cursor.close()
            db_connection.close()
            return None
        
    # Some helper methods
    def experience_object_to_tuple(self, experience: Experience, flag):
        return (
            experience._employee_id,
            experience._company_name,
            experience._position,
            experience._joining_date,
            experience._ending_date,
            experience._location
        ) if flag == "add" else (
            experience._employee_id,
            experience._company_name,
            experience._position,
            experience._joining_date,
            experience._ending_date,
            experience._location,
            experience._experience_id,
        )
    
    def db_data_to_experience_list(self, data) -> list[Experience]:
        experiences: list[Experience] = []
        for row in data:
            experience = Experience(
                row['experience_id'],
                row['employee_id'],
                row['company_name'],
                row['position'],
                row['joining_date'],
                row['ending_date'],
                row['location']
            )
            experiences.append(experience)
        return experiences