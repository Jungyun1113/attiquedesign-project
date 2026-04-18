from chalice import Chalice

from chalicelib.api.auth import auth_bp
from chalicelib.api.products import products_bp
from chalicelib.api.orders import orders_bp
from chalicelib.api.reservations import reservations_bp
from chalicelib.api.portfolios import portfolios_bp
from chalicelib.api.selections import selections_bp
from chalicelib.api.uploads import uploads_bp
from chalicelib.api.webhooks import webhooks_bp

app = Chalice(app_name="attique-project")
app.debug = True

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
