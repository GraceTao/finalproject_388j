# Career Search Website

## Link to the App:
You can check out the live app [here](https://finalproject-388j.vercel.app/).

## Overview:
Our website is essentially a career search site where users can explore different careers, save careers, and take a careers quiz that returns the top jobs aligning with their personality and interests. The homepage for users who are not logged in displays a button to go to all careers, and choices to register or login. The careers archive provides links to careers in alphabetical order, and displays a career details page for specific careers. Once logged in, the account page displays the user’s previous results from the quiz as well as any previously saved jobs, which are stored in a Mongo database. A logged-in user can save a job on any career details page. 

Only logged-in users can take the careers quiz or save a job.

## Forms:
- **Registration**: Same as project 4’s, allows users to register with a new username and password.
- **Login**: Same as project 4’s, allows users to log in with username and password.
- **Search**: Allows users to search for a career. The API is then queried for the top 21 closest matches, which are displayed as links to career details pages. This form is present on every single page.
- **Quiz**: When a user finishes taking the quiz (embedded as a widget), they can enter their top three career choices from the list of results displayed by the widget. These results are stored in the database and loaded onto the account page every time a user logs in.
- **Save Job**: Allows users to save the job whose page they are currently viewing. Each saved job is appended to a list of the user’s saved jobs stored in the database and displayed as links on the user’s account page.

## Blueprints and Routes:
### Careers Blueprint:
- **`/`**: Home page.
- **`/all-careers/<start>`**: Queries the API for 20 careers starting from index `<start>` and displays the results as links to career details pages. Pagination (of size 20) is used for efficient retrieval of results.
- **`/career/<code>`**: Once a user clicks on a career to learn more about, its career code is passed in to the route (and the API call) and details about the career are displayed.
- **`/search-results/<query>`**: Displays the top 21 closest matches to the `<query>` as links to career details pages.

### Users Blueprint:
- **`/register`**, **`/login`**, **`/logout`**: Same as project 4.
- **`/account`**: Landing page for the user upon logging in. Displays previous quiz results and saved jobs. A ‘take quiz’ button is also displayed.
- **`/quiz`**: Displays the careers quiz widget from O*NET and the form for users to input top three careers after taking the quiz.

## MongoDB:
- Stores user details, including username, email, password, quiz results, and saved jobs.
- Login information will be used to verify if a user has registered or not and if they're logging in correctly. Saved jobs and quiz results from previous sessions will also be retrieved on new sessions.

## O*NET Web Services API:
We use this API to retrieve all information pertaining to careers, including their “Search careers with key words”, “O*NET Interest Profiler”, “See all careers”, and “Full career report” endpoints. This information is used in various endpoints to display career lists, career details, and search results.
