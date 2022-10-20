from pro_excel import config, create_app


app = create_app()


app.config.from_object(config.Config)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)