import os
from flask import Flask
from config import APP_DIR


# Extend base application class
class App(Flask):
    pass


# Create application
app = App(__name__)

# Configure
app.config.from_object('network_graph.config.DevelopmentConfig')


# Import controllers to access their blueprints
from network_graph.controllers import main
from network_graph.controllers import network_table

# Register blueprints
app.register_blueprint(main.blueprint, url_prefix='/')
app.register_blueprint(network_table.blueprint, url_prefix='/network-table')
