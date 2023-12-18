from app import create_app

if __name__ == '__main__':
    create_app(config_name='dev').run(debug=True,port=8080)

#Краже запускати через app.py!