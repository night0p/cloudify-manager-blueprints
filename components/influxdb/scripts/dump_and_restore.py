import sys

from cloudify_system_workflows import db_helper

influxdb_endpoint = sys.argv[1]
port = int(sys.argv[2])
dump = sys.argv[3]
data_path = sys.argv[4]


def dump_influxdb_data():
    db_helper.local_dump_influxdb_data(data_path,
                                       endpoint=influxdb_endpoint,
                                       port=port)


def restore_influxdb_data():
    db_helper.local_restore_influxdb_data(data_path,
                                          endpoint=influxdb_endpoint,
                                          port=port)


if dump == 'True':
    dump_influxdb_data()
else:
    restore_influxdb_data()
