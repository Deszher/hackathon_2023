SHELL    := /bin/zsh

# Local development
.PHONY: init
init: create-venv install-deps

.PHONY: create-venv
create-venv:
	python -m venv .venv

.PHONY: install-deps
install-deps:
	. ./.venv/bin/activate && pip install -r requirements.txt

.PHONY: dump-deps
dump-deps:
	. ./.venv/bin/activate && echo "--extra-index-url https://download.pytorch.org/whl/cpu" > requirements.txt && python -m pip freeze >> requirements.txt

.PHONY: version
version:
	. ./.venv/bin/activate && python --version && pip --version

.PHONY: test
test:
	. ./.venv/bin/activate && python -m pytest -W ignore::DeprecationWarning

# Docker
.PHONY: docker-build-images
build-docker-images: docker-build-base docker-build-streamlit

.PHONY: docker-build-base
docker-build-base:
	docker build -t hackathon-2023-base -f Dockerfile_base .

.PHONY: docker-build-streamlit
docker-build-streamlit:
	docker build -t hackathon-2023-streamlit --build-arg DEPS_IMAGE=hackathon-2023-base -f Dockerfile_streamlit .

.PHONY: docker-start-streamlit
docker-start-streamlit:
	docker run -p 8501:8501 hackathon-2023-streamlit
