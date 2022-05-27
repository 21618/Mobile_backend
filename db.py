import sqlite3
import hashlib

USER_DB = "user.db"
POST_DB = "post.db"

#  A tuple is expected for params
def sqlite_query(query, params, db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    if(params == None):
        cursor.execute(query)
    else:
        cursor.execute(query, params)

    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result

#  Init database
sqlite_query("CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, username TEXT, password TEXT)", None, USER_DB)
sqlite_query("CREATE TABLE IF NOT EXISTS follows (follower INTEGER NOT NULL, followed INTEGER NOT NULL)", None, USER_DB)

sqlite_query("CREATE TABLE IF NOT EXISTS post (id INTEGER NOT NULL PRIMARY KEY, userid INTEGER NOT NULL,content TEXT, image BLOB, like_count INTEGER)", None, POST_DB)
sqlite_query("CREATE TABLE IF NOT EXISTS likes (postid INTEGER NOT NULL, userid INTEGER NOT NULL)", None, POST_DB)


#  User relations (follow/ likes)

#  User database interactions functions:
def find_user(username):
    return sqlite_query("SELECT id, username FROM user WHERE username=?", (username,), USER_DB)


def create_user(username, password):
    #  Check if user already exists
    if(len(find_user(username)) != 0):
        return False

    hashpass = hashlib.sha512(password.encode()).hexdigest()
    sqlite_query("INSERT INTO user (username, password) VALUES(?, ?)", (username, hashpass), USER_DB)
    return True


def check_user_creds(username, password):
    hashpass = hashlib.sha512(password.encode()).hexdigest()
    user = sqlite_query("SELECT * FROM user WHERE username=? AND password=?", (username, hashpass), USER_DB)
    if(len(user) != 0):
        return True
    return False


def follow_user(userid, target_id):
    sqlite_query("INSERT INTO follows (?, ?)", (user_id, target_id), USER_DB)



#  Binary data is expected for image
def create_post(userid, text, image):
    if(image == None):
        sqlite_query("INSERT INTO post (userid, content, image, like_count) VALUES (?, ?, ?, ?)", (userid, text, image, 0), POST_DB)
    else:
        sqlite_query("INSERT INTO post (userid, content, like_count) VALUES (?, ?, ?)", (userid, text, 0), POST_DB)
    return True


def find_user_post(username):
    #  Find user id
    user = find_user(username)
    if(len(user) == 0):
        return False

    userid = user[0][0]
    posts = sqlite_query("SELECT * FROM post WHERE userid=?", (userid,), POST_DB)

    return posts


def get_post_content(post_id):
    pass

def like_post(userid, postid):
    pass   

def post_feed(userid):
    pass

if __name__ == "__main__":
    print(create_user("test", "pass1234"))
    print(find_user("test"))
    print(check_user_creds("test", "pass1234"))
    print(check_user_creds("test", "wrongpass123"))
    print(create_post(1, "First test post!", None))
    print(find_user_post("test"))
