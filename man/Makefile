#
# this make file builds the docmanager man page
#

#DB := /usr/share/xml/docbook/stylesheet/nwalsh/current
DB := http://docbook.sourceforge.net/release/xsl/current/
BUILDDIR := build
XMLFILE := docmanager.xml
OUTFILE := docmanager.1

.PHONY: all clean

all: clean $(BUILDDIR)
	xmllint --noout --xinclude --postvalid xml/$(XMLFILE)
	xsltproc --xinclude --nonet $(DB)/manpages/docbook.xsl xml/$(XMLFILE)
	mv $(OUTFILE) $(BUILDDIR)

clean:
	-rm -rf $(BUILDDIR)

$(BUILDDIR):
	mkdir $(BUILDDIR)
