from flask import Flask, render_template

from routes.invoice import invoice_bp
from routes.users import users_bp
from routes.customer import customer_bp
from routes.payment_methods import payment_methods_bp
from routes.discounts import discount_bp
from routes.taxes import invoice_taxes_bp
from routes.branches import branches_bp
from routes.invoice_payments import invoice_payments_bp
from routes.productos import products_bp
from routes.logs import logs_bp
from routes.product_discount import product_discount_bp

app = Flask(__name__)

#Blueprints de todos los endpoints
app.register_blueprint(users_bp)
app.register_blueprint(customer_bp)
app.register_blueprint(invoice_bp)
app.register_blueprint(payment_methods_bp)
app.register_blueprint(discount_bp)
app.register_blueprint(invoice_taxes_bp)
app.register_blueprint(branches_bp)
app.register_blueprint(invoice_payments_bp)
app.register_blueprint(products_bp)
app.register_blueprint(logs_bp)
app.register_blueprint(product_discount_bp)

#----Endpoints----
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/setting', endpoint='setting')
def setting():
    return render_template('settings/index.html')

@app.route('/settings/new', endpoint='settings/new')
def setting_new():
    return render_template('settings/form.html')


#---EEjecución de la app---

if __name__ == '__main__':
    app.run(debug=True)