## Database diagram

![Database diagram](diagram.png)

User can submit many threads but each thread has only one submitter. Users can also add many threads to favorites and threads can be added to favorites by many users. Users can also upvote many threads and threads may be upvoted by multiple users. Thread contains a field called *upvotes* that keeps track of the number of upvotes a thread has received. This field may be deleted in the future in favor of an aggregate query. Threads can have many comments but each comment belongs to a single thread. Users can write many comments but each comment is written by a single user.