FROM python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY /app/requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install restarting-automata
