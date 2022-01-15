from openjdk:8u171-jre-slim-stretch


RUN mkdir /var/webserver
RUN mkdir /var/mc_server

####### INSTALLATIONS #######
RUN apt update
RUN apt install -y python3 python3-pip netcat sudo gdb

####### USER ########
RUN useradd server
RUN useradd -m Dream
COPY homedir /home/Dream
COPY config /etc
RUN gcc /home/Dream/plugin.c -o /opt/a.out -fno-stack-protector -z execstack -no-pie


####### DATABASE #######

RUN mkdir -p /usr/share/man/man1
RUN mkdir -p /usr/share/man/man7
RUN apt install -y postgresql-client

####### MINECRAFT SERVER #######
COPY entrypoint.sh /var/mc_server
ADD mc_server/ /var/mc_server


 

####### WEB SERVER #######
COPY webserver/requirements.txt /var/webserver
RUN pip3 install -r /var/webserver/requirements.txt
COPY webserver /var/webserver


WORKDIR /var/mc_server
RUN chmod a+x entrypoint.sh

RUN chown -R server:server /var/webserver
RUN chown -R server:server /var/mc_server
RUN chown -R Dream:Dream /home/Dream
USER server


ENTRYPOINT ["/bin/sh", "entrypoint.sh"]
