# from unicodedata import category
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import User, Set, Flashcard
from . import db
from sqlalchemy import desc

views = Blueprint("views", __name__)

@views.route("/study/<id>")
@login_required
def study(id):
    seth = Set.query.filter_by(id=id).first()
    flashc = Flashcard.query.filter_by(of_set=id).all()

    return render_template("study.html", seth = seth, flashc = flashc)


@views.route("/sets", methods=['GET', 'POST'])
@views.route("/")
@login_required
def sets():
    seth = Set.query.filter_by(author=current_user.id).order_by(desc(Set.date_created)).all()

    if request.method == 'POST':
        set_name = request.form.get('setname')

        if not set_name:
            flash("Can't be empty", category="danger")
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
    flashc = Flashcard.query.filter_by(of_set=setid).order_by(desc(Flashcard.date_created)).all()
    seth = Set.query.filter_by(id=setid).all()

    if request.method == 'POST':
        firstside = request.form.get('firstside')
        secondside = request.form.get('secondside')

        if not firstside:
            flash("Can't be empty fir", category="danger")
        elif not secondside:
            flash("Can't be empty sec", category="danger")
        else:
            new_flashcard = Flashcard(firstside=firstside, secondside=secondside, of_set=setid)
            db.session.add(new_flashcard)
            db.session.commit()
            flash("Flashcard added!", category="success")
            return redirect(url_for("views.flashcards", setid=setid))

        
    return render_template("flashcards.html", flashc=flashc, seth=seth)



@views.route("/delete-flashcard/<id>", methods=['GET', 'POST'])
@login_required
def delete_flashcard(id):
    flashcard = Flashcard.query.filter_by(id=id).first()
    db.session.delete(flashcard)
    db.session.commit()
    flash("Flashcard deleted", category='info')
    return redirect(url_for("views.flashcards", setid=flashcard.of_set))



@views.route("/delete-set/<id>", methods=['GET', 'POST'])
@login_required
def delete_set(id):
    seth = Set.query.filter_by(id=id).first()

    db.session.delete(seth)
    db.session.commit()
    flash("Set deleted", category='info')
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
        flash("No set found", category='danger')
    else:
        seth.name = request.form.get('updatesetname')
        db.session.commit()
        flash("Set name updated", category='info')
    
    
    return redirect(url_for("views.sets"))


@views.route("/change-flashcard-content/<id>", methods=['GET', 'POST'])
@login_required
def change_flashcard_content(id):
    flashc = Flashcard.query.filter_by(id=id).first()

    if not flashc:
        flash("No set found", category='danger')
    else:
        first = request.form.get('updatedfirstside')
        second = request.form.get('updatedsecondside')
        if first and second:
            flashc.firstside = first
            flashc.secondside = second
            flash("Whole flashcard updated", category='success')
        elif second:
            flashc.secondside = second
            flash("Updated second side of a flashcard", category='success')
        elif first:
            flashc.firstside = first
            flash("Updated first side of a flashcard", category='success')
        else:
            flash("Nothing updated", category='danger')
        db.session.commit()
        return redirect(url_for("views.flashcards", setid=flashc.of_set))
    
    return redirect(url_for("views.sets"))




# @views.route("/deletemultiple", methods=['GET', 'POST'])
# @login_required
# def deletemultiple():
#     if request.method == 'POST':
#         for fla in request.form.getlist('mycheckbox'):
#             print(fla)
#             seth = Set.query.filter_by(id=id).first()

#         db.session.delete(seth)
#         db.session.commit()
#         flash("Set deleted", category='success')
#     return redirect(url_for("views.sets"))


