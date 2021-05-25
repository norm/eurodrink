.PHONY: clean css static upload

clean:
	git co templates/css.html

css:
	@./script/fingerprint_css

static: css
	@python manage.py generate_static

upload:
	aws s3 sync site/ s3://eurovisiondrinking.com/
	./script/invalidate
