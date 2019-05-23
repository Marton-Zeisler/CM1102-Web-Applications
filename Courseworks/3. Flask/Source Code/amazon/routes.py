from flask import render_template, url_for, flash, redirect, request
from amazon.forms import RegistrationForm, LoginForm, AddCommentForm
from amazon import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from amazon.models import User, Product, Comment, Wishlist, Basket, BasketObject, Order, OrderProduct
from datetime import datetime

@app.route("/")
@app.route("/home/<string:query>")
def home(query=""):
    products = []
    if query == "name-ascending":
        products = Product.query.order_by(Product.title).all()
    elif query == "name-descending":
        products = Product.query.order_by(Product.title.desc())
    elif query == "price-ascending":
        products = Product.query.order_by(Product.price).all()
    elif query == "price-descending":
        products = Product.query.order_by(Product.price.desc())
    elif query == "year-ascending":
        products = Product.query.order_by(Product.year).all()
    elif query == "year-descending":
        products = Product.query.order_by(Product.year.desc())
    else:
        products = Product.query.all()

    if request.args.get("addBasket") != None and current_user.is_authenticated:
        productID = request.args.get("addBasket")
        product = Product.query.get(productID)
        basket = Basket.query.filter_by(user_id=current_user.id, product_id=productID).first()
        if basket != None:
            basket.quantity += 1
            basket.priceTotal += product.price
            db.session.commit()
        else:
            basket = Basket(user_id=current_user.id, product_id=productID, quantity=1, priceTotal=product.price)
            db.session.add(basket)
            db.session.commit()
        
        flash("You have successfully added a new product to your basket!", "success")


    wishProductIDs = []
    if current_user.is_authenticated:
        userWishes = Wishlist.query.filter_by(user_id=current_user.id)
        for each in userWishes:
            wishProductIDs.append(each.product_id)  
        
    return render_template("home.html", products=products, wishProductIDs=wishProductIDs)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get("next")
                flash(f"You have successfully signed in!", "success")
                return redirect(next_page) if next_page else redirect(url_for("home"))
            else:
                flash("Login failed! Please check your username and password!", "danger")
    return render_template("login.html", title="Login", form=form)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"You have successfully signed up!", "success")
        return redirect(url_for("login"))
    return render_template("signup.html", title="Sign Up", form=form)

@app.route("/signout")
def signout():
    logout_user()
    flash(f"You have successfully signed out!", "success")
    return redirect(url_for("home"))

@app.route("/product/<int:product_id>", methods=["GET", "POST"])
def product(product_id):
    product = Product.query.get_or_404(product_id)
    comments = Comment.query.filter_by(product_id=product_id).order_by(Comment.id.desc())
                
    form = AddCommentForm()
    if form.validate_on_submit():
        comment = Comment(title=form.title.data, comment=form.comment.data, product_id=product.id)
        db.session.add(comment)
        db.session.commit()
        flash("Your comment has been submitted!", "success")
        form.title.data = ""
        form.comment.data = ""

    wishProductIDs = []

    if current_user.is_authenticated:
        userWishes = Wishlist.query.filter_by(user_id=current_user.id)
        for each in userWishes:
            wishProductIDs.append(each.product_id)
    
    return render_template("product.html", title="Product", product=product, comments=comments, form=form, productInWishList=product.id in wishProductIDs)

@app.route("/wishlist")
@app.route("/wishlist/<int:addID>")
def wishlist(addID=0):
    if current_user.is_authenticated:
        if addID > 0:
            newWish = Wishlist(user_id=current_user.id, product_id=addID)
            db.session.add(newWish)
            db.session.commit()
            flash(f"You successfully added a new product to your wishlist!", "success")

        if request.args.get("delete") != None:
            print("deleteing???")
            deleteID = request.args.get("delete")
            print(deleteID)
            Wishlist.query.filter_by(user_id=current_user.id, product_id=deleteID).delete()
            db.session.commit()
            flash(f"You successfully removed a  product from your wishlist!", "success")

        if request.args.get("deleteAll") != None:
            Wishlist.query.filter_by(user_id=current_user.id).delete()
            db.session.commit()
            flash("You have successfuly removed all of your products from your wish list!", "success")

        userWishes = Wishlist.query.filter_by(user_id=current_user.id)
        productIDs = []
        for each in userWishes:
            productIDs.append(each.product_id)
        products = Product.query.filter(Product.id.in_(productIDs))    
        return render_template("wishlist.html", title="Wish List", products = products)
        
    flash(f"You must be logged in to view this page!", "danger")
    return redirect(url_for("home"))
    
    

@app.route("/basket")
def basket():
    if current_user.is_authenticated:

        if request.args.get("deleteAll") != None:
            Basket.query.filter_by(user_id=current_user.id).delete()
            db.session.commit()
            flash("You have successfully removed all of your products from your basket!", "success")
            
        if request.args.get("add") != None:
            basketID = request.args.get("add")
            basket = Basket.query.get(basketID)
            basket.priceTotal += (basket.priceTotal / basket.quantity)
            basket.quantity += 1
            db.session.commit()
            flash("You have successfully increased the quantity!", "success")

        if request.args.get("subtract") != None:
            basketID = request.args.get("subtract")
            basket = Basket.query.get(basketID)
            if basket.quantity == 1:
                Basket.query.filter_by(id=basketID).delete()
            else:
                basket.priceTotal -= (basket.priceTotal / basket.quantity)
                basket.quantity -= 1

            db.session.commit()
            flash("You have successfully decreased the quantity!", "success")

        if request.args.get("delete") != None:
            basketID = request.args.get("delete")
            Basket.query.filter_by(id=basketID).delete()
            db.session.commit()
            flash("You have successfully removed a product from your basket!", "success")

        userBaskets = Basket.query.filter_by(user_id=current_user.id)
        userBasketObjects = []
        totalPrice = 0
        totalProducts = 0
        for basket in userBaskets:
            product = Product.query.get(basket.product_id)
            basketObject = BasketObject(product, basket)
            userBasketObjects.append(basketObject)
            totalPrice += basket.priceTotal
            totalProducts += basket.quantity
        
        return render_template("basket.html", title="Wish List", userBasketObjects=userBasketObjects, totalPrice=totalPrice, totalProducts=totalProducts)
    
    flash(f"You must be logged in to view this page!", "danger")
    return redirect(url_for("home"))

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if current_user.is_authenticated:
        if request.method == "POST":
            baskets = Basket.query.filter_by(user_id=current_user.id)
            orderSumPrice = 0
            for eachBasket in baskets:
                orderSumPrice += eachBasket.priceTotal
            
            order = Order(user_id=current_user.id, date=datetime.utcnow(), priceTotal=orderSumPrice)
            db.session.add(order)
            db.session.commit()
            
            for eachBasket in baskets:
                product = Product.query.get(eachBasket.product_id)
                orderProduct = OrderProduct(order_id=order.id, quantity=eachBasket.quantity, product_title=product.title, priceTotal=eachBasket.priceTotal)
                db.session.add(orderProduct)
            
            baskets.delete()
            db.session.commit()
            flash(f"You successfully placed an order!", "success")
            return redirect(url_for("orders"))
        else:
            if request.args.get("ready") != None and request.args.get("totalPrice") != None:
                totalPrice = request.args.get("totalPrice")
                return render_template("checkout.html", title="Checkout", totalPrice=totalPrice)
            else:
                flash(f"Please review your order first!", "danger")
                return redirect(url_for("basket"))
    
    flash(f"You must be logged in to view this page!", "danger")
    return redirect(url_for("home"))

@app.route("/orders")
def orders():
    if current_user.is_authenticated:
        ordersAndProducts = {}
        orders = Order.query.filter_by(user_id=current_user.id)
        for eachOrder in orders:
            products = OrderProduct.query.filter_by(order_id=eachOrder.id)
            ordersAndProducts[eachOrder] = products

        return render_template("orders.html", title="Orders", ordersAndProducts=ordersAndProducts)

    flash(f"You must be logged in to view this page!", "danger")
    return redirect(url_for("home"))