MD=$(shell find . -iname "*.md" -not -path '*_layouts*')
HTML=$(MD:.md=.html)

.PHONY = clean backup deploy
clean:
	rm $(HTML)

backup:
	tar --exclude=backup.tar.gz --exclude=.git/ \
		--exclude=venv/ --exclude=__pycache__/ \
		-czvf backup.tar.gz ./

deploy:
	rsync -avz --exclude '_*' --exclude '.git*' \
		--exclude 'venv*' --exclude '*.md' \
		`pwd`/ rogue@oxal.org:/var/www/website/public/
