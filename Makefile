.PHONY: setup clean dev-up dev-down dev-logs test

VENV = .venv
UV = uv

setup:
	@echo "🚀 Setting up local environment..."
	$(UV) venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt

clean:
	rm -rf .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +

dev-up:
	@echo "🔥 Starting RIFE Processor environment..."
	docker compose up --build -d

dev-down:
	@echo "🛑 Shutting down..."
	docker compose down -v

dev-logs:
	@echo "📋 Tailing logs..."
	docker compose logs -f video-process-rife-service

setup-test:
	uv venv
	uv pip install grpcio 
	uv pip install sentiric-contracts-py git+https://github.com/sentiric/sentiric-contracts.git@v1.25.0

test:
	@echo "🧪 Running RIFE Refinement Test..."
	@. $(VENV)/bin/activate && python test_client.py