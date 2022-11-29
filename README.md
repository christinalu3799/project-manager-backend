# Backend Code for Project Manager App

This repo houses the API for the [Project Manager application](https://projectxmanager.herokuapp.com/). This application was built using Flask and Postgres and deployed on Heroku.

To use this API, clone down this repo and run ```. venv/bin/activate``` in your terminal. 

You can use Postman to test the different endpoints using ```http://localhost:8000``` as the base url on your local server.

### Endpoints

**/api/v1/users/login** - POST request to log the user in
**/api/v1/users/register** - POST request to register a new user

**/api/v1/projects** - GET all projects
- Adding **/:project_id** at the end will retrieve the single project associated with this project id. 

**/api/v1/projects/tasks/:project_id**
**/api/v1/projects/logs/:project_id**
- These routes will retrieve all tasks and logs associated with a particular project using through a GET request. 

To add a new project, data should match the following body formats: 

*Add Project* 
{
    "project_name": "Christina's First Project",
    "project_deadline": "November 29, 2022",
    "project_description": "some description",
    "project_status": "not started"
}

*Add Task* 
{
    "task": "new task"
}
*Add Log* 
{
    "log": "new log entry"
}
👉🏼 [Click here to view my frontend repo](https://github.com/christinalu3799/project-manager-frontend)