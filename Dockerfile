FROM python:3.8

USER root
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y ffmpeg curl cmake \
    && rm -rf /var/lib/apt/lists/*

# for apt to get the coral libraries
RUN echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | tee /etc/apt/sources.list.d/coral-edgetpu.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -

# actually fetch the c libs (for the coral)
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
        libedgetpu1-std \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash user
RUN python -m pip install --upgrade pip

USER user

WORKDIR /home/user

COPY . .
COPY .env.template .env

USER root
RUN chown -R user:user *
USER user
RUN cd ./src/; python install.py

COPY requirements.txt .
RUN pip install -r requirements.txt && rm requirements.txt

RUN python ./src/bot.py init

ENTRYPOINT [ "python", "./src/bot.py"]
CMD ["text"]
