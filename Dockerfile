FROM python:3.6.6

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt
COPY main.py /
COPY discord_util.py /
EXPOSE 443
CMD [ "python", "/main.py" ]