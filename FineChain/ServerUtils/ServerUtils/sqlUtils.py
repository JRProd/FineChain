from mysql import connector
connection = connector.connect(
    user='flaskUser',
    password='MMv8nN9*gVZn.gn0Df5L',
    host='127.0.0.1',
    database='FineChain'
)

get_session =         ("SELECT * "
                       "FROM sessions "
                       "WHERE session=%(session)s")

open_session =        ("INSERT INTO sessions "
                       "(user_id, session, resession, deleted_at) "
                       "VALUES (%(user_id)s, %(session)s, %(resession)s, %(deleted_at)s)")

close_session =             ("DELETE FROM sessions "
                             "WHERE session=%(session)s")

get_company_with_id =       ("SELECT * "
                             "FROM companys"
                             "WHERE id=%(id)s")

get_company_users =         ("SELECT id "
                             "FROM users "
                             "WHERE company_id=%(id)s")

insert_company =            ("INSERT INTO companys "
                            "(name, admin_id) "
                            "VALUES (%(name)s, %(admin_id)s)")

get_user_with_id =          ("SELECT id, name, email, company_id, username, created_at, updated_at, deleted_at "
                             "FROM users "
                             "WHERE id=%(id)s")

get_user_with_username =    ("SELECT * "
                             "FROM users "
                             "WHERE username=%(username)s")

insert_user =               ("INSERT INTO users "
                             "(name, email, username, password) "
                             "VALUES (%(name)s, %(email)s, %(username)s, %(password)s)")

update_user =               ("UPDATE users "
                             "SET name=%(name)s, email=%(email)s, passowrd=%(pass)s "
                             "WHERE id=%(id)s")

def getSession(session):
    cursor - connection.cursor()

    session = cursor.execute(get_session, {'session':session})

    returnVal = {
        'id':session[0],
        'user_id':session[1],
        'session':session[2],
        'resession':session[3],
        'created_at':session[4],
        'deleted_at':session[5],
    }

    return returnVal

def openSession(user_id, session, resession, deleted_at):
    cursor = connection.cursor()

    queryValues = {
        'user_id':user_id,
        'session':session,
        'resession':resession,
        'deleted_at':deleted_at
    }

    cursor.execute(open_session, queryValues)
    id = cursor.lastrowid

    returnVal = {
        'id':id,
        'user_id':user_id,
        'session':session,
        'resession':resession,
        'deleted_at':deleted_at
    }

    connection.commit()
    cursor.close()

    return returnVal

def postCompany(name, admin_id):
    cursor = connection.cursor()

    cursor.execute(insert_company, {'name':name, 'admin_id':admin_id})
    id = cursor.lastrowid

    #TODO: Add the company_id to the admin

    admin = getUserWithId(admin_id)
    # Remove unimportant values from the admin
    admin.pop('company_id', None)
    admin.pop('updated_at', None)
    admin.pop('deleted_at', None)

    returnVal = {
        'id':id,
        'name':name,
        'admin':admin,
        'user_ids':[],
        'blockchain':{},
    }

    connection.commit()
    cursor.close()

    return returnVal

def getCompany(company_id):
    cursor = connection.cursor()

    cursor.execute(get_company_with_id, {'id':company_id})
    company = cursor.fetchone()

    admin = getUserWithId(company[2])
    # Remove unimportant values from the admin
    admin.pop('company_id', None)
    admin.pop('updated_at', None)
    admin.pop('deleted_at', None)

    cursor.execute(get_company_users, {'id':company_id})
    user_ids = []
    for (id,) in cursor:
        user_ids.append(id)

    returnVal = {
        'id':company[0],
        'name':company[1],
        'admin':admin,
        'user_ids':user_ids,
        'created_at':company[4],
        'updated_at':company[5],
        'deleted_at':company[6]
    }

    return returnVal

# Gets a user with a id
#   id*     - Id of user to retrieve
def getUserWithId(user_id):
    cursor = connection.cursor()

    cursor.execute(get_user_with_id, {'id':user_id})
    user = cursor.fetchone()

    returnVal = {
        'id':user[0],
        'name':user[1],
        'email':user[2],
        'company_id':user[3],
        'username':user[4],
        'created_at':user[5],
        'updated_at':user[6],
        'deleted_at':user[7],
    }

    cursor.close()
    return returnVal

def getUserWithUsername(username):
    cursor = connection.cursor()

    cursor.execute(get_user_with_username, {'username':username})
    user = cursor.fetchone()

    returnVal = {
        'id':user[0],
        'username':user[4],
        'password':user[5],
        'created_at':user[6],
        'updated_at':user[7],
        'deleted_at':user[8],
    }

    cursor.close()
    return returnVal

# Adds a user to the users table
#   name*     - Users name
#   email     - Users email
#   username* - Users login identifier
#   password* - Hashed password
def postUser(name, email, username, password):
    # Prepare for sql query
    cursor = connection.cursor()

    queryValues = {
        'name':name,
        'email':email,
        'username':username,
        'password':password
    }

    # Execute the SQL command
    cursor.execute(insert_user, queryValues)
    id = cursor.lastrowid

    # Define value to return
    returnVal = {
        'id':id,
        'name':name,
        'email':email,
        'company_id':None,
        'username':username
    }

    # Commit changes and close
    connection.commit()
    cursor.close()
    # Return the new users ID
    return returnVal

def updateUser(user_id, data):
    cursor= connection.cursor()
    user = getUserWithId(user_id)

    queryValues = {
        'name':user['name'],
        'email':user['email'],
        'password':user['password']
    }
    for key, value in data.items():
        queryValues[key] = value

    cursor.execute(update_user, queryValues)

    # connection.commit()
    cursor.close()

    return data
