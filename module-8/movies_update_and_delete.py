import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values

# Load secrets from .env file
secrets = dotenv_values(".env")

# Database configuration
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True
}

# Function to show film data
def show_films(cursor, title):
    query = """
        SELECT film_name AS Name, film_director AS Director, genre_name AS Genre, studio_name AS 'Studio Name'
        FROM film
        INNER JOIN genre ON film.genre_id = genre.genre_id
        INNER JOIN studio ON film.studio_id = studio.studio_id
    """
    cursor.execute(query)
    films = cursor.fetchall()
    
    print(f"\n-- {title} --")
    for film in films:
        print("Film Name: {}".format(film[0]))
        print("Director: {}".format(film[1]))
        print("Genre Name ID: {}".format(film[2]))
        print("Studio Name: {}\n".format(film[3]))

try:
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    print("\n  Database user {} connected to MySQL on host {} with database {}".format(
        config["user"], config["host"], config["database"]
    ))

    # Show initial film records
    show_films(cursor, "DISPLAYING FILMS")

    # Insert a new film (not Star Wars)
    insert_query = """
        INSERT INTO film (film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    # Example: "Inception", studio_id = 1, genre_id = 1 (adjust IDs as needed)
    cursor.execute(insert_query, ("Inception", "2010", 148, "Christopher Nolan", 1, 1))
    db.commit()

    show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

    # Update Alien to be a Horror film
    update_query = """
        UPDATE film
        SET genre_id = (SELECT genre_id FROM genre WHERE genre_name = 'Horror')
        WHERE film_name = 'Alien'
    """
    cursor.execute(update_query)
    db.commit()

    show_films(cursor, "DISPLAYING FILMS AFTER UPDATE - Changed Alien to Horror")

    # Delete the film Gladiator
    delete_query = "DELETE FROM film WHERE film_name = 'Gladiator'"
    cursor.execute(delete_query)
    db.commit()

    show_films(cursor, "DISPLAYING FILMS AFTER DELETE")

    input("\n\n  Press any key to continue...")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")
    else:
        print(err)

finally:
    if 'db' in locals() and db.is_connected():
        db.close()
