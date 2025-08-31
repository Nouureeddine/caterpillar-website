from flask import Flask, render_template, request, flash, redirect, url_for
import os
from datetime import datetime
import secrets
from data import PRODUCTS_DATA, COMPANY_INFO

app = Flask(__name__)

# Security: Generate secret key from environment or use a secure random one
app.secret_key = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(32))

# Configuration
app.config['DEBUG'] = str(os.environ.get('FLASK_DEBUG', '')).lower() in ('1', 'true', 'yes', 'on')

def save_contact_to_log(sender_name: str, sender_email: str, message_body: str) -> None:
    """Save contact form content to contact_logs.txt file."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] Contact Form Submission\n"
    log_entry += f"Name: {sender_name or 'Not provided'}\n"
    log_entry += f"Email: {sender_email or 'Not provided'}\n"
    log_entry += f"Message: {message_body}\n"
    log_entry += "-" * 50 + "\n\n"
    
    try:
        with open('contact_logs.txt', 'a', encoding='utf-8') as f:
            f.write(log_entry)
        print(f"✅ Contact saved to log: {sender_name} <{sender_email}>")
    except Exception as e:
        print(f"❌ Error writing to contact log: {e}")
        raise

@app.route('/')
def accueil():
    """Page d'accueil"""
    recent_products = []
    for category in PRODUCTS_DATA.values():
        recent_products.extend(category[:2])
    
    return render_template('accueil.html', 
                         company=COMPANY_INFO,
                         recent_products=recent_products[:6])

@app.route('/about')
def about():
    """Redirige vers la section À propos sur la page d'accueil"""
    return redirect(url_for('accueil') + '#about')

@app.route('/produits')
def produits():
    """Page des produits"""
    all_products = {}
    for category, products in PRODUCTS_DATA.items():
        all_products[category] = products
    
    return render_template('produits.html', 
                         products=all_products,
                         company=COMPANY_INFO)

@app.route('/categorie/<category_name>')
def categorie_detail(category_name):
    """Page détaillée d'une catégorie de produits"""
    categories_data = {
        'carburant': {
            'title': 'Système de Carburant',
            'icon': 'fas fa-gas-pump',
            'description': 'Solutions complètes pour l\'alimentation et l\'injection de carburant',
            'products': [
                {'name': 'Coil Gp', 'description': 'Bobine d\'allumage haute performance', 'icon': 'fas fa-wrench'},
                {'name': 'Injecteur Standard', 'description': 'Injecteur haute performance pour moteurs industriels', 'icon': 'fas fa-syringe'},
                {'name': 'Nozzle Haute Pression', 'description': 'Buse d\'injection précise pour rendement optimal', 'icon': 'fas fa-spray-can'},
                {'name': 'Fuel Injection Pump', 'description': 'Pompe d\'injection haute pression pour moteurs diesel', 'icon': 'fas fa-cog'}
            ]
        },
        'electronique': {
            'title': 'Capteurs et Électronique Moteur',
            'icon': 'fas fa-microchip',
            'description': 'Systèmes de surveillance et de contrôle électronique de pointe',
            'products': [
                {'name': 'Capteur Température Eau', 'description': 'Surveillance précise de la température du liquide de refroidissement', 'icon': 'fas fa-thermometer-half'},
                {'name': 'Capteur Température Huile', 'description': 'Mesure de la température d\'huile moteur avec une précision exceptionnelle', 'icon': 'fas fa-temperature-high'},
                {'name': 'Capteur Pression Huile', 'description': 'Mesure précise de la pression d\'huile moteur', 'icon': 'fas fa-tachometer-alt'},
                {'name': 'Capteur Pression Carburant', 'description': 'Surveillance de la pression du système carburant', 'icon': 'fas fa-gauge'},
                {'name': 'Capteur Vitesse Camshaft', 'description': 'Détection précise de position arbre à cames', 'icon': 'fas fa-sync-alt'},
                {'name': 'Coil Gp Électronique', 'description': 'Bobine d\'allumage électronique avancée', 'icon': 'fas fa-bolt'}
            ]
        },
        'refroidissement': {
            'title': 'Système de Refroidissement',
            'icon': 'fas fa-snowflake',
            'description': 'Échangeurs thermiques et composants de refroidissement haute efficacité',
            'products': [
                {'name': 'Radiateur Eau', 'description': 'Échangeur thermique pour refroidissement moteur', 'icon': 'fas fa-car-battery'},
                {'name': 'Radiateur Huile', 'description': 'Refroidisseur d\'huile haute efficacité', 'icon': 'fas fa-oil-can'}
            ]
        },
        'turbo': {
            'title': 'Turbo et Système d\'Air',
            'icon': 'fas fa-fan',
            'description': 'Turbocompresseurs et composants de suralimentation de précision',
            'products': [
                {'name': 'Turbocharger', 'description': 'Turbocompresseur complet haute performance', 'icon': 'fas fa-wind'},
                {'name': 'Compressor Wheel', 'description': 'Roue de compresseur de précision', 'icon': 'fas fa-circle-notch'}
            ]
        },
        'composants': {
            'title': 'Composants Moteur & Pièces de Réparation',
            'icon': 'fas fa-cogs',
            'description': 'Pièces mécaniques essentielles et kits de maintenance complets',
            'products': [
                {'name': 'Shaft', 'description': 'Arbre de transmission haute résistance', 'icon': 'fas fa-arrow-right'},
                {'name': 'Valve Gp', 'description': 'Groupe valve pour système hydraulique', 'icon': 'fas fa-valve'},
                {'name': 'Core', 'description': 'Noyau d\'échangeur thermique', 'icon': 'fas fa-cube'},
                {'name': 'Kit de Réparation', 'description': 'Kit complet pour maintenance moteur', 'icon': 'fas fa-toolbox'}
            ]
        },
        'outils-sol': {
            'title': 'Outils d\'Attaque du Sol & Train de Roulement',
            'icon': 'fas fa-shovel',
            'description': 'Pièces d\'usure et composants de mobilité pour tous types d\'engins',
            'products': [
                {'name': 'Dents de Godet', 'description': 'Dents de godet haute résistance pour excavatrices et chargeuses', 'icon': 'fas fa-shovel'},
                {'name': 'Chaînes de Chenilles', 'description': 'Chaînes de chenilles renforcées pour engins lourds', 'icon': 'fas fa-circle-notch'},
                {'name': 'Galets de Roulement', 'description': 'Galets de roulement haute performance pour train de roulement', 'icon': 'fas fa-cog'},
                {'name': 'Lames de Bulldozer', 'description': 'Lames de bulldozer en acier trempé', 'icon': 'fas fa-tools'}
            ]
        },
        'filtres': {
            'title': 'Filtres',
            'icon': 'fas fa-filter',
            'description': 'Solutions de filtration premium pour tous types de fluides industriels',
            'products': [
                {'name': 'Filtres à Huile', 'description': 'Filtres à huile haute efficacité pour moteurs industriels', 'icon': 'fas fa-filter'},
                {'name': 'Filtres à Carburant', 'description': 'Filtres à carburant de précision pour injection diesel', 'icon': 'fas fa-tint'},
                {'name': 'Filtres à Air', 'description': 'Filtres à air haute performance pour moteurs turbo', 'icon': 'fas fa-wind'},
                {'name': 'Filtres Hydrauliques', 'description': 'Filtres hydrauliques pour systèmes haute pression', 'icon': 'fas fa-droplet'}
            ]
        },
        'hydraulique': {
            'title': 'Système Hydraulique',
            'icon': 'fas fa-water',
            'description': 'Composants hydrauliques haute performance pour engins de chantier',
            'products': [
                {'name': 'Pompes Hydrauliques', 'description': 'Pompes hydrauliques haute pression pour engins lourds', 'icon': 'fas fa-pump-medical'},
                {'name': 'Distributeurs Hydrauliques', 'description': 'Distributeurs hydrauliques de précision', 'icon': 'fas fa-valve'},
                {'name': 'Vérins Hydrauliques', 'description': 'Vérins hydrauliques haute résistance', 'icon': 'fas fa-arrows-alt'},
                {'name': 'Flexibles Hydrauliques', 'description': 'Flexibles hydrauliques haute pression', 'icon': 'fas fa-link'}
            ]
        },
        'electrique': {
            'title': 'Système Électrique',
            'icon': 'fas fa-bolt',
            'description': 'Composants électriques et électroniques pour engins industriels',
            'products': [
                {'name': 'Moteurs de Démarrage', 'description': 'Moteurs de démarrage haute performance pour engins lourds', 'icon': 'fas fa-car-battery'},
                {'name': 'Alternateurs', 'description': 'Alternateurs haute puissance pour systèmes électriques', 'icon': 'fas fa-charging-station'},
                {'name': 'Modules Électroniques', 'description': 'Modules électroniques de contrôle moteur', 'icon': 'fas fa-microchip'},
                {'name': 'Connecteurs Électriques', 'description': 'Connecteurs électriques étanches et robustes', 'icon': 'fas fa-plug'}
            ]
        },
        'joints': {
            'title': 'Pochette des Joints',
            'icon': 'fas fa-circle',
            'description': 'Joints toriques et joints d\'étanchéité de haute qualité',
            'products': [
                {'name': 'Joints Toriques', 'description': 'Joints toriques en caoutchouc haute performance', 'icon': 'fas fa-circle'},
                {'name': 'Joints d\'Étanchéité', 'description': 'Joints d\'étanchéité pour moteurs et transmissions', 'icon': 'fas fa-layer-group'},
                {'name': 'Kits de Joints', 'description': 'Kits complets de joints pour révisions moteur', 'icon': 'fas fa-box'},
                {'name': 'Joints Spéciaux', 'description': 'Joints spéciaux pour applications critiques', 'icon': 'fas fa-shield-alt'}
            ]
        },
        'silentblocs': {
            'title': 'Silentblocs',
            'icon': 'fas fa-shield-alt',
            'description': 'Amortisseurs et supports antivibratoires pour engins lourds',
            'products': [
                {'name': 'Silentblocs Moteur', 'description': 'Silentblocs antivibratoires pour moteurs', 'icon': 'fas fa-shield-alt'},
                {'name': 'Silentblocs Transmission', 'description': 'Silentblocs pour systèmes de transmission', 'icon': 'fas fa-cog'},
                {'name': 'Silentblocs Châssis', 'description': 'Silentblocs pour châssis et suspensions', 'icon': 'fas fa-tools'},
                {'name': 'Silentblocs Spéciaux', 'description': 'Silentblocs sur mesure pour applications spécifiques', 'icon': 'fas fa-layer-group'}
            ]
        },
        'transmission': {
            'title': 'Transmission et Freinage',
            'icon': 'fas fa-cogs',
            'description': 'Composants de transmission et systèmes de freinage haute performance',
            'products': [
                {'name': 'Embrayages', 'description': 'Embrayages haute performance pour engins lourds', 'icon': 'fas fa-cogs'},
                {'name': 'Pignons de Transmission', 'description': 'Pignons de transmission de précision', 'icon': 'fas fa-circle-notch'},
                {'name': 'Systèmes de Freinage', 'description': 'Systèmes de freinage haute performance', 'icon': 'fas fa-stop-circle'},
                {'name': 'Arbres de Transmission', 'description': 'Arbres de transmission haute résistance', 'icon': 'fas fa-link'}
            ]
        }
    }
    
    category_data = categories_data.get(category_name)
    
    if not category_data:
        return render_template('404.html'), 404
    
    return render_template('categorie.html', 
                         category=category_data,
                         category_name=category_name,
                         company=COMPANY_INFO)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Handle contact form submissions and save to contact_logs.txt"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()
        
        if not message or not (email or name):
            flash("Veuillez fournir au moins votre nom ou e-mail et un message.", 'error')
        else:
            try:
                save_contact_to_log(name, email, message)
                flash('Merci pour votre message. Nous avons bien reçu votre demande et vous répondrons rapidement.', 'success')
            except Exception as e:
                print(f"Erreur sauvegarde contact: {e}")
                flash("Une erreur est survenue lors de l'enregistrement de votre message. Veuillez réessayer.", 'error')
    
    return redirect(url_for('accueil') + '#contact')

@app.route('/api/products')
def api_products():
    """API simple pour récupérer les produits"""
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
            if 'brand' in product:
                brands.add(product['brand'])
    return {'brands': list(brands)}

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    try:
        return render_template('500.html'), 500
    except Exception:
        return ("<h1 style='font-family:Arial;'>Erreur serveur (500)</h1>"
                "<p>Un problème est survenu. Veuillez réessayer plus tard.</p>"), 500

@app.template_filter('capitalize_first')
def capitalize_first_filter(text):
    return text.capitalize() if text else ''

@app.template_filter('format_brand')
def format_brand_filter(brand):
    brand_names = {
        'caterpillar': 'Caterpillar',
        'doosan': 'Doosan',
        'volvo': 'Volvo'
    }
    return brand_names.get(brand.lower(), brand)

@app.context_processor
def inject_globals():
    lang = request.args.get('lang', 'fr').lower()
    if lang not in ('fr', 'en'):
        lang = 'fr'

    nav_labels = {
        'fr': {
            'home': 'Accueil',
            'about': 'À Propos',
            'catalogue': 'Catalogue',
            'contact': 'Contact',
            'fr': 'FR', 'en': 'EN',
        },
        'en': {
            'home': 'Home',
            'about': 'About',
            'catalogue': 'Catalogue',
            'contact': 'Contact',
            'fr': 'FR', 'en': 'EN',
        }
    }[lang]

    typing_phrases = {
        'fr': [
            "Équipements Industriels Premium",
            "Pièces Détachées d'Origine",
            "Solutions Pour Travaux Publics",
        ],
        'en': [
            "Premium Industrial Equipment",
            "Genuine Spare Parts",
            "Solutions for Public Works",
        ]
    }[lang]

    def url_for_lang(endpoint, **kwargs):
        kwargs.setdefault('lang', lang)
        return url_for(endpoint, **kwargs)

    def canonical_url():
        return request.base_url

    return {
        'current_year': datetime.now().year,
        'company_name': COMPANY_INFO['name'],
        'company_email': COMPANY_INFO['email'],
        'company_phone': COMPANY_INFO['phone'],
        'whatsapp_link': f"https://wa.me/{COMPANY_INFO['whatsapp'].replace('+', '').replace(' ', '')}",
        'lang': lang,
        'nav_labels': nav_labels,
        'typing_phrases': typing_phrases,
        'url_for_lang': url_for_lang,
        'canonical_url': canonical_url,
    }

@app.route('/robots.txt')
def robots_txt():
    lines = [
        "User-agent: *",
        "Allow: /",
        "Sitemap: " + url_for('sitemap_xml', _external=True),
    ]
    return ("\n".join(lines), 200, {"Content-Type": "text/plain; charset=utf-8"})

@app.route('/sitemap.xml')
def sitemap_xml():
    pages = [
        url_for('accueil', _external=True),
        url_for('produits', _external=True),
    ]
    categories = ['carburant','electronique','refroidissement','turbo','composants','outils-sol','filtres','hydraulique','electrique','joints','silentblocs','transmission']
    for key in categories:
        pages.append(url_for('categorie_detail', category_name=key, _external=True))

    xml_items = []
    for url in pages:
        xml_items.append(f"<url><loc>{url}</loc></url>")
    xml = "<?xml version='1.0' encoding='UTF-8'?>" \
          "<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>" + "".join(xml_items) + "</urlset>"
    return (xml, 200, {"Content-Type": "application/xml; charset=utf-8"})

if __name__ == '__main__':
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    if not os.path.exists('static'):
        os.makedirs('static')
        os.makedirs('static/css')
        os.makedirs('static/js')
        os.makedirs('static/images')
    
    print("🚀 Démarrage de l'application Fiklar...")
    print("📍 Accès: http://localhost:5000")
    print("📝 Contact forms will be saved to: contact_logs.txt")

    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5000)