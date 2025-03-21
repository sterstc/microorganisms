########################################################################################################################

test_api : 
	@curl -X 'POST' \
  'http://127.0.0.1:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' -d '{ "area": 1,"perimeter": 1,"major_axis_length": 2,"minor_axis_length": 3}'

########################################################################################################################

### STRIP_START ###
.PHONY: docker_build docker_run docker_push gcp_build deploy

docker_build:
	docker build -t ${IMAGE_FLASK} . --file Dockerfile_flask

docker_run: 
	docker run -e PORT=${PORT} -p 8000:8080 ${IMAGE_FLASK}

docker_push:
	docker push ${LOCATION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${IMAGE_FLASK}

gcp_build:
	docker build --build-arg TARGETPLATFORM=linux/amd64 -t ${LOCATION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${IMAGE_FLASK}:latest . --file Dockerfile_flask
	# docker build -t ${LOCATION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${IMAGE_FLASK}:latest . --file Dockerfile_flask

deploy_service: 
	gcloud run deploy ${SERVICE} --image=${LOCATION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${IMAGE_FLASK}:latest \
  --platform=managed --region=${LOCATION} --allow-unauthenticated

deploy: gcp_build docker_push deploy_service 
### STRIP_END ###