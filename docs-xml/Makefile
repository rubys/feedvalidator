docs: $(patsubst %.xml,../docs/%.html, error/*.xml warning/*.xml info/*.xml)

../docs/%.html: %.xml
	./build-html-docs.py template.html ../docs $<
