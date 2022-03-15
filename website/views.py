# from unicodedata import category
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import User, Set, Flashcard
from . import db

views = Blueprint("views", __name__)

@views.route("/home")
@views.route("/")
@login_required
def home():
    return render_template("home.html")


@views.route("/sets", methods=['GET', 'POST'])
@login_required
def sets():
    user = User.query.filter_by(id=current_user.id).first()
    seth = user.sets

    if request.method == 'POST':
        set_name = request.form.get('setname')

        if not set_name:
            flash("Can't be empty", category="error")
        else:
            new_set = Set(name=set_name, user=current_user)
            db.session.add(new_set)
            db.session.commit()
            flash("Set added!", category="success")
            return redirect(url_for("views.sets"))

    return render_template("sets.html", seth=seth)



@views.route("/flashcards/<setid>", methods=['GET', 'POST'])
@login_required
def flashcards(setid):
    flashc = Flashcard.query.filter_by(of_set=setid).all()
    seth = Set.query.filter_by(id=setid).all()

    if request.method == 'POST':
        firstside = request.form.get('firstside')
        secondside = request.form.get('secondside')

        if not firstside:
            flash("Can't be empty fir", category="error")
        elif not secondside:
            flash("Can't be empty sec", category="error")
        else:
            new_flashcard = Flashcard(firstside=firstside, secondside=secondside, of_set=setid)
            db.session.add(new_flashcard)
            db.session.commit()
            flash("Flashcard added!", category="success")
            return redirect(url_for("views.flashcards", setid=setid))

        
    return render_template("flashcards.html", flashc=flashc, seth=seth)



@views.route("/delete-flashcard/<id>")
@login_required
def delete_flashcard(id):
    flashcard = Flashcard.query.filter_by(id=id).first()
    db.session.delete(flashcard)
    db.session.commit()
    flash("Flashcard deleted", category='success')
    return redirect(url_for("views.flashcards", setid=flashcard.of_set))



@views.route("/delete-set/<id>")
@login_required
def delete_set(id):
    seth = Set.query.filter_by(id=id).first()

    db.session.delete(seth)
    db.session.commit()
    flash("Set deleted", category='success')
    return redirect(url_for("views.sets"))


@views.route("/account/")
@login_required
def account():
    user = User.query.filter_by(id=current_user.id).first()
    return render_template("account.html", user=user)


@views.route("/test")
@login_required
def test():

    return render_template("test.html")


@views.route("/change-set-name/<id>", methods=['GET', 'POST'])
@login_required
def change_set_name(id):
    seth = Set.query.filter_by(id=id).first()

    if not seth:
        flash("No set found", category='error')
    else:
        seth.name = request.form.get('updatesetname')
        db.session.commit()
        flash("Set name updated", category='success')
    
    
    return redirect(url_for("views.sets"))


@views.route("/change-flashcard-content/<id>", methods=['GET', 'POST'])
@login_required
def change_flashcard_content(id):
    flashc = Flashcard.query.filter_by(id=id).first()

    if not flashc:
        flash("No set found", category='error')
    else:
        flashc.firstside = request.form.get('updatedfirstside')
        flashc.secondside = request.form.get('updatedsecondside')
        db.session.commit()
        flash("Flashcard updated", category='success')
        return redirect(url_for("views.flashcards", setid=flashc.of_set))
    
    return redirect(url_for("views.sets"))

