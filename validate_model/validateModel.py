from mlflow.tracking import MlflowClient
from mlflow.entities import ViewType

import mlflow
import os 

client = MlflowClient('validate_model/mlruns')

experiments = client.list_experiments(view_type=ViewType.ACTIVE_ONLY)

fscore = 0.7 # fscore meno que 0.7 são eliminados. Para todos os maiores que 0.7, escolher o maior
max_fscore = 0
final_model =[]

for experiment in experiments:
    listModel = client.list_run_infos(experiment.experiment_id)
    for model in listModel:
        model.artifact_uri, model.run_uuid
        data = client.get_run(model.run_uuid).data
        if data.metrics['f1_score'] >= fscore:
            if data.metrics['f1_score'] > max_fscore:
                experiment_name = experiment.name
                max_fscore = data.metrics['f1_score']
                final_model = model.artifact_uri.partition('TCC/')
print ('Experiment name: {}'.format(experiment_name))
print('Max fscore: ' + str(max_fscore))
print('Variation with max fscore (path): {}'.format(final_model[2]))   

os.system("cp -r {0} {1}".format(final_model[2] + "/model/data/model", 'apiFungalDisease/'))

