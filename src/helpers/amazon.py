import boto3
import jwt

# Initialize a boto3 client for Cognito
client = boto3.client('cognito-idp', region_name='us-west-2')

# These are ok to share publicly
USER_POOL_ID = "us-west-2_EIgTRY9BB"
CLIENT_ID = "8b0e5aj57j4oevrtcdpe5455u"


# Signing in
def authenticate_user(username, password):
    try:
        response = client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": username,
                "PASSWORD": password
            }
        )
        # The ID token in response is used for authorization in further requests
        id_token = response["AuthenticationResult"]["IdToken"]
        access_token = response["AuthenticationResult"]["AccessToken"]
        refresh_token = response["AuthenticationResult"]["RefreshToken"]
        decoded_token = jwt.decode(id_token, options={"verify_signature": False})
        userId = decoded_token["sub"]
        email = decoded_token["email"]
        return {
            "userId": userId,
            "username": username,
            "email": email,
            "id_token": id_token,
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    except client.exceptions.NotAuthorizedException:
        print("The username or password is incorrect.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None


# Signing up
def register_user(username, password, email):
    try:
        response = client.sign_up(
            ClientId=CLIENT_ID,
            Username=username,
            Password=password,
            UserAttributes=[
                {"Name": "email", "Value": email}
            ]
        )
        return response
    except Exception as e:
        print(f"An error occurred during sign-up: {e}")
        return e


# Email will be sent to new user to verify their email
def confirm_user(username, confirmation_code):
    try:
        response = client.confirm_sign_up(
            ClientId=CLIENT_ID,
            Username=username,
            ConfirmationCode=confirmation_code
        )
        print("User confirmed successfully.")
        return response
    except Exception as e:
        print(f"An error occurred during user confirmation: {e}")
        return None


# Refresh user token. They have a 30 day expiration date.
# This doesnt need to be implemented till very end (not insanely important)
def refresh_session(refresh_token):
    try:
        response = client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={
                "REFRESH_TOKEN": refresh_token
            }
        )
        new_access_token = response["AuthenticationResult"]["AccessToken"]
        return new_access_token
    except Exception as e:
        print(f"An error occurred during session refresh: {e}")
        return None

# Potentially make a new access token refresh
# This could be when a user is inactive for a certain amount of time either log them out or get them a new one
