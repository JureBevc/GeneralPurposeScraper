class Extractor:
    def __init__(self, xpath_string, element_save_method=None, output_file="extracted.html"):
        self.xpath_string = xpath_string
        self.element_save_method = element_save_method
        self.output_file = output_file
        self.file = open(self.output_file, "a")

    def extract(self, driver):
        extracted_elements = driver.find_elements_by_xpath(self.xpath_string)
        if extracted_elements:
            print("Extracted elements: {}".format(len(extracted_elements)))
            for element in extracted_elements:
                if self.element_save_method:
                    self.element_save_method(element)
                else:
                    text = element.text
                    tl = text.lower()
                    if text and ("george" in tl or "michael" in tl):
                        self.file.write(text + "\n---\n")