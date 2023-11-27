from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from sqlalchemy.sql import func
from flask_cors import CORS
from datetime import datetime
import logging

app = Flask(__name__)

CORS(app)


app.logger.error('MESSAGE DE CONNEXION')

# Configuration de la base de données MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin@database_server:3306/part1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Définition du modèle Parking
class Parking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plaque = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    app.logger.error('MODULE BIEN CREER')


@app.route('/')
def hello_world():
    return render_template('index.html')

# Route pour l'ajout d'une plaque
@app.route('/plaque', methods=['POST'])
def ajout_plaque():
    data = request.get_json()
    nouvelle_plaque = Parking(plaque=data['plaque'])
    db.session.add(nouvelle_plaque)
    db.session.commit()
    return jsonify(message='Plaque ajoutée avec succès!')

@app.route('/liste', methods=['GET'])
def liste_plaques():
    app.logger.error('ENTRE DANS LA ROUTE')
    plaques = Parking.query.order_by(desc(Parking.date)).all()
    result = [{'id': plaque.id, 'plaque': plaque.plaque, 'date': plaque.date.strftime("%Y-%m-%d %H:%M:%S")} for plaque in plaques]
    app.logger.error('REPONSE BIEN EMISE')
    return jsonify(result)
# Route pour la récupération de la liste des plaques par groupe
@app.route('/liste_groupe', methods=['GET'])
def liste_groupe():
    liste = db.session.query(
        func.DATE_FORMAT(Parking.date, '%d-%m-%Y').label('date_fr'),
        func.DATE_FORMAT(Parking.date, '%H').label('heure'),
        func.count().label('nombre_vehicules')
    ).group_by(
        func.DATE_FORMAT(Parking.date, '%Y-%m-%d'),
        func.DATE_FORMAT(Parking.date, '%d-%m-%Y'),
        func.DATE_FORMAT(Parking.date, '%H')
    ).order_by(
        func.DATE_FORMAT(Parking.date, '%Y-%m-%d'),
        func.DATE_FORMAT(Parking.date, '%H')
    ).all()

    result = [{'date_fr': groupe.date_fr, 'heure': groupe.heure, 'nombre_vehicules': groupe.nombre_vehicules} for groupe in liste]
    return jsonify(result)

# Route pour les détails à une heure spécifique
@app.route('/details', methods=['GET'])
def details():
    date = request.args.get('date')
    heure = int(request.args.get('heure'))
    heure_fin = heure + 1

    details = Parking.query.filter(
        Parking.date >= f"{date} {heure:02}:00:00",
        Parking.date < f"{date} {heure_fin:02}:00:00"
    ).all()

    result = [{'id': detail.id, 'plaque': detail.plaque, 'date': detail.date.strftime("%Y-%m-%d %H:%M:%S")} for detail in details]
    return jsonify(result)



  # Route pour la recherche
@app.route('/recherche', methods=['GET'])
def recherche():
    date_debut = request.args.get('date_heure_debut')
    date_fin = request.args.get('date_heure_fin')
    plaque = request.args.get('plaque')

    # Vérification des dates
    pres = ""
    if date_debut and date_fin:
        pres = "1"

    # Vérification de la date de début inférieure à la date de fin
    if pres and date_debut > date_fin:
        return jsonify(message="La date de début ne doit pas être supérieure à la date de fin"), 400

    # Construction de la requête SQL
    req = Parking.query

    if date_debut and not date_fin:
        req = req.filter(Parking.date >= date_debut)
    elif date_fin and not date_debut:
        req = req.filter(Parking.date <= date_fin)
    elif pres:
        req = req.filter(Parking.date >= date_debut, Parking.date <= date_fin)

    if plaque:
        req = req.filter(Parking.plaque == plaque)

    result = req.order_by(Parking.date).all()
    result = [{'id': res.id, 'plaque': res.plaque, 'date': res.date.strftime("%Y-%m-%d %H:%M:%S")} for res in result]

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')