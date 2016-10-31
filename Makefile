MD=$(shell find . -iname "*.md" -not -path '*_layouts*')
HTML=$(MD:.md=.html)

.PHONY = clean backup deploy
clean:
	@-/bin/rm $(HTML) 2>/dev/null

backup:
	tar --exclude=backup.tar.gz --exclude=.git/ \
		--exclude=venv/ --exclude=__pycache__/ \
		-czvf backup.tar.gz ./

deploy:
	./stab.py && \
	rsync -avz --exclude '_*' --exclude '.git*' \
		--exclude 'venv*' --exclude '*.md' \
		`pwd`/ oxal:/var/www/oxal.org/stab/ && \
	$(MAKE) clean
