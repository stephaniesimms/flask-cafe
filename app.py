"""Flask App for Flask Cafe."""

from flask import Flask, render_template, flash, jsonify, request
from flask import redirect, session, g

from models import db, connect_db, Cafe, City, User, Like

from forms import CafeAddEditForm
from forms import SignupForm, LoginForm, EditUserForm

from sqlalchemy.exc import IntegrityError

from secrets import FLASK_SECRET_KEY

from config import DATABASE_URL

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SECRET_KEY'] = FLASK_SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


@app.errorhandler(404)
def page_not_found(e):
    """Return 404 page."""

    return render_template('404.html'), 404

#######################################
# auth & auth routes


CURR_USER_KEY = "curr_user"
NOT_LOGGED_IN_MSG = "You are not logged in."


@app.before_request
def add_user_to_g():
    """If logged in, add curr user to Flask global."""
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
    """Display signup form and handle request to register new user.
    Redirect to cafes list.

    If there is already a user with that username:
    flash message and display form again.
    """

    form = SignupForm()

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
                username=username,
                first_name=first_name,
                last_name=last_name,
                description=description,
                email=email,
                password=password,
                image_url=image_url
            )

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
    """Produce login form or handle login.
    Redirects to cafes list on successful login.
    """
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user_authenticated = User.authenticate(
            username=username,
            password=password
        )

        if user_authenticated:
            do_login(user_authenticated)
            flash(f"Hello, {username}", "success")
            return redirect("/cafes")

        else:
            form.username.errors = ["Invalid credentials"]

    return render_template("auth/login-form.html", form=form)


@app.route("/logout", methods=["POST", "GET"])
def logout():
    """Handle user logout. Redirects to homepage."""

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
        can_add=g.user and g.user.admin
    )


@app.route('/cafes/<int:cafe_id>')
def cafe_detail(cafe_id):
    """Show detail for cafe."""

    cafe = Cafe.query.get_or_404(cafe_id)

    if g.user:
        liked = g.user in cafe.liking_users
    else:
        liked = None

    return render_template(
        'cafe/detail.html',
        cafe=cafe,
        show_edit=g.user and g.user.admin,
        liked=liked
    )


@app.route('/cafes/add', methods=["GET", "POST"])
def add_cafe():
    """Handle add_cafe form.
    Only logged-in admin users can add/edit cafes."""

    if not g.user or not g.user.admin:
        flash("Only admins can add cafes.", "danger")
        return redirect("/login")

    form = CafeAddEditForm()

    form.city_code.choices = City.get_city_codes()

    if form.validate_on_submit():
        cafe = Cafe(
            name=form.name.data,
            description=form.description.data,
            url=form.url.data,
            address=form.address.data,
            city_code=form.city_code.data,
            image_url=form.image_url.data or None,
        )

        db.session.add(cafe)

        # In order to run save_map, we need to make sure the cafe has been
        # given an ID, so we need the database to "flush" --- this runs the
        # SQL [so postgres gives it an id] but doesn't commit the transaction
        db.session.flush()
        cafe.save_map()

        db.session.commit()

        flash(f"{cafe.name} added!", "success")
        return redirect(f"/cafes/{cafe.id}")

    else:
        return render_template("cafe/add-form.html", form=form)


@app.route('/cafes/<int:cafe_id>/edit', methods=["GET", "POST"])
def edit_cafe(cafe_id):
    """Handle edit cafe form.
    Only logged-in admin users can add/edit cafes."""

    if not g.user or not g.user.admin:
        flash("Only admins can edit cafes.", "danger")
        return redirect("/login")

    cafe = Cafe.query.get_or_404(cafe_id)

    # Do not display the static value of the default image
    # This will throw an error with the URL validator in wtforms
    if cafe.image_url == Cafe._default_img:
        cafe.image_url = ''

    form = CafeAddEditForm(obj=cafe)
    form.city_code.choices = City.get_city_codes()

    if form.validate_on_submit():
        need_new_map = (
                cafe.address != form.address.data or
                cafe.city_code != form.city_code.data
        )

        cafe.name = form.name.data
        cafe.description = form.description.data
        cafe.url = form.url.data
        cafe.address = form.address.data
        cafe.city_code = form.city_code.data
        cafe.image_url = form.image_url.data or None

        if need_new_map:
            cafe.save_map()

        # if the image_url is empty, then set the default again
        if not cafe.image_url:
            cafe.image_url = Cafe._default_img

        db.session.commit()
        flash(f"{cafe.name} edited", "success")
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

    # Do not display the static value of the default image
    # This will throw an error with the URL validator in wtforms
    if user.image_url == User._default_img:
        user.image_url = ''

    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        form.populate_obj(user)

        # if the image_url is empty, then set the default again
        if not user.image_url:
            user.image_url = User._default_img

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
    likes = like is not None

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


if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=False, passthrough_errors=True)
