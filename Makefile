
.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?# .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?# "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: constraint
constraint: # Download constraints.txt file required for Airflow installation
	@echo "Installing constraints..."
	@AIRFLOW_VERSION=2.9.3; \
	PYTHON_VERSION=3.10; \
	CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"; \
	echo "downloading constraints from ${CONSTRAINT_URL}"; \
	curl "${CONSTRAINT_URL}" > constraints.txt

.PHONY: install
install: constraint # Install only production-requirements pypi packages
	@echo "Installing Airflow..."
	@# https://airflow.apache.org/docs/apache-airflow/2.9.3/installation.html#installation-tools
	pip install -r requirements.txt -c constraints.txt

.PHONY: clean
clean: # Remove constaints.txt file
	@rm -f constraints.txt
	
.PHONY: run
run: # Start the Airflow instance
	@echo "Starting Airflow..."
	@docker-compose up -d

.PHONY: stop
stop: # Stop the Airflow instance
	@echo "Stopping Airflow..."
	@docker-compose down --volumes --remove-orphans

.PHONY: maestro
maestro:
	@echo "Exporting maestro actions..."
	@cd dags && python -m maestro.collect_actions