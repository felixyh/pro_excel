from pro_excel import create_app, config


app = create_app()

app.config.from_object(config.Config)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)