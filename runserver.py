#!/usr/bin/env python
from network_graph import app

if __name__ == '__main__':
    app.run(debug=app.debug, host='0.0.0.0', port=5000)
