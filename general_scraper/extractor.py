import hashlib

class Extractor:
    def __init__(self, xpath_string, extract_as_html=False, element_save_method=None, output_file="extracted.html"):
        self.xpath_string = xpath_string
        self.extract_as_html = extract_as_html
        self.element_save_method = element_save_method
        self.output_file = output_file
        self.file = open(self.output_file, "a")
        self.total_extractions = 0
        self.total_saved = 0
        self.saved_hashes = []

    def extract(self, driver):
        return self.extracted_elements(self.xpath_matches(driver))

    def extract_from_elements(self, xpath_elements):
        if xpath_elements:
            self.total_extractions += len(xpath_elements)
            for element in xpath_elements:
                if self.element_save_method:
                    self.element_save_method(element)
                else:
                    if self.extract_as_html:
                        text = element.get_attribute('outerHTML')
                        self.save_text(text)
                    else:
                        text = element.text
                        self.save_text(text)
            return len(xpath_elements)
        return 0

    def xpath_matches(self, driver):
        return list(driver.find_elements_by_xpath(self.xpath_string))

    def save_text(self, text):
        text_hash = int(hashlib.sha256(text.encode('utf-8')).hexdigest(), 16)
        if text_hash not in self.saved_hashes:
            self.saved_hashes.append(text_hash)
            self.total_saved += 1
            self.file.write(text + "\n<br>\n")
            self.file.flush()
