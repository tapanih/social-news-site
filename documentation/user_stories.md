## User stories

### As an user, I want to browse interesting news articles so I can read them.

The main page provides a list of posts that may contain links to news articles. The list of posts is sorted by upvotes to show articles that other users found interesting. Users also have karma that is acquired when submitted posts are upvoted.

#### SQL statements

Posts are fetched with
```sql
SELECT post.id, post.date_created, post.content, post.title, post.is_text,
(SELECT COUNT(*) FROM Upvote WHERE post_id = post.id) as post_upvotes,
(SELECT COUNT(*) FROM Upvote WHERE post_id = post.id AND account_id = <current_user_id>) as has_upvoted,
account.username as post_author,
COUNT(Comment.post_id) as post_comments FROM post
LEFT JOIN Account ON Account.id = Post.account_id
LEFT JOIN Comment ON Comment.post_id = Post.id
GROUP BY Post.id, Account.id
ORDER BY post_upvotes DESC
LIMIT <posts_per_page> OFFSET ((<page> - 1) * <posts_per_page>);
```

Upvotes are inserted with
```sql
INSERT INTO upvote (account_id, post_id) VALUES (<current_user_id>, <upvoted_post_id>)
```

Users' karma is calculated with
```sql
SELECT COUNT(*) FROM post
LEFT JOIN Upvote ON Upvote.post_id = Post.id
WHERE post.account_id = <current_user_id>;
```

### As an user, I want to read comments so I can find out what other people think.

Clicking on a appropriate link below an entry opens the comment section for that entry. Inside the comment section, there is a button to add the post to favorites so following the discussion becomes easier.

#### SQL statements

Comments are fetched with
```sql
SELECT * FROM comment 
WHERE comment.post_id = <current_post_id> ORDER BY comment.date_created DESC;
```

### As an user, I sometimes want the posts sorted by date so I can find the latest news.

Clicking on a link on the main page opens a listing that is sorted by date (newest first).

#### SQL statements

Newest posts are fetched with
```sql
SELECT post.id, post.date_created, post.content, post.title, post.is_text,
(SELECT COUNT(*) FROM Upvote WHERE post_id = post.id) as post_upvotes,
(SELECT COUNT(*) FROM Upvote WHERE post_id = post.id AND account_id = <current_user_id>) as has_upvoted, 
account.username as post_author,
COUNT(Comment.post_id) as post_comments FROM post 
LEFT JOIN Account ON Account.id = Post.account_id 
LEFT JOIN Comment ON Comment.post_id = Post.id 
GROUP BY Post.id, Account.id 
ORDER BY post.date_created DESC
LIMIT <posts_per_page> OFFSET ((<page> - 1) * <posts_per_page>);
```

### As an user, I want to create posts so I can share news articles or start a discussion.

The main page provides a link to a form where the user can give the post a descriptive title and content that can be either a link to a news article or simply text. After submission, other users can see the post and add comments to it.

#### SQL statements

A post is created with
```sql
INSERT INTO post (date_created, date_modified, content, title, is_text, account_id) 
VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, <content>, <title>, <is_text>, <current_user_id>);
```

### As an user, I want to edit my posts/comments so I can fix spelling errors or update the text content.

Posts and comments have an edit button that opens a form with the previous content pre-filled. User can edit the content and press a submit button to confirm changes.

#### SQL statements

Posts are updated with
```sql
UPDATE post
SET date_modified=CURRENT_TIMESTAMP, content=<new_content>, title=<new_title>
WHERE post.id = <edited_post_id>;
```
and comments are updated with
```sql
UPDATE comment
SET date_modified=CURRENT_TIMESTAMP, content = <new_content>
WHERE comment.id = <edited_comment_id>;
```

### As an user, I want to delete my posts/comments if I feel they are unnecessary.

Posts and comments also have a delete button.

#### SQL statements
Posts along with associated comments and upvotes are deleted with
```sql
DELETE FROM post WHERE post.id = <deleted_post_id>;
DELETE FROM comment WHERE comment.post_id = <deleted_post_id>;
DELETE FROM upvote WHERE upvote.post_id = <deleted_post_id>;
```

Comments are deleted with
```sql
DELETE FROM comment WHERE comment.id = <deleted_comment_id>;
```