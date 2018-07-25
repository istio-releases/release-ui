import logging
import os
import lib.cloudstorage as gcs
from resources.release_id_parser import release_id_parser

def read_file(bucket_name, release_id, task_name):
  dag_id, execution_date = release_id_parser(release_id)
  logging.debug('execution_date from read_file: ' + str(execution_date))
  execution_date = str(execution_date).replace(' ', 'T')  # put into same format as gcs bucket
  logging.debug('after T replacement: ' + str(execution_date))
  filename = '/' + bucket_name + '/logs/' + dag_id + '/' + task_name + '/' + str(execution_date) + '/' + '1.log'
  gcs_file = gcs.open(filename)
  contents = gcs_file.read()
  gcs_file.close()
  print contents
  print ''
  print gcs_file
  return contents
