FROM node:10.16.0

COPY services/tos_build_service /root/tos_build
COPY top-docker/tos_build_service/entrypoint.sh /root/entrypoint.sh


RUN chmod 777 -R /root/tos_build \
 && chmod 777 /root/entrypoint.sh \
 && chmod 777 /root/tos_build/make-cop-package-tmaxos.py \
 && apt-get update \
 && apt-get install python3 \
 && npm install yarn \
 && cd /root/tos_build \
 && yarn

EXPOSE 3400

ENTRYPOINT [ "/root/entrypoint.sh" ]