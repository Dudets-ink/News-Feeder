from flask import render_template, flash, redirect, request, \
    current_app, url_for
from flask_login import current_user

from central import db
from central.main import bp
from central.main.forms import CommentForm
from central.models import Comment
import requests


@bp.route('/')
def index():
    """Renders main page with 3 categories on it

    Returns:
        Html main page
    """
    
    categories = ['War', 'Economics', 'Healthcare']
    
    return render_template('index.html', categories=categories)

@bp.route('/<category>')
def category(category):
    """Renders page with articles on given category.
    News are taken from aggregator API

    Args:
        category (str): news category

    Returns:
        Html page with news for the selected category
    """
    
    # news aggregator API
    url = 'https://newsapi.org/v2/everything'
    API_KEY = '2140e1718dec417f9312363003c63bd0'
    
    cat = category
    language = 'en'
    sort_by = 'popularity'
    params = dict(q=cat, apiKey=API_KEY, language=language, 
                  sort_by=sort_by)
    news = requests.get(url, params=params)
    json = news.json()
    
    # pagination
    if json['status']:
        page = request.args.get('page', 1, type=int)
        articles = json['articles']
        posts = current_app.config['POSTS_PER_PAGE']
        next_url = url_for('main.category', category=cat, page=page+1) \
            if len(articles) > posts * page else False
        prev_url = url_for('main.category', category=cat, page=page-1) \
            if page != 1 else False
        min_posts = posts * (page - 1) if page != 1 else 0
        max_posts = posts * page
        
        return render_template(
            'category.html', title=category, articles=articles, next_url=next_url, \
            prev_url=prev_url, max_posts=max_posts, min_posts=min_posts
            )
    else:
        flash('Error encountered...', 'error')
        return redirect('main.index')
    
@bp.route('/<category>/<article>', methods=['GET', 'POST'])
def comments(category, article):
    """Renders page with comments to article, 
    Handles such methods:
    GET - on getting page,
    POST - adds new comment to DB 

    Args:
        category (str): news category
        article (str): category article

    Returns:
        Html page with comments to given article
    """
    
    form = CommentForm()
    comments = Comment.query.filter_by(on_article=article).all()
    if form.validate_on_submit():
        comment = Comment(text=form.text.data, on_article=article,
                          owner_id=current_user.id, owner=current_user)
        db.session.add(comment)
        db.session.commit()    
        return redirect(url_for('main.comments', category=category, article=article))
    
    return render_template('comments.html', title=article, \
                            comments=comments, form=form)