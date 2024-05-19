# **CITS3403 Group Project**

## PokeDexZone

PokeDexZone is a web application for Pokémon enthusiasts to trade Pokémon cards. Users can create, view, edit, and delete trade requests, post comments, and interact with other users.

## DESCRIPTION:

- **Purpose of application:**
  - Facilitate the trading of Pokémon cards.
  - Allow users to interact and comment on trade requests.
  
- **Design:**
  - User-friendly and responsive interface using Bootstrap.
  - Secure user authentication and session management.
  
- **Use:**
  - Users can register and log in to create trade requests.
  - Users can comment on requests and interact with other users..

### GROUP MEMBERS:

| Student Number | Student Name   | GitHub Username |
| :------------- | :------------: | --------------: |
| 23782402       | Tanmay Aggarwal|         Tanryu7 |
| 24128968       | David Pang     |       pohhui247 |

### ARCHITECTURE SUMMARY
The application follows the MVC (Model-View-Controller) design pattern using Flask as the web framework. The SQLAlchemy ORM is used for database interactions. The main components include:

- **Models:** Define the database schema for users, requests, and comments.
- **Views:** Render HTML templates and handle user interactions.
- **Controllers:** Manage the logic and database operations.

### HOW TO LAUNCH FLASK WEB APPLICATION

(On Windows):

1. **Create a virtual environment labeled "venv":**
    ```bash
    py -m venv venv 
    ```

2. **Activate that virtual environment:**
    ```bash
    venv\scripts\activate
    ```

3. **Install the necessary packages within that environment:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set the flask app environment variable:**
    ```bash
    $env:FLASK_APP="app"
    ```

5. **Run the app in localhost, with debug enabled so changes are made live:**
    ```bash
    flask run --debug
    ```

(On Linux):

1. **Create a virtual environment labeled "venv":**
    ```bash
    python3 -m venv venv 
    ```

2. **Activate that virtual environment:**
    ```bash
    source venv/bin/activate
    ```

3. **Install the necessary packages within that environment:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set the flask app environment variable:**
    ```bash
    export FLASK_APP="app"
    ```

5. **Run the app in localhost, with debug enabled so changes are made live:**
    ```bash
    flask run --debug
    ```

## Usage

1. **Home Page:**
    - Introduction to PokeDexZone.

2. **Registration and Login:**
    - New users can register.
    - Existing users can log in.

3. **Dashboard:**
    - View all requests.
    - Delete or comment on requests.

4. **Profile:**
    - View and edit profile information.
    - Change password.
    - View user-specific requests.

5. **Create Request:**
    - Users can create new requests.

6. **Contact:**
    - Contact information.

## Routes

### Main Routes
- `/` - Home Page
- `/dashboard` - Dashboard showing requests from all the users
- `/create_request` - Create a new request
- `/contact` - Contact page
- `/profile` - View and edit profile, change password, view your own personal requests

### Auth Routes
- `/login` - Login page
- `/register` - Registration page
- `/logout` - Logout

### Additional Routes
- `/add_comment/<int:request_id>` - Add a comment to a request
- `/delete_request/<int:request_id>` - Delete a request
- `/edit_request/<int:request_id>` - Edit a request
- `/delete_comment/<int:comment_id>` - Delete a comment


## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch-name`.
3. Make your changes and commit them: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature-branch-name`.
5. Submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements
- Inspired by our love for Pokémon.
  
