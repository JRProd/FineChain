from mysql import connector
connection = connector.connect(
    user='flaskUser',
    password='MMv8nN9*gVZn.gn0Df5L',
    host='127.0.0.1',
    database='FineChain'
)

get_company_with_id =       ("SELECT * "
                             "FROM companys "
                             "WHERE id=%(id)s")

get_company_users =         ("SELECT id "
                             "FROM users "
                             "WHERE company_id=%(id)s")

insert_company =            ("INSERT INTO companys "
                            "(name, admin_id) "
                            "VALUES (%(name)s, %(admin_id)s)")

update_company_info =       ("UPDATE companys "
                             "SET name=%(name)s "
                             "WHERE id=%(id)s")

update_company_admin =      ("UPDATE companys "
                             "SET admin_id=%(admin)s "
                             "WHERE id=%(id)s")

get_user_with_id =          ("SELECT id, name, email, company_id, username, created_at, updated_at, deleted_at "
                             "FROM users "
                             "WHERE id=%(id)s")

get_user_with_username =    ("SELECT * "
                             "FROM users "
                             "WHERE username=%(username)s")

insert_user =               ("INSERT INTO users "
                             "(name, email, username, password) "
                             "VALUES (%(name)s, %(email)s, %(username)s, %(password)s)")

update_user_info =          ("UPDATE users "
                             "SET name=%(name)s, email=%(email)s, company_id=%(company_id)s "
                             "WHERE id=%(id)s")

update_user_password =      ("UPDATE users "
                             "SET password=%(password)s "
                             "WHERE id=%(id)s")

def getCompanyWithId(company_id):
    cursor = connection.cursor()

    cursor.execute(get_company_with_id, {'id':company_id})
    company = cursor.fetchone()

    if company is None:
        raise ValueError("No company found with id: %s" % company_id)

    admin = getUserWithId(company[2])
    # Remove unimportant values from the admin
    admin.pop('company_id', None)
    admin.pop('updated_at', None)
    admin.pop('deleted_at', None)

    cursor.execute(get_company_users, {'id':company_id})
    user_ids = [None]
    for (id,) in cursor:
        user_ids.append(id)

    returnVal = {
        'id':company[0],
        'name':company[1],
        'admin':admin,
        'user_ids':user_ids,
        'created_at':company[3],
        'updated_at':company[4],
        'deleted_at':company[5]
    }

    return returnVal

def postCompany(name, admin_id):
    cursor = connection.cursor()

    cursor.execute(insert_company, {'name':name, 'admin_id':admin_id})
    id = cursor.lastrowid

    #TODO: Add the company_id to the admin

    admin = getUserWithId(admin_id)
    # Remove unimportant values from the admin
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

def updateCompanyInfo(company_id, data):
    cursor= connection.cursor()
    updatedCompany = getCompanyWithId(company_id)
    updatedCompany.pop('admin', None)
    updatedCompany.pop('user_ids', None)

    for key, value in data.items():
#        if key in updatedCompany:
         updatedCompany[key] = value

    cursor.execute(update_company_info, updatedCompany)

    connection.commit()
    cursor.close()

    return updatedCompany

def updateComapnyAdmin(company_id, user_id, username):
    cursor = connection.cursor()

    admin = getUserWithId(user_id);
    if admin['username'] != username:
        #TODO: Define errors for not matching username
        pass
    if admin['compnay_id'] != company_id:
        #TODO: User must be part of company to become admin
        pass

    cursor.execute(update_user_password, {'admin_id':admin['id']})

    connection.commit()
    cursor.close()

    return admin;

# Updates a user to reflect which company they are
def addUserToCompany(company_id, user_id, username):
    user = getUserWithId(user_id)
    if user['username'] != username:
        # TODO Usernames must match
        pass
    if user['company_id'] is not None:
        # TODO User must not be part of any other company
        pass

    updateUserInfo(user_id, {'company_id':company_id})
    returnVal = {
        'user_id':user_id,
        'user_ids':username,
        'company_id':company_id,
        'success':True,
        'message':'User added.'
    }

    return returnVal

def removeUserFromCompany(company_id, user_id, username):
    user = getUserWithId(user_id)
    if user['username'] != username:
        # TODO Usernames must match
        pass
    if user['company_id'] != company_id:
        # TODO User must be part of any other company
        pass

    updateUserInfo(user_id, {'company_id':None})
    returnVal = {
        'user_id':user_id,
        'username':username,
        'company_id':None,
        'success':True,
        'message':'User removed.'
    }

    return returnVal

# Gets a user with a id
#   id*     - Id of user to retrieve
def getUserWithId(user_id):
    cursor = connection.cursor()

    cursor.execute(get_user_with_id, {'id':user_id})
    user = cursor.fetchone()

    if user is None:
        raise ValueError("No user found with id: %s" % user_id)

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

    if user is None:
        raise ValueError("No user found with username: %s" % username)

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

def updateUserInfo(user_id, data):
    cursor= connection.cursor()
    updatedUser = getUserWithId(user_id)

    for key, value in data.items():
        updatedUser[key] = value

    cursor.execute(update_user_info, updatedUser)

    connection.commit()
    cursor.close()

    return updatedUser

def updateUserPassword(user_id, password):
    cursor= connection.cursor()

    cursor.execute(update_user_password, {'id':user_id, 'password':password})

    connection.commit()
    cursor.close()
