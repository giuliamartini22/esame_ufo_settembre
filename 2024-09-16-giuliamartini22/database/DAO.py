from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass


    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_valori_limite():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select MAX(Lat) as maxLat, min(Lat) as minLat, max(Lng) as maxLon, min(Lng) as minLon  
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append((row["maxLat"], row["minLat"], row["maxLon"], row["minLon"]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getLimiti() -> list[[int]]:
        cnx = DBConnect.get_connection()
        if cnx is not None:
            cursor = cnx.cursor()
            query = """select MAX(Lat) as maxLat, min(Lat) as minLat, max(Lng) as maxLon, min(Lng) as minLon  
                    from state s"""
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            cnx.close()
            return rows
        else:
            print("Errore di connessione")
            return None

    @staticmethod
    def getMaxLat() -> int:
        cnx = DBConnect.get_connection()
        if cnx is not None:
            cursor = cnx.cursor()
            query = """select MAX(Lat) as maxLat 
                        from state s"""
            cursor.execute(query)
            rows = cursor.fetchone()
            cursor.close()
            cnx.close()
            return rows
        else:
            print("Errore di connessione")
            return None

    @staticmethod
    def getAllShapes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct s.shape
                        from sighting s
                        where s.shape <> ""
                        order by s.shape asc
                    """
            cursor.execute(query)

            for row in cursor:
                result.append(row["shape"])
            cursor.close()
            cnx.close()
            return result

    @staticmethod
    def get_all_states(lat, long, shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct st.*
                        from sighting s, state st
                        where st.Lat > %s
                        and st.Lng > %s
                        and s.state = st.id 
                        and s.shape = %s"""
            cursor.execute(query, (lat, long, shape))

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result


    @staticmethod
    def getAllEdges(lat, long, shape):
        cnx = DBConnect.get_connection()

        result = []
        if cnx is None:
            print("Connessione fallita")
        else:

            cursor = cnx.cursor(dictionary=True)
            query = """select st1.id as st1, st2.id as st2, sum(s.duration) as peso
                        from sighting s, state st1, state st2, neighbor n 
                        where st1.Lat > %s
                        and st1.Lng > %s
                        and (s.state = st1.id or s.state = st2.id )
                        and st2.Lat > %s
                        and st2.Lng > %s
                        and s.state = st2.id 
                        and s.shape = %s
                        and n.state1 = st1.id
                        and n.state2 = st2.id 
                        group by st1.id, st2.id"""

            cursor.execute(query, (lat, long,lat, long, shape))

            for row in cursor:
                result.append((row["st1"], row["st2"], row["peso"]))

            cursor.close()
            cnx.close()
        return result


