from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models.blog_table import Blog
from app.models.tag_table import Tag
from .extensions import db
import os
import base64
import uuid

private_views = Blueprint("private_views", __name__)

@private_views.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_entry(id):
    if request.method == 'DELETE':
        # Finds entry based on id
        entry_to_delete = Blog.query.filter_by(id=id).first_or_404()
        blog_id = getattr(entry_to_delete, "id")

        # Finds and deletes image file from img static folder.
        for filename in os.listdir('app/static/img/'):
            if filename == os.path.basename(entry_to_delete.feature_image):
                name = os.path.basename(filename)
                path = os.path.join('app/static/img/', name)
                os.remove(path)

        # Deletes entry from database.
        db.session.delete(entry_to_delete)
        db.session.commit()
        return jsonify({"blog_id": blog_id})
    else:
        return jsonify({"Failure": "Method is not DELETE."})

@private_views.route('/create_entry', methods=['POST'])
@jwt_required()
def create_entry():
    if request.method == 'POST':
        # The blog post is received in the form of a JSON object
        new_blog = request.get_json()

        # The value of the JSON key 'feature_image' is an image formatted to base64
        # The following decodes the image and creates a unique filename
        image_decoded = base64.b64decode(new_blog['feature_image'])
        unique_filename = uuid.uuid4().hex + '.jpg'

        # The following creates a writeable image file that accepts bytes in the static folder of the app
        # Then writes our decoded image to the file
        upload_loc = 'app/static/img/'
        image = open(os.path.join(upload_loc, unique_filename), 'wb')
        image.write(image_decoded)
        image.close()

        # Then the path to the file and filename is saved to upload in the database
        for_image_display = '/static/img'
        file_path = os.path.join(for_image_display, unique_filename)

        # Creates a Blog Entry in the Blog table with the corresponding form data.
        entry_data = Blog(title=new_blog['title'],
                          feature_image=file_path,
                          content=new_blog['content'],
                          )

        # If the tag exists, the relationship to the blog is added to the associated blog tag table.
        # If the tag doesn't exist, it does the above step as well as creates the tag.
        for tag in new_blog['tags']:
            present_tag = Tag.query.filter_by(name=tag).first()
            if present_tag:
                present_tag.blogs_associated.append(entry_data)
            else:
                new_tag = Tag(name=tag)
                new_tag.blogs_associated.append(entry_data)
                db.session.add(new_tag)

        # The new blog entry record is saved to our database
        db.session.add(entry_data)
        db.session.commit()

        # The id attribute of the entry is retrieved and returned in the form of JSON
        blog_id = getattr(entry_data, "id")
        return jsonify({"blog_id": blog_id})
    else:
        return jsonify({"Failure": "Method is not POST."})

@private_views.route('/update_entry/<int:id>', methods=['GET','PUT'])
@jwt_required()
def update_entry(id):
    if request.method == 'GET':
        # If the method is GET we return a blog entry based on the id.
        # This way the current information associated with the post can be displayed.
        blog = Blog.query.filter_by(id=id).first()
        serialized_blog = blog.serialize
        serialized_blog["tags"] = []

        for tag in blog.tags:
            serialized_blog["tags"].append(tag.serialize)

        return jsonify({"single_blog": serialized_blog})

    elif request.method == 'PUT':
        # The info to update is received in the form of a JSON object
        updated_info = request.get_json()

        # Finds entry based on id
        entry_to_update = Blog.query.filter_by(id=id).first_or_404()

        entry_to_update.title = updated_info['title']
        entry_to_update.content = updated_info['content']

        # Finds and deletes current image file from img static folder.
        for filename in os.listdir('app/static/img/'):
            if filename == os.path.basename(entry_to_update.feature_image):
                name = os.path.basename(filename)
                path = os.path.join('app/static/img/', name)
                os.remove(path)

        # The value of the JSON key 'feature_image' is an image formatted to base64
        # The following decodes the image and creates a unique filename
        image_decoded = base64.b64decode(updated_info['feature_image'])
        unique_filename = uuid.uuid4().hex + '.jpg'

        # The following creates a writeable image file that accepts bytes in the static folder of the app
        # Then writes our decoded image to the file
        upload_loc = 'app/static/img/'
        image = open(os.path.join(upload_loc, unique_filename), 'wb')
        image.write(image_decoded)
        image.close()

        # Then the path to the file and filename is saved to upload in the database
        for_image_display = '/static/img'
        file_path = os.path.join(for_image_display, unique_filename)

        # Updates the database value to the new image filepath and filename
        entry_to_update.feature_image = file_path

        # Clears the contents of the current tags associated with the blog entry to be updated
        entry_to_update.tags = []

        # If the tag exists, the relationship to the blog is added to the associated blog tag table.
        # If the tag doesn't exist, it does the above step as well as creates the tag.
        for tag in updated_info["tags"]:
            present_tag = Tag.query.filter_by(name=tag).first()
            if(present_tag):
                present_tag.blogs_associated.append(entry_to_update)
            else:
                new_tag = Tag(name=tag)
                new_tag.blogs_associated.append(entry_to_update)
                db.session.add(new_tag)

        # The changes to the blog being updated are committed to the database.
        db.session.commit()

        blog_id = getattr(entry_to_update, "id")
        return jsonify({"blog_id": blog_id})

    else:
        return jsonify({"Failure": "Incorrect method."})

# The following is code only used in the creation of this app, to experiment with the use of templates.

# from flask import current_app as app
# from flask import render_template, redirect
# from app.models.user_table import User

# @private_views.route('/create_entry', methods=['POST', 'GET'])
# @jwt_required()
# def create_entry():
#     if request.method == 'POST':
#         # Requests the  file, gives it a secure filename, then places the image in the static img folder.
#         # Also, saves the img name with the associated Blog entry.
#         image = request.files['feature_image']
#         image_filename = secure_filename(image.filename)
#         upload_loc = 'app/static/img/'
#         for_image_display = '/static/img'
#         image.save(os.path.join(upload_loc, image_filename))
#         file_path = os.path.join(for_image_display, image_filename)
#
#         # Creates a Blog Entry in the Blog table with the corresponding form data.
#         entry_data = Blog(title=request.form['title'],
#                           feature_image=file_path,
#                           content=request.form['content'],
#                           )
#         tags = [request.form['tag1'], request.form['tag2'], request.form['tag3']]
#
#         # If the tag exists, the relationship to the blog is added to the associated blog tag table.
#         # If the tag doesn't exist, it does the above step as well as creating the tag.
#         for tag in tags:
#             present_tag = Tag.query.filter_by(name=tag).first()
#             if present_tag:
#                 present_tag.blogs_associated.append(entry_data)
#             else:
#                 new_tag = Tag(name=tag)
#                 new_tag.blogs_associated.append(entry_data)
#                 db.session.add(new_tag)
#
#         db.session.add(entry_data)
#         db.session.commit()
#         return redirect('/')
#     else:
#         return render_template('create_entry.html')