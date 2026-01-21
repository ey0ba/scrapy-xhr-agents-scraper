import scrapy
from urllib.parse import urljoin


class FirAgentsSpider(scrapy.Spider):
    name = "fir_agents"
    allowed_domains = ["fir.com"]
    start_urls = ["https://fir.com/agents"]

    custom_settings = {
        # polite + stable
        "ROBOTSTXT_OBEY": True,
        "AUTOTHROTTLE_ENABLED": True,
        "DOWNLOAD_DELAY": 0.8,
        "RETRY_TIMES": 3,
        "USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36",
    }

    def parse(self, response):
        # Luxury Presence typically renders an HTML grid with "team-member__container"
        cards = response.css(".team-member__container")
        if not cards:
            # fallback: sometimes class names vary slightly
            cards = response.css("[class*='team-member__container'], [class*='team-member__name']")

        for card in cards:
            name = self._clean(card.css(".team-member__name *::text").getall())
            role = self._clean(card.css(".team-member__role *::text").getall())

            # find a profile link (usually /agents/<slug> or /team/<slug>)
            href = (
                card.css("a::attr(href)").re_first(r"^/agents/[^\"'#?]+")
                or card.css("a::attr(href)").re_first(r"^/team/[^\"'#?]+")
                or card.css("a::attr(href)").get()
            )
            profile_url = urljoin(response.url, href) if href else None

            # image
            image_url = (
                card.css("img::attr(src)").get()
                or card.css("[style*='background-image']::attr(style)").re_first(r"url\(['\"]?([^'\")]+)")
            )
            if image_url:
                image_url = urljoin(response.url, image_url)

            item = {
                "name": name,
                "role": role,
                "profile_url": profile_url,
                "image_url": image_url,
                "source_url": response.url,
            }

            # If we have a profile URL, go deeper for phone/email/socials
            if profile_url:
                yield response.follow(
                    profile_url,
                    callback=self.parse_profile,
                    meta={"item": item},
                )
            else:
                yield item

        # pagination (if any)
        next_href = response.css("a[rel='next']::attr(href)").get()
        if next_href:
            yield response.follow(next_href, callback=self.parse)

    def parse_profile(self, response):
        item = response.meta["item"]

        # common contact patterns
        email = self._clean(response.css("a[href^='mailto:']::attr(href)").get())
        phone = self._clean(response.css("a[href^='tel:']::attr(href)").get())

        if email and email.lower().startswith("mailto:"):
            email = email.split("mailto:", 1)[1].strip()
        if phone and phone.lower().startswith("tel:"):
            phone = phone.split("tel:", 1)[1].strip()

        socials = {}
        for a in response.css("a::attr(href)").getall():
            if not a:
                continue
            a = a.strip()
            if "linkedin.com" in a:
                socials["linkedin"] = a
            elif "facebook.com" in a:
                socials["facebook"] = a
            elif "instagram.com" in a:
                socials["instagram"] = a
            elif "twitter.com" in a or "x.com" in a:
                socials["twitter"] = a

        # bio/description (best-effort)
        bio = self._clean(response.css("[class*='bio'] *::text, [class*='description'] *::text").getall())

        item.update(
            {
                "email": email,
                "phone": phone,
                "socials": socials,
                "bio": bio,
                "profile_source_url": response.url,
            }
        )
        yield item

    @staticmethod
    def _clean(text_or_list):
        if not text_or_list:
            return None
        if isinstance(text_or_list, list):
            s = " ".join([t.strip() for t in text_or_list if t and t.strip()])
        else:
            s = str(text_or_list).strip()
        s = " ".join(s.split())
        return s or None
