from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from custom_validation.validation import CustomValidation,OutputMessages

UserModel = get_user_model()

def custom_validation(data):
    required_fields = ["email","username","password"]
    cv = CustomValidation()
    
    #*validate passed all required fields as input fields
    validation = cv.basic_validation(user=False,input_fields=data,required_fields=required_fields)
    if not all(validation):
        return validation
    

    for key,value in data.items():
        if not isinstance(value,str):
            main = f"passed invalid type for {key}"
            err_msg = OutputMessages.error_with_message(main)
            return err_msg

    email = data['email'].strip()
    username = data['username'].strip()
    password = data['password'].strip()

    ## validate username password and username
    try:
        if not email or UserModel.objects.filter(email=email).exists():
            raise ValidationError('choose another email')
        ##
        if not password or len(password) < 8:
            raise ValidationError('choose another password, min 8 characters')
        ##
        if not username:
            raise ValidationError('choose another username')
        
        ##return successful data
        return True,data
    
    #here im returning the validation error message as a string
    except ValidationError as e:
        err_msg = OutputMessages.error_with_message(*e)
        return err_msg


def validate_email(data):
    email = data['email'].strip()
    if not email:
        raise ValidationError('an email is needed')
    return True

def validate_username(data):
    username = data['username'].strip()
    if not username:
        raise ValidationError('choose another username')
    return True

def validate_password(data):
    password = data['password'].strip()
    if not password:
        raise ValidationError('a password is needed')
    return True