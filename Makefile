.PHONY: css static

css:
	@./script/fingerprint_css

static: css
	@python manage.py generate_static
