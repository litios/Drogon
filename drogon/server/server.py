import connexion
from connexion.resolver import MethodViewResolver

# Create the application instance
app = connexion.FlaskApp(__name__, specification_dir='./')

# Read the swagger.yml file to configure the endpoints
app.add_api('api.yml', resolver=MethodViewResolver('routes'))

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
