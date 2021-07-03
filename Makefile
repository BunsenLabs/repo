VERSION ?= 0.99.0
ARCH ?= amd64
DIST ?= lithium

repo_$(VERSION)_$(ARCH).deb: repo.dist repo.shim
	chmod 755 repo.dist/repo
	chmod 644 repo.dist/*.so
	chmod 755 repo.shim
	cd repo.dist && fpm             \
		-s dir                           \
		-t deb                           \
		--deb-dist $(DIST)               \
		-n repo                       \
		-v $(VERSION)                    \
		-d python3                       \
		-d python3-apt                   \
		.=/opt/bunsenlabs/repo        \
		../repo.shim=/usr/bin/repo
	cd repo.dist && mv $@ ./..

repo.dist: repo.shim
	poetry install
	poetry run nuitka3 --standalone repo

clean:
	-rm -rf -- ./repo.build ./repo.dist *.deb
