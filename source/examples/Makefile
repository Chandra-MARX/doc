# -*- sh -*-

SUBDIRS = ACISpowerpileup aped hetgplaw LETGpow marxcat background simobs
SUBCLEAN = $(addsuffix .clean,$(SUBDIRS))
SUBDISTCLEAN = $(addsuffix .distclean,$(SUBDIRS))

.PHONY: all clean distclean $(SUBDIRS) $(SUBCLEAN)

all: $(SUBDIRS)

$(SUBDIRS):
	$(MAKE) -C $@

clean: $(SUBCLEAN)
        
$(SUBCLEAN): %.clean:
	$(MAKE) -C $* clean

distclean: $(SUBDISTCLEAN)
        
$(SUBDISTCLEAN): %.distclean:
	$(MAKE) -C $* distclean
