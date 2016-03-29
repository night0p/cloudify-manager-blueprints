import sys

from cloudify_system_workflows import db_helper

es_endpoint = sys.argv[1]
port = int(sys.argv[2])
dump = sys.argv[3]
data_path = sys.argv[4]


def dump_es_data():
    db_helper.local_dump_elasticsearch_data(data_path,
                                            endpoint=es_endpoint,
                                            port=port)


def restore_es_data():
    db_helper.local_restore_elasticsearch_data(data_path,
                                               endpoint=es_endpoint,
                                               port=port)


if dump == 'True':
    dump_es_data()
else:
    restore_es_data()
