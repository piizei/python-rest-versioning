import os
import logging
from app.model.model import fit
import shutil

# This is entry file for Azure ML online rest services (see deployment in notebooks/control)


def init():
    """
    This function is called when the container is initialized/started, typically after create/update of the deployment.
    You can write the logic here to perform init operations like caching the model in memory
    """
    #global model
    # AZUREML_MODEL_DIR is an environment variable created during deployment.
    # It is the path to the model folder (./azureml-models/$MODEL_NAME/$VERSION)
    #model_path = os.path.join(
    #    os.getenv("AZUREML_MODEL_DIR"), "sklearn_regression_model.pkl"
    #)
    # deserialize the model file back into a sklearn model
    #model = joblib.load(model_path)

    # We don't really have a trained ML model here, we just want to execute our python module
    # (in cloud deployment the model would be stored outside of the VM and mounted)
    # Copy the model dir to name of the module, so that the imports work
    model_dir = os.getenv("AZUREML_MODEL_DIR")
    if model_dir:
        try:
            shutil.copytree(model_dir, "./app")
        except:
            print("Model dir already existed, since this is just a demo not really reacting to it...")

    logging.info("Init complete")


def run(raw_data):
    """
    This function is called for every invocation of the endpoint to perform the actual scoring/prediction.
    In the example we extract the data from the json input and call the scikit-learn model's predict()
    method and return the result back
    """
    logging.info("Request received")
    logging.info("Request processed")
    return {'version':'3', 'fit': fit().tolist() }
