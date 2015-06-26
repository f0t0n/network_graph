import os


APP_DIR = os.path.dirname(os.path.abspath(__file__))


class Config(object):
    DEBUG = False
    GRAPH_DB_PATH = os.path.join(APP_DIR, 'network_graph.json')


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
