
make:
	./workspace build

novision:
	./workspace build:novision

novision_debug:
	./workspace build:novision_debug

clean:
	./workspace clean

install:
	./deploy
