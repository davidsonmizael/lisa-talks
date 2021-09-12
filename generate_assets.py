import os
from scripts import test_mongodb_connection
from scripts import generate_pickle
from scripts import generate_models
from scripts import test_model

os.makedirs('logs', exist_ok=True)

test_mongodb_connection.test()
generate_pickle.generate()
generate_models.generate()
test_model.test()