from mysql import connector
connection = connector.connect(
    user='flaskUser',
    password='MMv8nN9*gVZn.gn0Df5L',
    host='127.0.0.1',
    database='FineChain'
)

get_user_with_id = ("SELECT id, name, email, company_id, username, created_at, updated_at, deleted_at "
                    "FROM users "
                    "WHERE id=%(id)s")
insert_user =       ("INSERT INTO users "
                     "(name, email, username, password, salt) "
                     "VALUES (%(name)s, %(email)s, %(username)s, %(password)s, %(salt)s)")

# Adds a user to the users table
#   name*     - Users name
#   email     - Users email
#   username* - Users login identifier
#   password* - Hashed password
#   salt*     - The salt to imporve security
def postUser(name, email, username, password, salt):
    # Prepare for sql query
    cursor = connection.cursor()

    queryValues = {
        'name':name,
        'email':email,
        'username':username,
        'password':password,
        'salt':salt
    }

    # Execute the SQL command
    cursor.execute(insert_user, queryValues)
    id = cursor.lastrowid

    # Commit changes and close
    connection.commit()
    cursor.close()

    # Return the new users ID
    return id

def getUserWithId(id):
    cursor = connection.cursor()

    cursor.execute(get_user_with_id, {'id':id})
    value = cursor.fetchone()

    print(value)
    print(type(value))
