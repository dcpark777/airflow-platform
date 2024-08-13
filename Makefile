.PHONY
help:
	@echo "make help"
	@echo "make build"
	@echo "make run"
	@echo "make clean"

.PHONY
run: # Run the application
	@echo "Running the application"
	@python3 main.py