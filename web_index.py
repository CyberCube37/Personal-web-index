from app import create_app, db

app = create_app()


if app.config["TESTING"]:
    from app.models import Link, Tag, User
    
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'Link': Link, 'Tag': Tag, 'User':User}