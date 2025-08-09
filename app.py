from flask import Flask, render_template, request, flash, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'fiklar-secret-key-2025'

# Configuration
app.config['DEBUG'] = True

# Données des produits (simulation base de données)
PRODUCTS_DATA = {
    'engines': [
        {
            'id': 1,
            'name': 'Moteur Caterpillar C15',
            'brand': 'caterpillar',
            'category': 'Moteurs',
            'description': 'Moteur diesel haute performance pour applications lourdes',
            'price': 'Sur devis',
            'image': '🔧'
        },
        {
            'id': 2,
            'name': 'Bloc Moteur Doosan',
            'brand': 'doosan',
            'category': 'Moteurs',
            'description': 'Bloc moteur complet pour excavateurs Doosan',
            'price': 'Sur devis',
            'image': '⚙️'
        },
        {
            'id': 3,
            'name': 'Kit Moteur Volvo D13',
            'brand': 'volvo',
            'category': 'Moteurs',
            'description': 'Kit de révision complète moteur Volvo D13',
            'price': 'Sur devis',
            'image': '🛠️'
        }
    ],
    'hydraulics': [
        {
            'id': 4,
            'name': 'Pompe Hydraulique CAT',
            'brand': 'caterpillar',
            'category': 'Hydraulique',
            'description': 'Pompe hydraulique principale pour excavateurs',
            'price': 'Sur devis',
            'image': '💨'
        },
        {
            'id': 5,
            'name': 'Vérin Hydraulique Doosan',
            'brand': 'doosan',
            'category': 'Hydraulique',
            'description': 'Vérin de flèche pour excavateurs Doosan',
            'price': 'Sur devis',
            'image': '🔧'
        },
        {
            'id': 6,
            'name': 'Distributeur Hydraulique Volvo',
            'brand': 'volvo',
            'category': 'Hydraulique',
            'description': 'Distributeur hydraulique multi-voies Volvo',
            'price': 'Sur devis',
            'image': '⚡'
        }
    ]
}

COMPANY_INFO = {
    'name': 'Fiklar',
    'slogan': 'Votre Partenaire Industriel de Confiance',
    'description': 'Spécialisée dans la vente de pièces détachées et équipements industriels pour les marques Caterpillar, Doosan et Volvo',
    'location': 'Marrakech, Maroc',
    'email': 'contact@fiklar.ma',
    'phone': '+212 5 24 XX XX XX',
    'whatsapp': '+212600000000',
    'services': [
        'Pièces détachées neuves',
        'Équipements industriels',
        'Livraison nationale et internationale',
        'Support technique 24/7',
        'Devis gratuits',
        'Garantie qualité'
    ],
    'brands': ['Caterpillar', 'Doosan', 'Volvo'],
    'years_experience': 10,
    'clients_count': 500,
    'products_count': 1000
}

@app.route('/')
def accueil():
    """Page d'accueil"""
    # Produits récents pour la homepage
    recent_products = []
    for category in PRODUCTS_DATA.values():
        recent_products.extend(category[:2])  # 2 produits par catégorie
    
    return render_template('accueil.html', 
                         company=COMPANY_INFO,
                         recent_products=recent_products[:6])

@app.route('/about')
def about():
    """Page À propos"""
    return render_template('about.html', 
                         company=COMPANY_INFO)

@app.route('/produits')
def produits():
    """Page des produits"""
    # Organiser tous les produits par catégorie
    all_products = {}
    for category, products in PRODUCTS_DATA.items():
        all_products[category] = products
    
    return render_template('produits.html', 
                         products=all_products,
                         company=COMPANY_INFO)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Page de contact avec formulaire"""
    if request.method == 'POST':
        # Récupération des données du formulaire
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        subject = request.form.get('subject', 'Demande générale')
        message = request.form.get('message', '').strip()
        product = request.form.get('product', '').strip()
        quantity = request.form.get('quantity', 1)
        
        # Validation simple
        if not name or not email or not message:
            flash('Veuillez remplir tous les champs obligatoires.', 'error')
            return render_template('contact.html', company=COMPANY_INFO)
        
        # Simulation d'envoi d'email (ici on affiche juste un message de succès)
        try:
            # Dans un vrai projet, ici vous enverriez l'email avec:
            # - Flask-Mail
            # - SendGrid API
            # - Ou sauvegarder dans une base de données
            
            # Log de la demande (simulation)
            log_entry = f"""
            [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Nouvelle demande:
            Nom: {name}
            Email: {email}
            Téléphone: {phone}
            Sujet: {subject}
            Produit: {product if product else 'N/A'}
            Quantité: {quantity if product else 'N/A'}
            Message: {message}
            ---
            """
            
            # En développement, on peut écrire dans un fichier log
            if app.config['DEBUG']:
                with open('contact_logs.txt', 'a', encoding='utf-8') as f:
                    f.write(log_entry)
            
            flash('Votre message a été envoyé avec succès! Nous vous recontacterons dans les plus brefs délais.', 'success')
            return redirect(url_for('contact'))
            
        except Exception as e:
            flash('Une erreur est survenue lors de l\'envoi de votre message. Veuillez réessayer.', 'error')
            if app.config['DEBUG']:
                print(f"Erreur contact: {e}")
    
    return render_template('contact.html', company=COMPANY_INFO)

@app.route('/api/products')
def api_products():
    """API simple pour récupérer les produits (pour futures intégrations)"""
    all_products = []
    for category, products in PRODUCTS_DATA.items():
        all_products.extend(products)
    return {'products': all_products, 'total': len(all_products)}

@app.route('/api/brands')
def api_brands():
    """API pour récupérer les marques"""
    brands = set()
    for category in PRODUCTS_DATA.values():
        for product in category:
            brands.add(product['brand'])
    return {'brands': list(brands)}

# Gestion d'erreurs
@app.errorhandler(404)
def page_not_found(e):
    """Page d'erreur 404 personnalisée"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Page d'erreur 500 personnalisée"""
    return render_template('500.html'), 500

# Filtres template personnalisés
@app.template_filter('capitalize_first')
def capitalize_first_filter(text):
    """Filtre pour capitaliser la première lettre"""
    return text.capitalize() if text else ''

@app.template_filter('format_brand')
def format_brand_filter(brand):
    """Filtre pour formater les noms de marques"""
    brand_names = {
        'caterpillar': 'Caterpillar',
        'doosan': 'Doosan',
        'volvo': 'Volvo'
    }
    return brand_names.get(brand.lower(), brand)

# Context processor pour variables globales
@app.context_processor
def inject_globals():
    """Injecte des variables globales dans tous les templates"""
    return {
        'current_year': datetime.now().year,
        'company_name': COMPANY_INFO['name'],
        'company_email': COMPANY_INFO['email'],
        'company_phone': COMPANY_INFO['phone'],
        'whatsapp_link': f"https://wa.me/{COMPANY_INFO['whatsapp'].replace('+', '').replace(' ', '')}"
    }

if __name__ == '__main__':
    # Créer le dossier templates s'il n'existe pas
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Créer le dossier static s'il n'existe pas
    if not os.path.exists('static'):
        os.makedirs('static')
        os.makedirs('static/css')
        os.makedirs('static/js')
        os.makedirs('static/images')
    
    # Lancer l'application
    print("🚀 Démarrage de l'application Fiklar...")
    print("📍 Accès: http://localhost:5000")
    print("📧 Logs des contacts: contact_logs.txt")
    
    app.run(debug=True, host='0.0.0.0', port=5000)