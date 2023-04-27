import secrets
from http import HTTPStatus

from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import FileResponse, Response
from starlette.templating import Jinja2Templates

from business_logic.authentication import oauth, is_google_authoritative, is_person_authorized, GOOGLE_MIN_OAUTH

router = APIRouter(
    prefix="/interface",
    tags=["interface"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

# Configure the app to use Jinja2 templates
templates = Jinja2Templates(directory='templates')


# Define a login route that redirects the user to the Google login page
@router.get('/login')
async def login(request: Request):
    """Generates a google authentication uri.
    Args:
        The request from the calling endpoint (i.e. 'login').
    Returns:
        The uri in str format, to be used in an HTML.
    Note:
        hasher & state - google recommends adding a random str
        to the uri for security purposes.
    """
    state = secrets.token_urlsafe(16)
    GOOGLE_MIN_OAUTH['state'] = state
    oauth.register(**GOOGLE_MIN_OAUTH)
    request.session["state"] = state
    redirect_url = request.url_for('auth').components.geturl()
    return await oauth.google.authorize_redirect(request, redirect_url, state=state)


@router.get('/auth')
async def auth(request: Request):
    """ Define an authentication route that exchanges the Google authorization code for an access token
    Note - oauth_state is a security measure. If fails, the process if aborted.
   If the user is authorized, they're logged into the session.
   Otherwise, return UNAUTHORIZED.
   Returns:
       person_info - person info from google.
   """
    user = await oauth.google.authorize_access_token(request)
    if not is_google_authoritative(user):
        # todo - add captcha - to prevent bot attacks
        pass
    email = user.get('email')
    if not is_person_authorized(email):
        return Response(HTTPStatus.UNAUTHORIZED)
    request.session['user'] = user
    return {'message': 'You are now logged in!'}  # todo - route back to main and flash login as a notification


@router.get('/add_user')
async def add_user():
    return FileResponse('view/templates/new_user.html')


@router.get('/new_user')
async def add_user(request: Request, user=Depends(auth.get_current_user)):
    # todo - finish authorization
    new_user_email = request.query_params.get("email", None)
    if new_user_email is None:
        return {"message": "Invalid email"}  # todo - validation that the email format is ok
    is_successful = auth.add_a_new_user_to_whitelist(new_user_email)
    if not is_successful:
        return {"message": "Failed to add a new user. Please try again later"}
    return {"message": f"Added a new user {new_user_email}"}
