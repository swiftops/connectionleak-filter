from flask import Flask, request
from com.swiftops.connleak import ConnleakFilterServices as ConFilter
import connexion
import json

app = Flask(__name__)
app = connexion.App(__name__)
#app.add_api('swagger.yaml')

@app.route('/api/connectionleak/v1/connfilterservice/', methods=['POST'])
def get_data_release():
    if request.method == 'POST':
        query = json.loads(request.data.decode())
        release = query.split(';')[0].split()[1].replace("_", ".")
        build = query.split(';')[1]
        return ConFilter.get_nightly_data(release, build)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6003, debug=True)