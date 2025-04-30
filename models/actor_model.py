from database.db_connection import mysql

class ActorModel:
    @staticmethod
    def get_all_actors(page=1, per_page=10):
        offset = (page - 1) * per_page
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM actors LIMIT %s OFFSET %s", (per_page, offset))
        actors = cursor.fetchall()
        cursor.close()
        return actors

    @staticmethod
    def get_actor_by_id(actor_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM actors WHERE actor_id = %s", (actor_id,))
        actor = cursor.fetchone()
        
        if actor:
            # Get movies the actor has appeared in
            cursor.execute("""
                SELECT m.movie_id, m.title, m.release_year, ma.role
                FROM movie_actors ma
                JOIN movies m ON ma.movie_id = m.movie_id
                WHERE ma.actor_id = %s
            """, (actor_id,))
            actor['movies'] = cursor.fetchall()
        
        cursor.close()
        return actor

    @staticmethod
    def add_actor(actor_data):
        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO actors (name, birth_date, bio)
            VALUES (%s, %s, %s)
        """, (actor_data['name'], actor_data['birth_date'], actor_data['bio']))
        actor_id = cursor.lastrowid
        mysql.connection.commit()
        cursor.close()
        return actor_id

    @staticmethod
    def update_actor(actor_id, actor_data):
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE actors 
            SET name = %s, birth_date = %s, bio = %s
            WHERE actor_id = %s
        """, (actor_data['name'], actor_data['birth_date'], 
              actor_data['bio'], actor_id))
        mysql.connection.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        return affected_rows > 0

    @staticmethod
    def delete_actor(actor_id):
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM actors WHERE actor_id = %s", (actor_id,))
        mysql.connection.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        return affected_rows > 0

    @staticmethod
    def search_actors(query, page=1, per_page=10):
        offset = (page - 1) * per_page
        cursor = mysql.connection.cursor()
        query = f"%{query}%"
        cursor.execute("""
            SELECT * FROM actors 
            WHERE name LIKE %s
            LIMIT %s OFFSET %s
        """, (query, per_page, offset))
        actors = cursor.fetchall()
        cursor.close()
        return actors