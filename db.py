import sqlite3
import base64
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
    return sqlite_query("SELECT id, username FROM user WHERE username LIKE ?", ("%"+username+"%",), USER_DB)


def create_user(username, password):
    #  Check if user already exists
    if(len(find_user(username)) != 0):
        return False

    hashpass = hashlib.sha512(password.encode()).hexdigest()
    sqlite_query("INSERT INTO user (username, password) VALUES(?, ?)", (username, hashpass), USER_DB)
    return True


def check_user_creds(username, password):
    hashpass = hashlib.sha512(password.encode()).hexdigest()
    return sqlite_query("SELECT id FROM user WHERE username=? AND password=?", (username, hashpass), USER_DB)


def follow_user(user_id, target_id):
    already_follows = sqlite_query("SELECT * FROM follows WHERE follower=? AND followed=?", (user_id, target_id), USER_DB)
    if(len(already_follows) == 0):
        sqlite_query("INSERT INTO follows VALUES (?, ?)", (user_id, target_id), USER_DB)
        return True
    return False  #  User already followed


def create_post(userid, text, image):
    if(image != None):
        sqlite_query("INSERT INTO post (userid, content, image, like_count) VALUES (?, ?, ?, ?)", (userid, text, image, 0), POST_DB)
    else:
        sqlite_query("INSERT INTO post (userid, content, like_count) VALUES (?, ?, ?)", (userid, text, 0), POST_DB)
    return True


def find_user_posts(username):
    #  Find user id
    user = find_user(username)
    if(len(user) == 0):
        return False

    userid = user[0][0]
    posts = sqlite_query("SELECT id, content FROM post WHERE userid=?", (userid,), POST_DB)
    
    return posts


def get_post_content(post_id):
    post = sqlite_query("SELECT content, image, like_count FROM post WHERE id=?", (post_id,), POST_DB)
    if(len(post) == 0):
        return False
    post = list(post[0])
    #  Coonvert immage to b64 if not null
    if(post[1] != None):
        post[1] = base64.b64encode(post[1]).decode()
    return post


def like_post(user_id, post_id):
    if(len(sqlite_query("SELECT * FROM post WHERE id=?", (post_id,), POST_DB)) == 0):
        return False

    if(is_post_liked(user_id, post_id)):
        return True
    sqlite_query("INSERT INTO likes VALUES (?, ?)", (post_id, user_id), POST_DB)
    post_likes = sqlite_query("SELECT like_count FROM post WHERE id=?", (post_id,), POST_DB)[0][0]
    post_likes += 1
    sqlite_query("UPDATE post SET like_count=? WHERE id=?", (post_likes, post_id), POST_DB)
    return True


def is_post_liked(user_id, post_id):
    post_status = sqlite_query("SELECT * FROM likes WHERE userid=? AND postid=?", (user_id, post_id), POST_DB)
    if(len(post_status) == 1):
        return True
    return False


def post_feed(userid):
    pass


if __name__ == "__main__":
    print(create_user("test", "pass1234"))
    print(create_user("user2", "pass123"))
    print(find_user("test"))
    print(check_user_creds("test", "pass1234"))
    print(check_user_creds("test", "wrongpass123"))
    #print(create_post(1, "First test post!", None))
    print(find_user_post("test"))
    follow_user(1, 2)

