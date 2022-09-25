#mcandrew;

PYTHON:=python3 -W ignore

process_HJ_predictions:
	mkdir -p ./data/continuous_predictions/ && \
	mkdir -p ./data/binary_predictions/ && \
	$(PYTHON) process_predictions.py && echo "HJ predictions processsed"
