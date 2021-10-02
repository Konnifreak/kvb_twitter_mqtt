FROM python:3.8

#ENV consumer_key: ${consumer_key}
#ENV consumer_secret: ${consumer_secret}
#ENV access_token: ${access_token}
#ENV access_token_secret: ${access_token_secret}

#ENV twitter_user_id: ${twitter_user_id}
#ENV mqtt_host_ip: ${mqtt_host_ip}
#ENV mqtt_client_id: ${mqtt_client_id}

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

CMD [ "python3","-u", "twitter_scraper.py" ]