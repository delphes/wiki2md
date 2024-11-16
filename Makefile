HTML = $(shell find html -type f)
MD = $(patsubst html/%, md/%, $(patsubst %.html, %.md, $(HTML)))

PANDOC = pandoc -d defaults.yml
FORMAT = mdformat

MKDIR = mkdir -p
RM = rm -rf

.PHONY: clean

html:
	@python3 download.py

md: $(MD)

md/%.md: html/%.html
	@echo ">> Converting $^"
	@$(MKDIR) $(@D)
	@$(PANDOC) $< | sed '/^&nbsp;$$/d ; s/ *$$//' > $@
	@$(FORMAT) $@

clean:
	@$(RM) md html
