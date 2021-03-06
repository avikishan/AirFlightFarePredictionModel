import joblib
import numpy as np
import os

from inference_schema.schema_decorators import input_schema, output_schema
from inference_schema.parameter_types.numpy_parameter_type import NumpyParameterType
from sklearn.ensemble import RandomForestRegressor

# The init() method is called once, when the web service starts up.
#
# Typically you would deserialize the model file, as shown here using joblib,
# and store it in a global variable so your run() method can access it later.
def init():
    global model

    # The AZUREML_MODEL_DIR environment variable indicates
    # a directory containing the model file you registered.
    model_filename = 'sklearn_regression_model.pkl'
    model_path = os.path.join(os.environ['AZUREML_MODEL_DIR'], model_filename)
    model = joblib.load(model_path)


# The run() method is called each time a request is made to the scoring API.
#
# Shown here are the optional input_schema and output_schema decorators
# from the inference-schema pip package. Using these decorators on your
# run() method parses and validates the incoming payload against
# the example input you provide here. This will also generate a Swagger
# API document for your web service.
@input_schema('data', NumpyParameterType(np.array([[2,21,5,15,5,1,30,10,25,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0]])))
@output_schema(NumpyParameterType(np.array([16689.04177428127])))
def run(data):
    # Use the model object loaded by init().
    result = model.predict(data)

    # You can return any JSON-serializable object.
    return result.tolist()


