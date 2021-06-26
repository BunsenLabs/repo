VERSION ?= 0.99.0
ARCH ?= amd64
DIST ?= lithium

repomgr_$(VERSION)_$(ARCH).deb: repomgr.dist repomgr.shim
	chmod 755 repomgr.dist/repomgr
	chmod 644 repomgr.dist/*.so
	chmod 755 repomgr.shim
	cd repomgr.dist && fpm             \
		-s dir                           \
		-t deb                           \
		--deb-dist $(DIST)               \
		-n repomgr                       \
		-v $(VERSION)                    \
		-d python3                       \
		-d python3-apt                   \
		.=/opt/bunsenlabs/repomgr        \
		../repomgr.shim=/usr/bin/repomgr
	cd repomgr.dist && mv $@ ./..

repomgr.dist: repomgr.shim
	poetry install
	poetry run nuitka3 --standalone repomgr

clean:
	-rm -rf -- ./repomgr.build ./repomgr.dist *.deb
