"""Flask App for Flask Cafe."""

from flask import Flask, render_template, flash, jsonify, request
from flask import redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Cafe, City, User, Like

from forms import AddCafeForm, EditCafeForm, SignupForm, LoginForm, EditUserForm

from sqlalchemy.exc import IntegrityError

from secrets import FLASK_SECRET_KEY


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///flaskcafe'
app.config['SECRET_KEY'] = FLASK_SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

toolbar = DebugToolbarExtension(app)

connect_db(app)


#######################################
# auth & auth routes


CURR_USER_KEY = "curr_user"
NOT_LOGGED_IN_MSG = "You are not logged in."


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Produce signup form and handle request to register new user"""

    form = SignupForm()

    # catch error to check for unique username before submitting form
    if form.validate_on_submit():
        try:
            username = form.username.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            description = form.description.data
            email = form.email.data
            password = form.password.data
            image_url = form.image_url.data

            if not image_url:
                image_url = None

            user = User.register(
                username=username, first_name=first_name,
                last_name=last_name, description=description,
                email=email, password=password, image_url=image_url)

            db.session.add(user)
            db.session.commit()
            do_login(user)
            flash("You are signed up and logged in.", "success")

        except IntegrityError:
            flash("That username is taken. Try again.", "danger")
            return render_template("auth/signup-form.html", form=form)

        return redirect("/cafes")

    else:
        return render_template("auth/signup-form.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Produce login form or handle login"""
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user_authenticated = User.authenticate(
            username=username, password=password)

        if user_authenticated:
            do_login(user_authenticated)
            flash(f"Hello, {username}", "success")
            return redirect("/cafes")

        else:
            form.username.errors = ["Invalid credentials"]

    return render_template("auth/login-form.html", form=form)


@app.route("/logout", methods=["POST", "GET"])
def logout():
    do_logout()
    flash("successfully logged out", "success")
    return redirect("/")


#######################################
# homepage

@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")


#######################################
# cafes

@app.route('/cafes')
def cafe_list():
    """Return list of all cafes."""

    cafes = Cafe.query.order_by('name').all()

    return render_template(
        'cafe/list.html',
        cafes=cafes,
    )


@app.route('/cafes/<int:cafe_id>')
def cafe_detail(cafe_id):
    """Show detail for cafe."""

    cafe = Cafe.query.get_or_404(cafe_id)

    return render_template(
        'cafe/detail.html',
        cafe=cafe,
    )


@app.route('/cafes/add', methods=["GET", "POST"])
def add_cafe():
    """Handle add_cafe form. Only logged-in users can add/edit cafes."""
    
    if not g.user:
        flash("Only logged-in users can add cafes.", "danger")
        return redirect("/login")
    
    form = AddCafeForm()

    form.city_code.choices = City.get_city_codes()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        url = form.url.data
        address = form.address.data
        city_code = form.city_code.data
        image_url = form.image_url.data

        if not image_url:
            image_url = None

        cafe = Cafe(name=name, 
                    description=description, 
                    url=url, 
                    address=address, 
                    city_code=city_code,
                    image_url=image_url)

        flash(f"{name} added!", "success")
        db.session.add(cafe)
        db.session.commit()

        return redirect(f"/cafes/{cafe.id}")
    
    else:
        return render_template("cafe/add-form.html", form=form)


@app.route('/cafes/<int:cafe_id>/edit', methods=["GET", "POST"])
def edit_cafe(cafe_id):
    """Handle edit cafe form. Only logged-in users can add/edit cafes."""

    if not g.user:
        flash("Only logged-in users can add cafes.", "danger")
        return redirect("/login")
    
    cafe = Cafe.query.get_or_404(cafe_id)
    
    form = EditCafeForm(obj=cafe)
    form.city_code.choices = City.get_city_codes()

    if form.validate_on_submit():
        form.populate_obj(cafe)

        if not cafe.image_url:
            cafe.image_url = None

        flash(f"{cafe.name} edited", "success")
        db.session.commit()

        return redirect(f"/cafes/{cafe.id}")

    else:
        return render_template("cafe/edit-form.html", form=form, cafe=cafe)


#######################################
# display and edit user profiles

@app.route('/profile')
def display_profile():
    """Displays profile if user is logged in"""

    if not g.user:
        flash(NOT_LOGGED_IN_MSG, "danger")
        return redirect("/login")

    return render_template("profile/detail.html", user=g.user)


@app.route('/profile/edit', methods=["GET", "POST"])
def edit_user():
    """Edit profile for user."""

    if not g.user:
        flash(NOT_LOGGED_IN_MSG, "danger")
        return redirect("/login")

    user = g.user

    form = EditUserForm(obj=g.user)

    if form.validate_on_submit():
        form.populate_obj(user)

        db.session.commit()

        flash("Profile edited.", "success")
        return redirect("/profile")

    else:
        return render_template("profile/edit-form.html", form=form)

#######################################
# API for likes


@app.route("/api/likes")
def likes_cafe():
    """Does user like a cafe?"""

    if not g.user:
        return jsonify({"error": "Not logged in"})

    cafe_id = int(request.args['cafe_id'])
    cafe = Cafe.query.get_or_404(cafe_id)

    like = Like.query.filter_by(user_id=g.user.id, cafe_id=cafe.id).first()
    # likes = like is not None
    if like is not None:
        likes = True
    else:
        likes = False

    return jsonify({"likes": likes})


@app.route("/api/like", methods=["POST"])
def like_cafe():
    """Like a cafe"""

    if not g.user:
        return jsonify({"error": "Not logged in"})

    cafe_id = int(request.json['cafe_id'])
    cafe = Cafe.query.get_or_404(cafe_id)

    g.user.liked_cafes.append(cafe)
    db.session.commit()

    response = {"liked": cafe.id}
    return jsonify(response)


@app.route("/api/unlike", methods=["POST"])
def unlike_cafe():
    """Unlike a cafe"""

    if not g.user:
        return jsonify({"error": "Not logged in"})

    cafe_id = int(request.json['cafe_id'])
    cafe = Cafe.query.get_or_404(cafe_id)

    Like.query.filter_by(cafe_id=cafe_id, user_id=g.user.id).delete()
    db.session.commit()

    response = {"unliked": cafe.id}
    return jsonify(response)
