from bs4 import BeautifulSoup

def get_text_of_html(doc):
    """ 
    This function is for extracting text content from an HTML string.
    Input: HTML style string.
    Output: Extracted text content string.
    """
    
    soup = BeautifulSoup(doc, features='lxml')
    for script in soup(['script', 'style']):
        script.extract()
    
    text = soup.get_text().split()
    text = ' '.join([t for t in text if t])
    return text

def main():
    t = '  '
    get_text_of_html(t)

if __name__ == '__main__':
    main()