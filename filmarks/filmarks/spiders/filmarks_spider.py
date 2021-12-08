import scrapy


class QuotesSpider(scrapy.Spider):
    name = "filmarks"

    def start_requests(self):
        urls = [
            'https://filmarks.com/list/year/2000s?view=poster',
            'https://filmarks.com/list/year/2010s?view=poster',
            'https://filmarks.com/list/year/2020s?view=poster',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        details_links = response.css(
            'body > div.l-main > div.p-content.p-content--grid > div.p-main-area.p-main-area--wide > div.p-contents-grid > div > a::attr(href)').getall()
        for link in details_links:
            yield response.follow(link, callback=self.parse_details)

        next = response.css(
            'body > div.l-main > div.p-content.p-content--grid > div.p-main-area.p-main-area--wide > div.c-pagination > a.c-pagination__next::attr(href)').get()
        if next:
            yield response.follow(next, callback=self.parse)

    def parse_details(self, response):
        # movie id
        id = response.url.split('/')[4]

        # poster img url
        img_url = response.css(
            'body > div.l-main > div.p-content-detail > div.p-content-detail__head > div > div.p-content-detail__body > div.p-content-detail__left > div.c-content.c-content--large > div.c-content__jacket > img::attr(src)').get()
        if img_url is None:
            img_url = response.css(
                'body > div.l-main > div.p-content-detail > div.p-content-detail__head > div > div.p-content-detail__body > div.p-content-detail__left > div.c-content.c-content--large > a > img::attr(src)').get()
        # japanese title
        title = response.css(
            'body > div.l-main > div.p-content-detail > div.p-content-detail__head > div > div.p-content-detail__body > div.p-content-detail__main > h2 > span::text').get()

        # original title
        original_title = response.css(
            'body > div.l-main > div.p-content-detail > div.p-content-detail__head > div > div.p-content-detail__body > div.p-content-detail__main > p::text').get()

        # movie info
        other_info = response.css(
            'body > div.l-main > div.p-content-detail > div.p-content-detail__head > div > div.p-content-detail__body > div.p-content-detail__main > div.p-content-detail__other-info')

        release_date = None
        production_countries = []
        runtime = None

        for other_info_title in other_info.css('h3::text').getall():
            if '上映日' in other_info_title:
                release_date = other_info_title.split('：')[1]

            elif '製作国' in other_info_title:
                production_countries = other_info.css(
                    'ul > li > a::text').getall()

            elif '上映時間' in other_info_title:
                runtime = other_info_title.split('：')[1]

        # production_year
        d = response.css(
            'body > div.l-main > div.p-content-detail > div.p-content-detail__head > div > div.p-content-detail__body > div.p-content-detail__main > h2 > small > a::attr(href)').get()

        production_year = None
        if d is not None:
            production_year = d.split('/')[4]

        # movie genres
        genres = response.css(
            'body > div.l-main > div.p-content-detail > div.p-content-detail__head > div > div.p-content-detail__body > div.p-content-detail__main > div.p-content-detail__genre > ul > li > a::text').getall()

        # movie outline
        outline = response.css(
            '#js-content-detail-synopsis > content-detail-synopsis')
        outline = outline.attrib[':outline'] if ':outline' in outline.attrib else None

        # directors and screenwriters
        other_people = {}
        for o in response.css(
                'body > div.l-main > div.p-content-detail > div.p-content-detail__head > div > div.p-content-detail__body > div.p-content-detail__main > div.p-content-detail__people-list > div.p-content-detail__people-list-others__wrapper > div'):
            t = o.css('h3::text').get()
            other_people[t] = []
            for a in o.css('ul > li > a'):
                other_people[t].append({'id': a.css('::attr(href)').get().split(
                    '/')[2], 'name': a.css('::text').get()})

        # actors
        actors = []
        for a in response.css('#js-content-detail-people-cast > ul > li > a'):
            actors.append({'id': a.css('::attr(href)').get().split(
                '/')[2], 'name': a.css('::text').get()})

        # star rating score
        rating_score = response.css(
            'body > div.l-main > div.p-content-detail > div.p-content-detail__head > div > div.p-content-detail__body > div.p-content-detail__main > div.p-content-detail-state > div > div > div.c-rating__score::text').get()

        trailer_url = response.css(
            '#js-tab-content__trailer > div > iframe::attr(src)').get()

        yield {
            'id': id,
            'title': title,
            'original_title': original_title,
            'img_url': img_url,
            'release_date': release_date,
            'production_year': production_year,
            'production_countries': production_countries,
            'runtime': runtime,
            'rating_score': rating_score,
            'genres': genres,
            'outline': outline,
            'production_members': other_people,
            'actors': actors,
            'trailer_url': trailer_url
        }
