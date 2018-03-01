from mysql import connector
connection = connector.connect(
    user='flaskUser',
    password='MMv8nN9*gVZn.gn0Df5L',
    host='127.0.0.1',
    database='FineChain'
)

get_company_users = ("SELECT id "
                     "FROM users "
                     "WHERE company_id=%(id)s")

get_company_with_id = ("SELECT * "
                       "FROM companys"
                       "WHERE id=%(id)s")

get_user_with_id = ("SELECT id, name, email, company_id, username, created_at, updated_at, deleted_at "
                    "FROM users "
                    "WHERE id=%(id)s")
insert_user =       ("INSERT INTO users "
                     "(name, email, username, password, salt) "
                     "VALUES (%(name)s, %(email)s, %(username)s, %(password)s, %(salt)s)")

def getCompany(company_id):
    cursor = connection.cursor()

    cursor.execute(get_company_with_id, {'id':company_id})
    company = cursor.fetchone()

    admin = getUserWithId(company[2])
    admin.pop('company_id', None)
    admin.pop('updated_at', None)
    admin.pop('deleted_at', None)

    cursor.execute(get_company_users, {'id':company_id})
    user_ids = []
    for (id,) in cursor:
        user_ids.append(id)

    returnVal = {
        'id':company[0],
        'name'company[1],
        'admin':admin,
        'user_ids':[],
        'created_at':company[4],
        'updated_at':company[5],
        'deleted_at':company[6]
    }

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

# Gets a user with a id
#   id*     - Id of user to retrieve
def getUserWithId(user_id):
    cursor = connection.cursor()

    cursor.execute(get_user_with_id, {'id':user_id})
    value = cursor.fetchone()

    returnVal = {
        'id':value[0],
        'name':value[1],
        'email':value[2],
        'company_id':value[3],
        'username':value[4],
        'created_at':value[5],
        'updated_at':value[6],
        'deleted_at':value[7],
    }

    return returnVal
