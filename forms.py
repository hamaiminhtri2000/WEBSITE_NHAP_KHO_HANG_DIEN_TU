from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired

class SignUpForm(FlaskForm):
    inputFirstName = StringField('FirstName', [DataRequired(message="Hãy nhập Tên của bạn!")])
    inputLastName = StringField('LastName', [DataRequired(message="Hãy nhập Họ của bạn!")])
    inputEmail = StringField('Email Address', [Email(message="Địa chỉ Email đã tồn tại!"),
                                               DataRequired(message="Hãy nhập Email của bạn")])
    inputPassword = PasswordField('Password', [InputRequired(message="Hãy nhập Mật Khẩu của bạn!"),
                                               EqualTo('inputConfirmPassword', message="Mật Khẩu không hợp lệ!!")])
    inputConfirmPassword = PasswordField('ConfirmPassword', [DataRequired(message="Hãy nhập Xác Nhận Mật Khẩu của bạn!")])
    submit = SubmitField('Đăng Ký')

class SignInForm(FlaskForm):
    inputEmail = StringField('Email Address',
        [Email(message='Địa chỉ Email không có sẵn!'),
        DataRequired(message="Hãy nhập Email của bạn!")])
    inputPassword = PasswordField('Password',
        [InputRequired(message="Hãy nhập Mật Khẩu của bạn!")])
    submit = SubmitField('Đăng Nhập')

class AddProductForm(FlaskForm):
    inputProductName = StringField('Name',
        [DataRequired(message="Hãy nhập Tên Sản Phẩm!")])
    inputCategory = StringField('Category',
        [DataRequired(message="Hãy nhập Mã Sản Phẩm!")])
    inputPrice = IntegerField('Price',
        [DataRequired(message="Hãy nhập Đơn Giá!")])
    inputDate = DateTimeLocalField('Date',
        validators=[DataRequired(message="Hãy nhập Ngày Nhập!")], format='%Y-%m-%dT%H:%M')
    submit = SubmitField('Cập Nhật Danh Sách')