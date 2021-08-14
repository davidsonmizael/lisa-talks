# LISA Talks
## _LISA Application Backend_

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

LISA Talks is one part of the application backend for LISA, which evolves around processing natural language to understand the users input.

## Features

- Trains the model based on a single Intent file
- Test the model with a list of inputs
- MongoDB integration to load Intents for model training
- Simple API to consume the model predictions

#### TODO

- Implement connection with a sql database for authentication

## Utilization

Create a virtual environment to run the project
```
cd lisa-talks
virtualenv venv
source venv/bin/activate
```

Use `setup.py` to install the dependencies and generate the model to run locally.

```sh
python setup.py develop
```

## Libraries

LISA Talks is currently using the following libraries.
Instructions on how to use them in your own application are linked below.

| Plugin | README |
| ------ | ------ |
| Natural Language Toolkit | [NLTK Website][PlNltk] |
| Pickle | [Python Docs for Pickle][PlPk] |
| Numpy | [Numpy Official Docs][PlNp] |
| Tensorflow | [Tensorflow Official Docs][PlTf] |
| Flask | [Flask Official Docs][PlFl] |

## License

MIT

   [PlNltk]: <https://www.nltk.org/>
   [PlPk]: <https://docs.python.org/3/library/pickle.html>
   [PlNp]: <https://numpy.org/doc/>
   [PlTf]: <https://www.tensorflow.org/api_docs/python/>
   [PlFl]: <https://flask.palletsprojects.com/en/2.0.x/>