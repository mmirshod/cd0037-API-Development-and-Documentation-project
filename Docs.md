# Trivia API

## Usage:

### Authentication:

*Current version of app do NOT require/provide any authentication or API key.*

### *By API URL:*

- *Currently, API can be accessed only by downloading on your local computer

### *On your local computer:*

Steps:
1. Fork repository to your account.
2. Clone it to local machine
3. Define variables `FLASK_ENV` and `FLASK_APP`
```
$ export  FLASK_APP={project_directory}
$ export FLASK_ENV=development
```
4. Run backend application using:
```
$ flask run
```

**NOTE:** *by default it will run on:* ```127.0.1:5000```. *And all routes are given relative to it.
i.e.:* `127.0.1:5000/questions` === `/questions` 


## Endpoints:

### 1. `GET` Requests:

> #### *1.1. All Categories `GET /categories`*
>
> **Parameters:** `None`
> 
> **Return type:** `JSON Object`
> 
> **Return Object:**
> ```
> {
>     'success': True, 
>     'categories': <list of strings>, 
>     'total_categories': <Number of categories>
> }
> ```

> #### *1.2. Paginated Questions `GET /questions?page=${page_num}`*
> 
> **Parameters:** `page_num[:int]` &rarr; Number of the page
> 
> **Return Type:** `JSON Object`
> 
> **Return Object:**
> ```
> {
>     'questions': <list of objects>,
>     'total_question': <Number of questions (total)>
>     'categories': <list of strings>, 
> }
> ```

> #### *1.3. Questions by Category* [`GET /questions/<int: category_id>?page=${page_num}`]
> 
> **Parameters:** 
> 
> `page_num[:int]` &rarr; Number of the page
> 
> `category_id[:int]` &rarr; Category
> 
> **Status Code:** `200. OK`
> 
> **Return Type:** `JSON Object`
> 
> **Return Object:**
> ```
> {
>     'success': True
>     'questions': <list: question objects>,
>     'total_question': <int: Number of questions (total)>
>     'current_category': <str: current category>
> }
> ```
> 
> **Troubleshooting:**
> 
> + `404. Not Found`:
>   + User have typed URL by himself, check for correctness of `category_id`
> + No more Errors are expected

### 2. `POST` Requests:

> #### *2.1. Create Question `POST /questions`*
>
> **Parameters:** `None`
> 
> **Sent Data:**
> 
> `JSON Object`
> 
> ```
> {
>     'question': <str: question name>
>     'answer': <str: answer>
>     'difficulty': <int: difficulty level>
>     'categort': <str: category name>
> }
> ```
> 
> **Return type:** `JSON Object`
> 
> **Return Object:**
> ```
> {
>     'success': True, 
>     'message': "New Question has been added."
> }
> ```
> 
> **Troubleshooting:**
> 
> + `404. Not Found`:
>   + User have typed URL by himself, check for correctness of `category_id`
> + `422. Not Proccessable`:
>   + User has violated data type validation
> + `500. Server Side Error`:
>   + Problems on the site of backend. Contact to developers
> + No more Errors are expected

> #### *2.2. Search Question `POST /questions/search`*
>
> **Parameters:** `None`
> 
> **Sent Data:**
> 
> `JSON Object`
> 
> ```
> {
>    'search_term': <str: prompt>
> }
> ```
> 
> **Return type:** `JSON Object`
> 
> **Return Object:**
> ```
> {
>     'questions': <list: question objects>, 
>     'total_questions': <int: total found>
> }
> ```
> 
> **Troubleshooting:**
>
> + No Errors are expected

> #### *2.3. Play Quiz `POST /quizzes`*
>
> **Parameters:** `None`
> 
> **Sent Data:**
> 
> `JSON Object`
> 
> ```
> {
>     'previous_questions': <list: previous question objects>
>     'quiz_category': <str: category>
> }
> ```
> 
> **Return type:** `JSON Object`
> 
> **Return Object:**
> ```
> {
>     'question': <object: question>, 
>     'success': True
> }
> ```
> 
> **Troubleshooting:**
>
> + `422. Not Proccessable`:
>   + User probably has answered all questions
> + No more Errors are expected

### 3. `DELETE` Requests:

> #### *3.1. Delete Question* [`GET /questions/<int: question_id>`]
> 
> **Parameters:**
> `question_id[:int]` &rarr; Question
> 
> **Status Code:** `200. OK`
> 
> **Return Type:** `JSON Object`
> 
> **Return Object:**
> ```
> {
>     'success': True,
>     'message': "Question deleted successfully."
> }
> ```
> 
> **Troubleshooting:**
> 
> + `404. Not Found`:
>   + User have typed URL by himself, check for correctness of `question_id`
> + `500. Server Error`:
>   + Problems on the site of backend. Contact to developers
> + No more Errors are expected