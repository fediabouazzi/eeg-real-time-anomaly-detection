up:
	docker-compose up --build

down:
	docker-compose down

logs:
	docker-compose logs -f

trainer:
	docker-compose run trainer

consumer:
	docker-compose restart consumer

streamlit:
	docker-compose restart streamlit

clean:
	rm -f *.pkl *.csv

test:
	python data_generator.py --samples 50
	python kafka_producer.py
	@echo "✅ Data sent to Kafka. Check Streamlit at http://localhost:8501"

test-alert:
	python scripts/test_alert_trigger.py

sync-hf:
	bash sync_to_hf.sh

