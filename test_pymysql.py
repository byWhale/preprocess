import pymysql

connection = pymysql.connect(host='10.1.0.177',
                                 user='root',
                                 password='root',
                                 database='patent',
                                 cursorclass=pymysql.cursors.DictCursor)

with connection:
    for i in range(10):
        with connection.cursor() as cursor:
             # Create a new record
            sql = "INSERT INTO `signory` (`signory_item`, `patent_id`) VALUES (%s, %s)"
            try:
                cursor.execute(sql, ('webmaster@python.org', 1))
                connection.commit()
            except:
                connection.rollback()
