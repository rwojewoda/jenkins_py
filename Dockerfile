FROM arm32v6/openjdk:8-alpine
VOLUME /tmp
COPY target/*.jar app.jar
EXPOSE 808a
ENTRYPOINT ["java","-jar","/app.jar"]