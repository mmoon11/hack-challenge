# AppHub
A centralized hub for all Cornell clubs and organizations recruitment.

### iOS GitHub

### Description
A centralized hub for all Cornell clubs and organizations to post their applications, coffee chats, or upcoming recruitment events, and a place for students to access all applications in one place. Clubs/organizations can post any recruitment information and/or links, and applicants can find all their recruitment resources through this hub.

### Requirements
- Uses GET, POST, DELETE requests
  - GET /api/categories/: gets all categories
  - GET /api/applications/: gets all application posts
  - GET /api/applications/<string:category>: gets all application posts from one category
  - POST /api/applications/: creates a new application post
  - DELETE /api/applications/<int:application_id>: deletes application post by id
- Uses 2 tables for Categories and Applications (one-to-many)
  
