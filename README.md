# float note ML API
### Flask microservice for image to text and NLP analysis of text for [float note app](https://github.com/mickeybarcia/float-note-server)
## tools used
- Microsoft OCR API to convert images of journal entries to text
- Microsoft sentiment API to generate sentiment scores
- Aylien summary API to generate summaries of text
- nltk to pick out keywords of a text
- Heroku for deployment

## local development
```
# get .env for development environment values
pip install -r requirements
python app.py
```
