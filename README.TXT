===============================================================================
TRAVELTOGETHER - WEB APPLICATION PROJECT
Team 5

AUTHORS:
L Øyvind Nordbø: 100576766   
L Simon Volkmann: 100575156  
L Mathias Gjestad: 100576768 

===============================================================================
ADDITIONAL FUNCTIONALITY
===============================================================================

Beyond the 12 mandatory requirements, these additional features have been 
implemented for our project:

1. USER PROFILES WITH ALIASES
   - Users can set a display name (alias) instead of showing email addresses
   - Upon registering, users are prompted to set an alias and profile bio
   - Users can change their password from the profile edit page

2. LOCATION AUTOCOMPLETE
   - Integration with OpenStreetMap Nominatim API 
      - Real-time location suggestions for departure and destination fields
      - Clickable link to OpenStreetMap website in proposal forms 
   - Note: Limited to locations in OpenStreetMap database

3. PROPOSAL MANAGEMENT ENHANCEMENTS
   - Reopen closed proposals: 
      Editors can reopen "closed to new participants" proposals
   - Automatic editor transfer: 
      When an editor leaves and no other editors remain, rights transfer 
      automatically to the first remaining participant
   - Automatic cleanup:
      When last participant leaves, proposal is deleted
   - Role visibility: 
      All participants can see who has editor rights (editor/participant labels)

4. ENHANCED PROPOSAL DETAILS
   - Additional optional fields: Departure location and activities
   - Field validation: Budget cannot be negative, displays 0 instead of TBD when set to 0
   - Extended location fields: Support for longer addresses (255 characters)

5. IMPROVED NAVIGATION
   - Back buttons: Easy navigation from proposals and profile pages
   - Navigation bar: Quick access to proposals list and profile from detail pages
   - Browser history integration: Back button uses browser history

===============================================================================
HOW TO USE THE APPLICATION
===============================================================================

STEP 1: REGISTER A NEW USER
----------------------------
1. Navigate to http://localhost:5000
2. Click "Register" link
3. Enter your email address and password (minimum 6 characters)
4. Click "Register"
5. Set your alias (display name) and write a short bio about yourself
6. Click "Save" to complete registration

STEP 2: CREATE A TRIP PROPOSAL
-------------------------------
1. After logging in, click "+ Add proposal" button
2. Fill in the proposal details:
   - Title (required)
   - Departure location (with autocomplete suggestions)
   - Destination (with autocomplete suggestions)
   - Activities (comma-separated)
   - Budget (leave empty for TBD, or enter 0 or any positive number)
   - Max participants (required, default: 4)
   - Start date and End date (optional)
3. Click "Create"
4. You are automatically added as a participant with editor rights

STEP 3: VIEW AND JOIN PROPOSALS
--------------------------------
1. Browse the "Open proposals" list on the main page
2. Click "Join" to join a proposal created by another user
3. Click "Open" to view details of proposals you've already joined
4. View proposal information, participants, messages, and meetup suggestions

STEP 4: PARTICIPATE IN A PROPOSAL
----------------------------------
As a participant, you can:
- Post messages on the message board
- Suggest meetup times and locations
- View all participants and their roles (editor/participant)
- Leave the proposal by clicking "Leave"

STEP 5: MANAGE AS EDITOR
-------------------------
If you have editor rights (creator or granted by another editor), you can:

A. EDIT PROPOSAL DETAILS
   - Click the blue "Edit" button
   - Modify title, locations, dates, budget, activities, or max participants
   - Click "Save changes"

B. MANAGE PARTICIPANTS
   - Grant edit rights to other participants by clicking "Grant edit rights"
   - View all participants and their roles

C. CHANGE PROPOSAL STATUS
   - "Close to New": Stop accepting new participants
   - "Reopen to New": Allow new participants again (if previously closed)
   - "Finalize": Mark the trip as confirmed and final
   - "Cancel": Cancel the entire trip proposal

D. DELETE PROPOSAL
   - Click the X button in the top-right corner
   - Confirm deletion

STEP 6: MANAGE YOUR PROFILE
----------------------------
1. Click your profile link or "My Profile" button
2. Click "Edit profile"
3. Update your alias or bio
4. To change password:
   - Enter new password in "New Password" field
   - Confirm password in "Confirm New Password" field
   - Leave both fields empty to keep current password
5. Click "Save"

STEP 7: LEAVING PROPOSALS
--------------------------
When you leave a proposal:
- If you're the last participant, the proposal is automatically deleted
- If you're an editor and other participants remain without editor rights, 
  editor rights transfer to the first remaining participant automatically
- If the proposal was full, it reopens to new participants

===============================================================================
TEST USERS
===============================================================================

For more efficient testing, you can use the following user accounts:

User 1 (Creater of proposal):
  Email: test1@t1.com
  Password: Password

User 2 (Participant w/o permissions):
  Email: test2@t2.com
  Password: Password

User 3 (Newley created user, no proposals):
  Email: test3@t3.com
  Password: Password         

===============================================================================
IMPORTANT INFORMATION FOR TESTING
===============================================================================

DATABASE CONFIGURATION
----------------------
The application is configured to use the UC3M lab MariaDB infrastructure:
- Database: 26_webapp_34a
- Host: mysql.lab.it.uc3m.es
- User: 26_webapp_34

RUNNING THE APPLICATION
-----------------------
1. Ensure virtual environment is activated:
   source venv/bin/activate 

2. Run database migrations if needed:
   python migrate_add_proposal_fields.py

3. Start the application:
   python app.py

4. Access at: http://localhost:5000

TESTING WORKFLOW
----------------
1. Register a new user account or use test accounts above
2. Create a trip proposal with various details
3. Mark some information as "final" using checkboxes
4. Join proposals as different users to test collaboration
5. Test meetup creation with date/time
6. Try changing proposal status (close, finalize, cancel)
7. Test leaving proposals and automatic cleanup

KNOWN CONSIDERATIONS
--------------------
- Location autocomplete requires internet connection (uses OpenStreetMap API)
- Only proposal creators and users with can_edit permission can modify 
  proposals
- Proposals are automatically deleted when the last participant leaves

===============================================================================
ARTIFICIAL INTELLIGENCE DECLARATION
===============================================================================

We declare that artificial intelligence tools (specifically GitHub Copilot) were 
used during the development of this project for the following purposes:

1. CODE GENERATION AND ASSISTANCE
   - Generating boilerplate code for Flask routes and database models
   - Implementing form validation and error handling logic
   - Creating HTML templates with proper Jinja2 syntax
   - Writing SQL migration scripts

2. DEBUGGING AND OPTIMIZATION
   - Identifying and fixing bugs 
   - Optimizing database queries
   - Refactoring redundant code for better maintainability

3. DOCUMENTATION
   - Generating code comments and docstrings
   - Helping structure the README

All AI-generated code was reviewed, tested, and adapted by the team members 
to ensure it meets the project requirements and our quality standards. We 
take full responsibility for the final implementation and any issues that 
may arise from it.

The core architecture, design decisions, and business logic were conceived 
and implemented by the team members with AI serving as a development 
assistant tool.

===============================================================================
END OF README
===============================================================================
