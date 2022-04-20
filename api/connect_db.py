import psycopg2

def connect():
    try:
        conn = psycopg2.connect(
            host="db",
            port="5432",
            database="geoApp",
            user="postgres",
            password="smeMioUI4m12q"
        )
        return conn
    except:
        return False


def elem1(conn, point, date):   
    pointSplit = point.split()
    cur = conn.cursor()
    # cur.execute(
    #     """
    #     select amount, p_month,  p_age, p_gender, postal_code_id 
    #         from paystats 
    #         where postal_code_id=(
    #             select id 
    #                 from postal_codes where st_Contains(
    #                     st_geomfromtext(st_astext(the_geom)), st_point({long}, {lat})
    #                 )
    #         )
    #     """.format(long=pointSplit[0], lat=pointSplit[1])
    # )
    cur.execute(
        """
        select p_age as age, p_gender as gender, SUM (amount) as amount 
        from paystats 
            where postal_code_id=(
                select id from postal_codes 
                    where st_Contains(st_geomfromtext(st_astext(the_geom)), st_point({long}, {lat}))
            ) 
            and p_month='{d}' 
            group by amount, p_month, p_age, p_gender, postal_code_id 
            order by p_age 
        """.format(long=pointSplit[0], lat=pointSplit[1], d=date)
    )
    result = cur.fetchall()
    cur.close()
    return result
