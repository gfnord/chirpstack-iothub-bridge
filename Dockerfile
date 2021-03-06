FROM python

ENV VIRTUAL_ENV=/home/gustavo/environments/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app to image
COPY bridge_chirpstack_iothub.py .

