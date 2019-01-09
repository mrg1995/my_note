from flask_script import Manager
from app import create_app
from flask_migrate import MigrateCommand

app = create_app('default')
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.route('/index/<name>', methods=['POST', 'GET'])
def hello_world(name):
    # print(name)
    # print(request.json)
    # print(request.script_root)
    # print(request.url_root)
    # print(request.host_url)
    # print(request.host)
    return 'Hello World!'


if __name__ == '__main__':
    # app.run(debug=True)
    manager.run()
