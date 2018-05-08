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
                             "SET admin_id=%(admin_id)s "
                             "WHERE id=%(id)s")

get_current_hash =          ("SELECT current_hash"
                             "FROM blockchains "
                             "WHERE company_id=%(company_id)s")

insert_blockchain =         ("INSERT INTO blockchains "
                             "(company_id) "
                             "VALUES (%(company_id)s)")

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

# Gets a company from an ID
#   company_id* - Company to get
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

# Creates a new company
#   name*       - The name of the company
#   admin_id*   - The new admin of the company
def postCompany(name, admin_id):
    cursor = connection.cursor()

    # Post a company to the server
    cursor.execute(insert_company, {'name':name, 'admin_id':admin_id})
    id = cursor.lastrowid

    returnVal = {
        'id':id,
        'name':name,
        'user_ids':[admin_id],
    }

    connection.commit()
    cursor.close()

    return returnVal

# Update company information
#   company_id*    - ID to update
#   data*       - Any updatable data on the server
def updateCompanyInfo(company_id, data):
    cursor= connection.cursor()
    updatedCompany = getCompanyWithId(company_id)
    updatedCompany.pop('admin', None)
    updatedCompany.pop('user_ids', None)

    # Get all of the updated values
    for key, value in data.items():
         updatedCompany[key] = value

    cursor.execute(update_company_info, updatedCompany)

    connection.commit()
    cursor.close()

    return updatedCompany

# Updates who is in control of the company
#   company_id*     - Company to update
#   user_id*        - The User to be the new admin
#   username*       - Username for verification
def updateCompanyAdmin(company_id, user_id, username):

    cursor = connection.cursor()

    # Check if values are correct
    admin = getUserWithId(user_id);
    if admin['username'] != username:
        raise KeyError('Username given did not match ID given')
    if admin['company_id'] != company_id:
        raise ValueError('User must be part of the company to be promoted')

    queryValues = {
        'admin_id':admin['id'],
        'id':company_id,
    }

    cursor.execute(update_company_admin, queryValues)

    connection.commit()
    cursor.close()

    return admin;

# Adds an authorized users from the company
#   company_id*     - Company to modify
#   user_id*        - Ids to be added
#   username*       - usernames for verification
def addUserToCompany(company_id, user_id, username):
    user = None
    try:
        user = getUserWithId(user_id)
    except ValueError as e:
        return False, str(e)

    # Check if values are correct
    if user['username'] != username:
        return False, 'ID and username must match'
    if user['company_id'] is not None:
        return False, 'Part of another Company'

    updateUserInfo(user_id, {'company_id':company_id})
    returnVal = {
        'user_id':user_id,
        'user_ids':username,
        'company_id':company_id,
        'success':True,
        'message':'User added.'
    }

    return True, returnVal

# Removes an authorized users from the company
#   company_id*     - Company to modify
#   user_id*        - Ids to be added
#   username*       - usernames for verification
def removeUserFromCompany(company_id, user_id, username):
    user = None
    try:
        user = getUserWithId(user_id)
    except ValueError as e:
        return False, str(e)

    # Check if values are correct
    if user['username'] != username:
        return False, 'ID and username must match'
    if user['company_id'] != company_id:
        return False, 'User must be part of this Company'

    updateUserInfo(user_id, {'company_id':None})
    returnVal = {
        'user_id':user_id,
        'username':username,
        'company_id':None,
        'success':True,
        'message':'User removed.'
    }

    return True, returnVal

# Gets the blockchain from the MySQL server
#   company_id*     - Company to get blockchain from
def getBlockchainHash(company_id):
    cursor = connection.cursor()

    currentHash = cursor.execute(get_current_hash, {'compnay_id':company_id})

    return currentHash[0]

# Creates blockchain in the MySQL server
#   company_id*     - Company who created the blockchain
def postBlockchain(company_id):
    cursor = connection.cursor()

    cursor.execute(insert_blockchain, {'company_id':company_id})
    id = cursor.lastrowid

    returnVal = {
        'id':id,
        'compnay_id':company_id,
        'current_hash':None,
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

# Gets the user profile from a Username
#   username*    - username used in search
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

# Update users information
#   user_id*    - ID to update
#   data*       - Any updatable data on the server
def updateUserInfo(user_id, data):
    cursor= connection.cursor()
    updatedUser = getUserWithId(user_id)

    for key, value in data.items():
        updatedUser[key] = value

    cursor.execute(update_user_info, updatedUser)

    connection.commit()
    cursor.close()

    return updatedUser

# Updates a users password
#   user_id*     - User's ID
#   password*    - New Password
def updateUserPassword(user_id, password):
    cursor= connection.cursor()

    cursor.execute(update_user_password, {'id':user_id, 'password':password})

    connection.commit()
    cursor.close()
