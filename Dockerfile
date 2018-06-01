FROM python:3

ADD Main.py
ADD BotFunctions.py
ADD ESIFunctions.py
ADD ZkillFunctions.py
ADD FuzzworksFunctions.py

RUN pip install https://github.com/Rapptz/discord.py/archive/rewrite.zip

CMD [ "python", "./Main.py" ]