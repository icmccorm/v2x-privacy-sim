FROM python:3.9.9
WORKDIR /usr/src/v2x
RUN apt update && apt upgrade -y && apt install bc -y
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN wget https://github.com/GGZ8/PTF/raw/7156d10d2da4e3e8568d7a3b56551804281c4e7d/simulation_output.tgz
RUN tar -xzf simulation_output.tgz
COPY . .
CMD [ "make", "eval-dp" ]
