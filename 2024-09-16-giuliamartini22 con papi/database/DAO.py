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
                        order by s.shape desc
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
    def getAllEdges(lat, long):
        cnx = DBConnect.get_connection()

        result = []
        if cnx is None:
            print("Connessione fallita")
        else:

            cursor = cnx.cursor(dictionary=True)
            query =""" select n.state1 as stato1, n.state2 as stato2
                        from state st1, state st2, neighbor n 
                        where st1.id = n.state1 
                        and st1.id < st2.id 
                        and st2.id = n.state2
                        and st1.Lat > %s
                        and st1.Lng > %s
                        and st2.Lat > %s
                        and st2.Lng > %s"""

            cursor.execute(query, (lat, long,lat, long))

            for row in cursor:
                result.append((row["stato1"], row["stato2"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getPesi(lat, long, shape):
        cnx = DBConnect.get_connection()

        result = []
        if cnx is None:
            print("Connessione fallita")
        else:

            cursor = cnx.cursor(dictionary=True)
            query = """select st1.id as st1, sum(s.duration) as peso
                        from sighting s, state st1
                        where st1.Lat > %s
                        and st1.Lng > %s
                        and s.shape = %s
                        and s.state = st1.id
                        group by st1.id"""

            cursor.execute(query, (lat, long, shape,))

            for row in cursor:
                result.append((row["st1"], row["peso"]))

            cursor.close()
            cnx.close()
        return result


