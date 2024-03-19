FROM ubuntu:22.04

RUN apt-get update && apt-get install -y tzdata 
CMD date

RUN apt-get update && apt-get install -y software-properties-common \
    && apt-get install -y build-essential \
    && apt-get install -y wget unzip

RUN add-apt-repository ppa:deadsnakes/ppa && apt-get update -y \
    && apt-get install -y python3.8

RUN apt-get install -y openjdk-8-jdk

RUN apt-get install -y kotlin

RUN wget https://services.gradle.org/distributions/gradle-7.3-bin.zip -P /tmp \
    && unzip -d /opt /tmp/gradle-*.zip \
    && ln -s /opt/gradle-*/ /opt/gradle \
    && echo "export PATH=$PATH:/opt/gradle/bin" >> /etc/profile.d/gradle.sh \
    && chmod +x /etc/profile.d/gradle.sh \
    && /bin/bash -c "source /etc/profile.d/gradle.sh"

WORKDIR /app
COPY . /app

RUN sed -i 's|dependencies {|dependencies {\n    implementation "org.xerial:sqlite-jdbc:3.36.0.3"|' build.gradle
RUN /opt/gradle/bin/gradle build

RUN ls -l /app

CMD ["kotlin", "-classpath", "app.jar", "HelloWorldKt"]
    