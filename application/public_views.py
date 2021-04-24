from flask import Blueprint, request, redirect, make_response, jsonify
from flask_jwt_extended import create_access_token, set_access_cookies
from werkzeug.security import check_password_hash
from application.models.user_table import User
from application.models.blog_table import Blog
from application.models.tag_table import Tag
from application.models.tag_blog_relationship_table import tag_blog
from .extensions import db

public_views = Blueprint("public_views", __name__)

@public_views.route('/single_blog/<int:id>', methods=["GET"])
def get_single_blog(id):
    # The blog record is retrieved from the database according to it's id.
    blog = Blog.query.filter_by(id=id).first_or_404()

    # The blog record is serialized, to include its relevant info.
    serialized_blog = (blog.serialize)

    # A tags field is added to the post in the form of a list.
    # This list will hold the tag information for the sake of display.
    serialized_blog["tags"] = []

    # The tag info for each tag associated with the blog entry is added to the list.
    for tag in blog.tags:
        serialized_blog["tags"].append(tag.serialize)

    # The serialized blog is added to a list for the sake of matching all the other response formats.
    # To include [] brackets.
    serialized_data = []
    serialized_data.append(serialized_blog)

    return jsonify(serialized_data)

@public_views.route('/all_blog_entries', methods=['GET'])
def get_all_blog_entries():
    # All blog entries are queried
    blog_entries = Blog.query.order_by(Blog.created_at).all()
    serialized_data = []

    # All the blogs are individually serialized and added to a list of serialized data
    for blog in blog_entries:
        serialized_data.append(blog.serialize)

    # Each item in the list of serialized data is given a tags field
    for item in serialized_data:
        item['tags'] = []

    # The information for each tag is added to it's corresponding blog entry
    i = 0
    for blog in blog_entries:
        for tag in blog.tags:
            serialized_data[i]['tags'].append(tag.serialize)
        i += 1

    return jsonify(serialized_data)

@public_views.route("/tag/<string:tag>", methods=['GET'])
def get_entries_with_tag(tag):
    # Getting all the blog entries associated with a specific tag
    # First the database is queried for the tag id associated with the tag.
    tag_id = 0
    blog_id = []
    serialized_data = []

    for item in Tag.query.filter_by(name=tag).order_by(Tag.id).all():
        tag_id = item.id
    # Then the blog ids for the entries containing that tag are added to a list
    for item in db.session.query(tag_blog).filter_by(tag_id=tag_id).all():
        blog_id.append(item[1])

    # All the blog entries with ids in the list are fetched
    blog_entries_with_tag = Blog.query.filter(Blog.id.in_(blog_id)).order_by(Blog.created_at).all()

    # All the blogs are individually serialized and added to a list of serialized data
    for blog in blog_entries_with_tag:
        serialized_data.append(blog.serialize)

    # Each item in the list of serialized data is given a tags field
    for item in serialized_data:
        item['tags'] = []

    # The information for each tag is added to it's corresponding blog entry
    i = 0
    for blog in blog_entries_with_tag:
        for tag in blog.tags:
            serialized_data[i]['tags'].append(tag.serialize)
        i += 1

    return jsonify(serialized_data)

@public_views.route("/all_tags", methods=['GET'])
def get_all_tags():
    # Getting all tags
    all_tags = Tag.query.order_by(Tag.id).all()
    serialized_data = []
    all_relevant_tags = []

    # Adding only the tags with an existing blog entry to data being returned.
    # Also ignoring duplicate Tags
    for blog in Blog.query.order_by(Blog.created_at).all():
        for tag in all_tags:
            if tag in blog.tags:
                if tag in all_relevant_tags:
                    pass
                else:
                    all_relevant_tags.append(tag)

    for tag in all_relevant_tags:
        serialized_data.append(tag.serialize)

    return jsonify(serialized_data)


@public_views.route('/admin', methods=['POST'])
def login():
    # Receives login data in the form of JSON
    request_data = request.get_json()
    if request.method == 'POST':
        username = request_data['username']
        password = request_data['password']
        # Queries the database for all users
        user = User.query.filter_by(username=username).first()
        # If users are present it compares the username and password to see if that match.
        if user:
            if check_password_hash(user.password, password):
                response_object = {
                    'login': 'true',
                    'message': 'You have successfully logged in.'
                }
                json_object = jsonify(response_object)
                access_token = create_access_token(identity="Adam")
                set_access_cookies(json_object, access_token)
                return json_object
            else:
                return jsonify({'login': 'false', 'message': 'Invalid password.'})
        else:
            return jsonify({'login': 'false', 'message': 'Invalid username.'})
    else:
        return jsonify({'login': 'false', 'message': 'Method not POST.'})

# The following is code only used in the creation of this application, to experiment with the use of templates.

from flask import current_app as app
from flask import render_template, redirect, make_response
from werkzeug.security import generate_password_hash

@public_views.route("/")
def index():
    blog_entries = Blog.query.order_by(Blog.created_at).all()
    tags = Tag.query.order_by(Tag.id).all()
    return render_template('home.html', blog_entries=blog_entries, tags=tags)

# @public_views.route('/admin', methods=['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#
#         user = User.query.filter_by(username=username).first()
#         if user:
#             if check_password_hash(user.password, password):
#                 response = make_response(redirect('/admin/welcome'))
#                 access_token = create_access_token(identity="Adam")
#                 set_access_cookies(response, access_token)
#                 print('working')
#                 return response
#             else:
#                 print('password not found')
#                 return "Invalid email or password", 400
#         else:
#             print('user not found')
#             return redirect('/admin')
#     else:
#         print('method not post')
#         return render_template('login.html')

# @public_views.route("/tag/<string:tag>")
# def get_entries_with_tag(tag):
#     tag_id = 0
#     blog_id = []
#     for item in Tag.query.filter_by(name=tag).order_by(Tag.id).all():
#         tag_id = item.id
#     for item in db.session.query(tag_blog).filter_by(tag_id=tag_id).all():
#         blog_id.append(item[1])
#     blog_entries_with_tag = Blog.query.filter(Blog.id.in_(blog_id)).order_by(Blog.created_at).all()
#
#     return render_template('home.html', blog_entries=blog_entries_with_tag)

# @public_views.route('/create_user', methods=['POST'])
# def create_genesis():
#     from application.extensions import db
#     if request.method == 'POST':
#         username1 = request.form['username1']
#         password1 = request.form['password1']
#         password_hashed = generate_password_hash(password1, 'sha256', salt_length=12)
#         user_to_add = User(username=username1, password=password_hashed)
#         db.session.add(user_to_add)
#         db.session.commit()
#         return redirect('/')