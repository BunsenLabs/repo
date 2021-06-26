VERSION ?= 0.99.0
ARCH ?= amd64

repomgr_$(VERSION)_$(ARCH).deb: repomgr.dist repomgr.shim
	cd repomgr.dist && fpm -s dir -t deb -n repomgr -v $(VERSION) -d python3 -d python3-apt .=/opt/bunsenlabs/repomgr ../repomgr.shim=/usr/bin/repomgr
	cd repomgr.dist && mv $@ ./..

repomgr.dist: repomgr.shim
	poetry install
	poetry run nuitka3 --standalone repomgr
