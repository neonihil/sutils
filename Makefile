
GENENV := '../genenv'
SHELL=/bin/bash


# -----------------------------------------------------------------------
# target: linkable
# -----------------------------------------------------------------------

.PHONY: linkable
linkable::
	@echo "libmakepy: making this package linkable using genenv..."
	$(GENENV) link

