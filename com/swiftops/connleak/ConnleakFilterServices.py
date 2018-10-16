from pymongo import MongoClient
from flask import jsonify
import json
import configparser

config = configparser.ConfigParser()
config.read("com/swiftops/connleak/db_conn.ini")


def get_nightly_data(release, build):
    """
            This api finds connection leak data from mongo db for given release and build number
            :return: connection leak data with release and build number in jason format.
    """

    error_data = {}
    try:

        db_ip = config.get("db_properties", "DB_IP")
        db_port = int(config.get("db_properties", "DB_PORT"), 10)
        db_user = config.get("db_properties", "DB_USERNAME")
        db_pwd = config.get("db_properties", "DB_PASSWORD")
        db_name = config.get("db_properties", "DB_NAME")
        client = MongoClient(host=db_ip, port=db_port)
    except Exception as e:
        error_data["status_code"] = 404
        error_data["error_msg"] = "exception occurred while reading config file. Exception is " + e.__str__()
        return build_error_response(error_data)
    try:
        mongo_perf_db = client[db_name]
        mongo_perf_db.authenticate(db_user, db_pwd)
        db = mongo_perf_db.connleak_nightly_build
        data_package = db.find({"Release No": release, "Build No": build})
        result = 'No Connleak found for release ' + release +'and build '+ build
        for param in data_package:
            result = param['total']
            tabular_result = param['tabulardata']
            break
        data = {"total": result, "tabulardata": tabular_result}
        return get_success_response(data)

    except Exception as e:
        error_data["status_code"] = 404
        error_data["error_msg"] = "exception occurred while adding records to mongo " + e.__str__()
        return build_error_response(error_data)


def get_success_response(data):
    """
       this api forms response for success
       :return: success response in jason format
    """
    return_data={}
    return_data["success"] = "true"
    return_data["data"] = data
    return_data["error"] = {}
    return json.dumps(return_data)


def build_error_response(data):
    """
            This api forms response for failure
            :return: failure response in jason format
    """
    return_data = {}
    return_data["success"] = "false"
    return_data["data"] = {}
    return_data["error"] = data
    return json.dumps(return_data)
