from fastapi import FastAPI
from api.routes import session, convert_session, accept_terms, remove_users, reset_password, change_bio, reset_link

app = FastAPI()

app.include_router(session.router, prefix="/session")
app.include_router(convert_session.router, prefix="/convert_session")
app.include_router(accept_terms.router, prefix="/accept_terms")
app.include_router(remove_users.router, prefix="/remove_users")
app.include_router(reset_password.router, prefix="/reset_password")
app.include_router(change_bio.router, prefix="/change_bio")
app.include_router(reset_link.router, prefix="/reset_link")
