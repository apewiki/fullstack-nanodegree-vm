#
# Database access functions for the web forum.
#
import psycopg2
import time
import bleach

## Database connection
#db = sqlite3.connect("forum")
DB=[]

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    db = psycopg2.connect("dbname=forum")
    if db:
      c = db.cursor()
      query = "select content, time from posts;"
      print query
      c.execute(query)
      DB = c.fetchall()
      posts = [{'content': str(row[1]), 'time': str(row[0])} for row in DB]
      posts.sort(key=lambda row: row['time'], reverse=True)
      db.close()
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    new_content = bleach.clean(content)
    print new_content

    db = psycopg2.connect("dbname = forum")
    c = db.cursor()
    t = time.strftime('%c', time.localtime())
    #DB.append((t, content))
    # use tuple for query?? query is performed safely this way, python safe mode
    #query paramter instead of string substitution
    c.execute("insert into posts (content) values (%s) ", (new_content,))
    db.commit()
    db.close()
