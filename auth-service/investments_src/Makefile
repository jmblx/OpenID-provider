ifeq ($(OS),Windows_NT)
    OS := windows
else
    OS := $(shell uname -s | tr A-Z a-z)
endif



collect-data:
ifeq ($(OS),windows)
	python -m main
else
	python3 -m main
endif
