.PHONY: build

SQLITE=sqlite3

install:
	pip3 install -r requirements.txt
	cd src; python3 install.py
	python3 src/bot.py init

database:
	$(SQLITE) fr.db -init ./data/import.sql ".exit"

clean_up:
	rm ./audio/*
	rm ./video/*
	rm ./image/*

run:
	@python3 src/bot.py

docker_build:
	rm -rf ./src/TensorFlowTTS
	rm -rf ./src/__pycache__
	@docker image build . -t mastodon_fr_bot

docker_run:
	@docker container run --rm \
		-v $(PWD)/.env:/home/user/.env \
		-t mastodon_fr_bot:latest

docker_run_video:
	@docker container run --rm \
		-v $(PWD)/.env:/home/user/.env \
		-v $(PWD)/audio:/home/user/audio \
		-v $(PWD)/image:/home/user/image \
		-v $(PWD)/video:/home/user/video \
		-t mastodon_fr_bot:latest video
