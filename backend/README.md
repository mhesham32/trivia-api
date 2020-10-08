# Full Stack Trivia API Backend

you have to set the proxy in your front-end application in order to use the endpoints as the following format or you need to add `http://localhost:5000` before every endpoint

```

Endpoints
GET '/api/categories'
GET '/api/questions'
POST '/api/questions'
DELETE '/api/questions/<int:id>'
POST '/api/questions/search'
GET '/api/categories/<int:id>/questions'
POST '/api/quizzes'

GET '/api/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET '/api/questions'
- fetches a dictionary of all questions plus all categories
- Request Arguments: None
_ returns object the contains list of all questions for every question to be in this format {
            'id': int,
            'question': str,
            'answer': str,
            'category': int,
            'difficulty': int
        }
plus a list of all categories.

POST '/api/questions'
- adds a new question to the database
- Request Arguments: {question:str, answer:str, category:int, difficulty:int}
- if success it returns the following {
                "success": True,
                "code": 201
            }

DELETE '/api/questions/<int:id>'

- deletes a question from database
- Request arguments: <int:id>
- returns if success {
            "success": True,
            "code": 200,
        }

POST '/api/questions/search'

- searches for questions that contains simialr words of the search term
- Request Arguments: {search_term:str}
- returns if success {
                'questions': `all related questions`,
                'total_questions': `number of related questions`
            }

GET '/api/categories/<int:id>/questions'

- returns all the questions of a category by its id
- Request Argument: <int:category_id>

POST '/api/quizzes'

- returns a random question for a given category
- Request Arguments: {quiz_category:`category object`,              previous_questions: [list of questions ids]}

```

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
