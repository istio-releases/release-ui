"""Copyright 2017 Istio Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Echo the python path
"""
import datetime
import logging
import sys

from airflow import DAG
from airflow.operators.python_operator import PythonOperator


YESTERDAY = datetime.datetime.combine(
    datetime.datetime.today() - datetime.timedelta(days=1),
    datetime.datetime.min.time())

default_args = {
    'owner': 'laane',
    'depends_on_past': False,
    # This is the date to when the airlfow pipline tryes to backfil to.
    'start_date': YESTERDAY,
    'email': 'laane@google.com',
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': datetime.timedelta(minutes=5),
}


def EchoPath(*args, **kwargs):
  path = sys.path
  logging.info( "the path is ___________________________________")
  logging.info(path)
  logging.info("Lets try importing the 'broken' modules---------------------------")
  import environment_config
  logging.info(environment_config)
  import istio_common_dag
  logging.info(istio_common_dag)
  logging.info("Lets try branches with C style call--------------------------")
  branches = istio_common_dag.AirflowGetVariableOrBaseCase(
    'current_release_branches', ['release-0.8'], True)
  logging.info(branches)
  logging.info("Lets try branches with dict style call--------------------------")
  branches = istio_common_dag.AirflowGetVariableOrBaseCase(
    var='current_release_branches', base=['release-0.8'], deserialize_json=True)
  logging.info(branches)

  return path,  str(environment_config), str(istio_common_dag)


sync_dag = DAG(
    'istio_setup_for_new_release',
    default_args=default_args,
    schedule_interval='15 4 * * *',
)

sync_git_repo = PythonOperator(
    task_id='echo-python-path',
    python_callable=EchoPath,
    provide_context=True,
    dag=sync_dag,
)

sync_dag
