from py2neo import Graph, Node, Relationship
import mysql.connector
import logging
import decimal

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MySQL connection details
mysql_config = {
    'user': 'root',
    'password': 'bq625902',
    'host': 'localhost',
    'database': 'University'
}

# Neo4j connection details
neo4j_url = "bolt://localhost:7687"
neo4j_user = "neo4j"
neo4j_password = "bakha2002"

# Connect to MySQL
try:
    mysql_conn = mysql.connector.connect(**mysql_config)
    mysql_cursor = mysql_conn.cursor(dictionary=True)
    logger.info("Connected to MySQL")
except mysql.connector.Error as err:
    logger.error(f"Error connecting to MySQL: {err}")
    exit(1)

# Connect to Neo4j
try:
    graph = Graph(neo4j_url, auth=(neo4j_user, neo4j_password))
    logger.info("Connected to Neo4j")
except Exception as e:
    logger.error(f"Error connecting to Neo4j: {e}")
    exit(1)

# Function to handle Neo4j errors and drop all data
def handle_neo4j_error():
    logger.error("Error during migration. Dropping all data from Neo4j.")
    try:
        graph.run("MATCH (n) DETACH DELETE n")
        logger.info("All data dropped from Neo4j database")
    except Exception as drop_err:
        logger.error(f"Error dropping data from Neo4j: {drop_err}")
    finally:
        mysql_cursor.close()
        mysql_conn.close()
        exit(1)

# Migration functions with error handling
def migrate_faculty():
    try:
        mysql_cursor.execute("SELECT * FROM Faculty")
        for row in mysql_cursor:
            node = Node("Faculty", FacultyID=row["FacultyID"], FacultyName=row["FacultyName"])
            graph.create(node)
    except Exception as e:
        handle_neo4j_error()

def migrate_degree():
    try:
        mysql_cursor.execute("SELECT * FROM Degree")
        for row in mysql_cursor:
            node = Node("Degree", DegreeID=row["DegreeID"], DegreeName=row["DegreeName"])
            graph.create(node)
            relationship = Relationship(graph.nodes.match("Faculty", FacultyID=row["FacultyID"]).first(), "HAS_DEGREE", node)
            graph.create(relationship)
    except Exception as e:
        handle_neo4j_error()

def migrate_student():
    try:
        mysql_cursor.execute("SELECT * FROM Student")
        for row in mysql_cursor:
            node = Node("Student", StudentID=row["StudentID"], FirstName=row["FirstName"], LastName=row["LastName"],
                        DateOfBirth=row["DateOfBirth"], Gender=row["Gender"], Email=row["Email"])
            graph.create(node)
    except Exception as e:
        handle_neo4j_error()

def migrate_professor():
    try:
        mysql_cursor.execute("SELECT * FROM Professor")
        for row in mysql_cursor:
            node = Node("Professor", ProfessorID=row["ProfessorID"], FirstName=row["FirstName"], LastName=row["LastName"],
                        DateOfBirth=row["DateOfBirth"], Gender=row["Gender"], Email=row["Email"])
            graph.create(node)
            relationship = Relationship(node, "BELONGS_TO", graph.nodes.match("Faculty", FacultyID=row["FacultyID"]).first())
            graph.create(relationship)
    except Exception as e:
        handle_neo4j_error()

def migrate_course():
    try:
        mysql_cursor.execute("SELECT * FROM Course")
        for row in mysql_cursor:
            node = Node("Course", CourseID=row["CourseID"], CourseName=row["CourseName"], Credits=row["Credits"])
            graph.create(node)
    except Exception as e:
        handle_neo4j_error()

def migrate_degree_student():
    try:
        mysql_cursor.execute("SELECT * FROM Degree_Student")
        for row in mysql_cursor:
            student = graph.nodes.match("Student", StudentID=row["StudentID"]).first()
            degree = graph.nodes.match("Degree", DegreeID=row["DegreeID"]).first()
            if student and degree:
                # Convert GPA to float if it's a decimal.Decimal
                gpa = float(row["GPA"]) if isinstance(row["GPA"], decimal.Decimal) else row["GPA"]
                relationship = Relationship(student, "ENROLLED_IN", degree, GPA=gpa)
                graph.create(relationship)
    except Exception as e:
        handle_neo4j_error()

def migrate_degree_course():
    try:
        mysql_cursor.execute("SELECT * FROM Degree_Course")
        for row in mysql_cursor:
            degree = graph.nodes.match("Degree", DegreeID=row["DegreeID"]).first()
            course = graph.nodes.match("Course", CourseID=row["CourseID"]).first()
            if degree and course:
                relationship = Relationship(degree, "INCLUDES_COURSE", course)
                graph.create(relationship)
    except Exception as e:
        handle_neo4j_error()

def migrate_course_student():
    try:
        mysql_cursor.execute("SELECT * FROM Course_Student")
        for row in mysql_cursor:
            student = graph.nodes.match("Student", StudentID=row["StudentID"]).first()
            course = graph.nodes.match("Course", CourseID=row["CourseID"]).first()
            if student and course:
                # Convert Grade to float if it's a decimal.Decimal
                grade = float(row["Grade"]) if isinstance(row["Grade"], decimal.Decimal) else row["Grade"]
                relationship = Relationship(student, "TAKES", course, Grade=grade)
                graph.create(relationship)
    except Exception as e:
        handle_neo4j_error()

def migrate_course_professor():
    try:
        mysql_cursor.execute("SELECT * FROM Course_Professor")
        for row in mysql_cursor:
            professor = graph.nodes.match("Professor", ProfessorID=row["ProfessorID"]).first()
            course = graph.nodes.match("Course", CourseID=row["CourseID"]).first()
            if professor and course:
                relationship = Relationship(professor, "TEACHES", course)
                graph.create(relationship)
    except Exception as e:
        handle_neo4j_error()

# Migrate data
try:
    migrate_faculty()
    migrate_degree()
    migrate_student()
    migrate_professor()
    migrate_course()
    migrate_degree_student()
    migrate_degree_course()
    migrate_course_student()
    migrate_course_professor()
    logger.info("Data migration completed successfully")
except Exception as e:
    logger.error(f"Error during migration: {e}")
    handle_neo4j_error()
finally:
    mysql_cursor.close()
    mysql_conn.close()
