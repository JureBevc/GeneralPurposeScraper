class Extractor:
    def __init__(self, xpath_string, extract_as_html=False, element_save_method=None, output_file="extracted.html"):
        self.xpath_string = xpath_string
        self.extract_as_html = extract_as_html
        self.element_save_method = element_save_method
        self.output_file = output_file
        self.file = open(self.output_file, "a")
        self.total_extractions = 0
        self.total_saved = 0

    def extract(self, driver):
        extracted_elements = driver.find_elements_by_xpath(self.xpath_string)
        if extracted_elements:
            self.total_extractions += len(extracted_elements)
            for element in extracted_elements:
                if self.element_save_method:
                    self.element_save_method(element)
                else:
                    if self.extract_as_html:
                        text = element.get_attribute('outerHTML')
                        self.save_text(text)
                    else:
                        text = element.text
                        self.save_text(text)

    def save_text(self, text):
        self.total_saved += 1
        self.file.write(text + "\n<br>\n")
        self.file.flush()
