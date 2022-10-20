from pro_excel import config, create_app, db

app = create_app()
app.config.from_object(config.Config)

db.init_app(app)

if __name__ == '__main__':
    app.app_context().push()
    db.create_all()
    app.run(host='0.0.0.0', debug=True)