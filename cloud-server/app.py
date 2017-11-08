import argparse
from admin_app_config import (server, admin)
from admin_views import add_admin_views
from init_dash import user_dash


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Server run options')
    parser.add_argument('port', type=int)
    parser.add_argument('--debug', action='store_true', default=False)
    args = parser.parse_args()

    app = user_dash(server)
    add_admin_views(admin, app)
    with app.app_context():
        app.run_server(host='0.0.0.0', port=args.port, debug=args.debug)
