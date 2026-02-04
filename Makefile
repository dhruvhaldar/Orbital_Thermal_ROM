install:
	pip install -r requirements.txt

train:
	cd src/offline_training/rom_generator && python pod_extract.py

run:
	cd src/onboard_runtime && python main_control.py

test:
	pytest tests/

docker-build:
	docker build -t orbital-thermal-rom .
