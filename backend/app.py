from chalice import Chalice

from chalicelib.api.auth import auth_bp
from chalicelib.api.products import products_bp
from chalicelib.api.orders import orders_bp
from chalicelib.api.reservations import reservations_bp
from chalicelib.api.portfolios import portfolios_bp
from chalicelib.api.selections import selections_bp
from chalicelib.api.uploads import uploads_bp
from chalicelib.api.webhooks import webhooks_bp

from chalicelib.core.db import create_db_and_tables
# Import all models to ensure they are registered with SQLModel.metadata
from chalicelib.models import user, product, order, reservation, portfolio, selection, waitlist # noqa

app = Chalice(app_name="attique-project")
app.debug = True

# Create tables if they don't exist
try:
    create_db_and_tables()
except Exception as e:
    print(f"INFO: Database initialization deferred: {e}")

app.register_blueprint(auth_bp)
app.register_blueprint(products_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(reservations_bp)
app.register_blueprint(portfolios_bp)
app.register_blueprint(selections_bp)
app.register_blueprint(uploads_bp)
app.register_blueprint(webhooks_bp)


@app.route("/health", methods=["GET"], cors=True)
def health():
    return {"status": "ok"}


@app.route("/debug/aws-account", methods=["GET"], cors=True)
def debug_aws_account():
    import boto3
    sts = boto3.client("sts")
    identity = sts.get_caller_identity()
    return {"account": identity["Account"], "arn": identity["Arn"]}
