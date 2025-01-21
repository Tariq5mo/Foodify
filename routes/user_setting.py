#!/usr/bin/env python3
"""Signup route handler"""
from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from flask_login import current_user, login_required
from wtforms.validators import DataRequired, Length, Email, ValidationError, Regexp, Optional
from models import storage
setting_routes = Blueprint('setting_routes', __name__)


class UserSettingForm(FlaskForm):
    """User settings form"""
    username = StringField("Username", validators=[DataRequired()])
    address = StringField("Address", validators=[
        DataRequired(),
        Length(min=3, max=70, message="Address must be between 3 and 70 characters")
    ])
    email = StringField("Email", validators=[
        DataRequired(),
        Email(message="Please enter a valid email address")
    ])
    current_password = PasswordField("Current Password")
    new_password = PasswordField("New Password", validators=[
        Regexp(
            "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&_])[A-Za-z\\d@$!%*?&_]{8,32}$",
            message="Password must be 8-32 characters and include uppercase, lowercase, number and special character"
        ),
        Optional()
    ])
    submit = SubmitField("Submit")

    def validate_email(self, email):
        """Validate email is unique"""
        if email.data != current_user.email:
            from models.client import Client
            clients = storage.all(Client).values()
            if any(client.email == email.data for client in clients):
                raise ValidationError(
                    "Email already exists! Please choose a different one")

    def validate_current_password(self, current_password):
        """Validate current password if new password is provided"""
        if self.new_password.data and not current_password.data:
            raise ValidationError(
                "Current password is required to set new password")


@setting_routes.route("/setting", methods=["GET", "POST"])
@login_required
def setting():
    """Handle user settings"""
    user_setting_form = UserSettingForm()
    if request.method == "GET":
        user_setting_form.username.data = current_user.username
        user_setting_form.email.data = current_user.email
        user_setting_form.address.data = current_user.address
        # Changed from form to user_setting_form
        return render_template("user_setting.html", user_setting_form=user_setting_form)
    if user_setting_form.validate_on_submit():
        try:
            from models.client import Client
            from app import bcrypt

            # Get client
            clients = storage.all(Client).values()
            client = next(
                (c for c in clients if c.id == current_user.id), None)

            if client:
                # Handle password update first
                if user_setting_form.new_password.data:
                    # Verify current password
                    if not bcrypt.check_password_hash(client.password, user_setting_form.current_password.data):
                        flash("Current password is incorrect", "danger")
                        return redirect(url_for("setting_routes.setting"))

                    # Update password
                    hashed_password = bcrypt.generate_password_hash(
                        user_setting_form.new_password.data).decode('utf-8')
                    client.password = hashed_password
                    storage.save()
                    flash("Password updated successfully!", "success")

                # Handle profile updates
                if user_setting_form.email.data != client.email or user_setting_form.address.data != client.address:
                    client.email = user_setting_form.email.data
                    client.address = user_setting_form.address.data
                    storage.save()
                    flash("Profile information updated successfully!", "success")

            else:
                flash("User not found", "danger")

        except Exception as e:
            flash(f"Error updating profile: {str(e)}", "danger")

        return redirect(url_for("setting_routes.setting"))
    # If form validation failed, show errors
    for field, errors in user_setting_form.errors.items():
        for error in errors:
            flash(f"{field}: {error}", "danger")

    return redirect(url_for("setting_routes.setting"))
