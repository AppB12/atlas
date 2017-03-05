from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import re
import traceback
from datetime import datetime
import logging
from atlas.config import dbConfig


# Global variables
browser = None
next_page_link = ''  # Holds link to the next Result page
pagination = []  # Holds list of all Result pages
has_next_page = False  # If current page HAS a next page (for PRODUCTS)
links_list = []  # Holds links to all products on current Result page
all_links_list = []  # Holds links of all products through all pages
abbreviated_reviews_list = []  # List of abbreviated reviews of current product
final_reviews_list = []  # Holds all reviews of current product
is_last_page = True  # If current page IS the last page (for REVIEWS)
all_reviews = []  # Holds all reviews of one product (iteration)
all_kw_all_rev = []  # Holds all reviews of all products/keywords
prods_info = []   # Holds all product information for all products

###################################################################


# Scrape links for each product on current Result page, and store link to next Result page
def link_scraper():

    global links_list, next_page_link, pagination, has_next_page, browser

    links = []  # Links obtained on current Result page

    prods = browser.find_elements_by_xpath("//div[@class='pod-plp__description']//a")  # Links to products
    for p in prods:
        links.append(p.get_attribute("href"))

    # To check if link to next Result page is present
    try:
        next_res_page = browser.find_element_by_xpath("//a[contains(@class,'hd-pagination__link') and contains(@title,'Next')]")
        next_page_link = next_res_page.get_attribute("href")
        has_next_page = True
    except:
        has_next_page = False

    for i in range(0, 3):  # for i in links:  # To add fetched product links from current Result page to 'links_list'
        links_list.append(links[i])  # links_list.append(i)
        print "Link: " + links[i]
        logging.info("Link: " + str(links[i]))

    print "Total products on this Result page: ", len(links_list)
    logging.info("Total products on this Result page: " + str(len(links_list)))

###################################################################


# To remove HTML tags present in the abbreviated reviews list (obtained when fetching full text)
def clean_abbr_reviews(abbreviated_reviews_list1):
    global abbreviated_reviews_list, final_reviews_list
    for s in range(len(abbreviated_reviews_list1)):
        temp_str = ''
        str1 = abbreviated_reviews_list1[s]
        start_index = []
        end_index = []

        # To store start index and end index in order to select and remove substring containing only full text of review
        for m in re.finditer('<span class="BVRRReviewText">', str1):
            start_index.append(m.start())
        for m in re.finditer('</span>', str1):
            end_index.append(m.end())
        for n in range(len(start_index)):
            str2 = str1[start_index[n]+29:end_index[n]-7]  # 29 characters in opening tag and 7 characters in closing tag (Character at start index is included, character at end index is excluded)
            temp_str += " " + str2
        abbreviated_reviews_list1[s] = temp_str
    abbreviated_reviews_list = abbreviated_reviews_list1
    return abbreviated_reviews_list

###################################################################


# To fetch all reviews of the current product
def get_reviews(curr_link):
    global all_reviews, abbreviated_reviews_list, final_reviews_list, has_next_page, is_last_page, browser

    browser.get(curr_link)  # Navigate to link
    time.sleep(5)

    try:
        # Each variable related to reviews stores an array of corresponding values from all reviews
        try:  # Element may or may not be present, hence try-except used
            prod_brand = str(browser.find_element_by_class_name("product-title__brand").text)
            if "Discontinued" in prod_brand:  # Generally prefixed to the brand, if product is discontinued
                prod_brand = prod_brand[12:]  # To extract only the brand name
                prod_brand = prod_brand.strip()  # Trims white spaces from both ends
        except:
            prod_brand = '#N/A'
        print "Product Brand: " + prod_brand
        logging.info("Product Brand: " + prod_brand)

        # Product title is always present
        prod_title = browser.find_element_by_class_name("product-title__title").text
        print "Product Title: " + prod_title
        logging.info("Product Title: " + prod_title)

        try:
            model_info = browser.find_element_by_class_name("brandModelInfo").text
        except:
            model_info = '#N/A'
        print "Model Number: " + model_info
        logging.info("Model Number: " + model_info)

        try:
            rating_elem = browser.find_element_by_css_selector("div.BVRRRatingNormalOutOf")
            rating_value = rating_elem.get_attribute("textContent")
        except:
            rating_value = '#N/A'
        print "Rating: " + rating_value
        logging.info("Rating: " + rating_value)

        try:
            price = browser.find_element_by_id('ajaxPrice').text
        except:
            price = '#N/A'
        print "Price: " + price
        logging.info("Price: " + price)

        try:  # To check if reviews are available for product
            review_text = browser.find_elements_by_class_name("BVRRReviewTextContainer")
        except:
            review_text = ''  # >>> DO NOT PUT N/A OR ANY OTHER VALUE <<< for the sake of 'if' condition below

        if len(review_text):  # Checking if reviews are available for the product, hence not appending anything if no review text found
            print "Now fetching reviews on this page..."
            logging.info("Now fetching reviews on this page...")
            is_last_page = False
            final_reviews_list = []
            while not is_last_page:  # While is_last_page is FALSE

                # Following WebElements are fetched for the current Review page only
                user_name = browser.find_elements_by_class_name("BVRRNickname")
                review_title = browser.find_elements_by_class_name("BVRRReviewTitleContainer")
                review_date = browser.find_elements_by_class_name("BVRRReviewDateContainer")
                review_text = browser.find_elements_by_class_name("BVRRReviewTextContainer")  # Contains abbreviated versions of review texts (if any)

                print "Total reviews on this page: ", len(review_text)
                logging.info("Total reviews on this page: " + str(len(review_text)))

                flag = 0  # To indicate if abbreviated reviews are present or not

                # To extract all abbreviated reviews' content in full (if any), and store in (subset) array
                abbreviated_reviews_list = []
                for r in review_text:  # Loop through each review fetched on the current Review page
                    if "Read More" in r.text[-9:]:  # If 'Read More' is present at the end of the text
                        flag = 1  # Flag made 1 when abbreviated text found

                        div_elems = browser.find_elements_by_xpath("//div[@class='BVRRReviewText BVDIHidden']")  # Contains only abbreviated reviews' full text

                        print "No. of abbreviated reviews on this Review page: ", len(div_elems)
                        logging.info("No. of abbreviated reviews on this Reviews page: " + str(len(div_elems)))

                        for e in div_elems:
                            abbreviated_reviews_str = e.get_attribute("innerHTML")
                            abbreviated_reviews_list.append(abbreviated_reviews_str)

                        # To remove HTML tags and fetch only text content
                        abbreviated_reviews_list = clean_abbr_reviews(abbreviated_reviews_list)
                        break

                k = len(final_reviews_list)  # Index of latest review fetched

                # Separate array is used to store final list of reviews for the product (for easier manipulation)

                # If abbreviated reviews are present on this page, store their full text instead
                if flag == 1:
                    j = 0  # Index for abbreviated_reviews_list

                    for r1 in range(0, len(review_text)):  # Loop through each review fetched from current Review page
                        if "Read More" in review_text[r1].text[-9:]:  # If it's an abbreviated review, store its full text
                            final_reviews_list.append(abbreviated_reviews_list[j])
                            j += 1  # Increment index
                        else:  # If review is not abbreviated, store it as is
                            final_reviews_list.append(review_text[r1].text)

                # If no abbreviated reviews are present on this page, then simply copy the reviews into final_reviews_list
                else:
                    for r1 in range(0, len(review_text)):
                        final_reviews_list.append(review_text[r1].text)

                # Reviews are ready.
                # Create a data frame for each review and append it to a main data frame
                print "Appending all the fetched reviews..."
                logging.info("Appending all the fetched reviews...")

                for i in range(0, len(review_date)):  # Loop through reviews
                    try:
                        one_review = pd.DataFrame({'siteCode': ['HD'],
                                                   'pBrand': [prod_brand],
                                                   'pTitle': [prod_title],
                                                   'pModel': [model_info],
                                                   'price': [price],
                                                   'rUser': [user_name[i].text],
                                                   'rRating': [rating_value],
                                                   'rTitle': [review_title[i].text],
                                                   'rDate': [review_date[i].text],
                                                   'rText': [final_reviews_list[k]],
                                                   'pURL': [curr_link]}, index=[0])
                        k += 1  # Increment index of latest fetched review
                        all_reviews = all_reviews.append(one_review)

                    except:
                        print "Error while collating this review!!!"
                        logging.info("Error while collating this review!!!")
                        print traceback.print_exc()
                        logging.info(traceback.print_exc())
                # 'for' loop for collating reviews ends here

                # FOLLOWING CODE IS WORKING FOR LOOPING THROUGH ALL REVIEW PAGES. COMMENTED OUT TEMPORARILY.
                #
                #print "Checking for more review pages..."
                #logging.info("Checking for more review pages...")
                #
                ## If next Review page is available, go to next Review page
                #if browser.find_elements_by_xpath("//span[@class='BVRRPageLink BVRRNextPage']"):  # If " > " (Next Review Page arrow) is fetched
                #    is_last_page = False
                #    # Emulate clicking it
                #    next_page_elem = browser.find_elements_by_xpath("//span[@class='BVRRPageLink BVRRPageNumber BVRRSelectedPageNumber']//following-sibling::span")
                #    for n in next_page_elem:
                #        n.click()
                #        break
                #    print "Going to next Review page..."
                #    logging.info("Going to next Review page...")
                #    time.sleep(2.5)
                #
                ## If " > " (Next Review Page arrow) is not fetched
                #else:
                #    print "No more Review pages..."
                #    logging.info("No more Review pages...")
                #    is_last_page = True
                #    break
                break
            # 'while not is_last_page' ends here

            print "Total reviews fetched for this product: ", len(final_reviews_list)
            logging.info("Total reviews fetched for this product: " + str(len(final_reviews_list)))

        # If no reviews available for this product, then create dummy data frame without reviews and append to main data frame
        else:
            print "No reviews available for this product..."
            logging.info("No reviews available for this product...")
            try:
                one_review = pd.DataFrame({'siteCode': ['HD'],
                                           'pBrand': [prod_brand],
                                           'pTitle': [prod_title],
                                           'pModel': [model_info],
                                           'price': [price],
                                           'rUser': '#N/A',
                                           'rRating': [rating_value],
                                           'rTitle': '#N/A',
                                           'rDate': '#N/A',
                                           'rText': '#N/A',
                                           'pURL': [curr_link]}, index=[0])
            except:
                print "Error while appending dummy review!"
                logging.info("Error while appending dummy review!")
                all_reviews = all_reviews.append(one_review)
        # 'else' of (if len(review_text)) ends here

    except:
        print "Error(!) while scraping reviews @ ", curr_link
        logging.info("Error(!) while scraping reviews @ " + curr_link)
        print traceback.print_exc()
        logging.info(traceback.print_exc())

###################################################################


# To scrape product information and reviews from HomeDepot
def home_depot_all_info(keywords_list):
    global all_reviews, all_kw_all_rev, next_page_link, has_next_page, all_links_list, links_list, browser

    print 'Keywords: ', keywords_list
    logging.info('Keywords: ' + str(keywords_list))

    # chrome_path = 'C:\Python27\selenium\webdriver\chromedriver.exe'
    chrome_path = dbConfig.dict["chromeDriver"]
    browser = webdriver.Chrome(chrome_path)

    # Create main data frame to hold all product information and reviews of current keyword
    all_reviews = pd.DataFrame({'siteCode': ['HD'],
                                'pBrand': [' '],
                                'pTitle': [' '],
                                'pModel': [' '],
                                'price': [' '],
                                'rUser': [' '],
                                'rRating': [' '],
                                'rTitle': [' '],
                                'rDate': [' '],
                                'rText': [' '],
                                'pURL': [' ']}, index=[0])

    # Creates aggregated data frame to hold all product information and reviews of all keywords
    all_kw_all_rev = pd.DataFrame({'siteCode': ['HD'],
                                   'pBrand': [' '],
                                   'pTitle': [' '],
                                   'pModel': [' '],
                                   'price': [' '],
                                   'rUser': [' '],
                                   'rRating': [' '],
                                   'rTitle': [' '],
                                   'rDate': [' '],
                                   'rText': [' '],
                                   'pURL': [' ']}, index=[0])

    print "Scraper started at ", datetime.now().strftime("%A, %d %B %Y %I:%M:%S %p")

    # Searches for each keyword and extracts links for each product through all product pages
    for i in range(0, len(keywords_list)):
        print "Searching for '"+keywords_list[i]+"'..."
        logging.info("Searching for '"+keywords_list[i]+"'...")

        browser.get("http://www.homedepot.com/")
        time.sleep(5)

        element = browser.find_element_by_id("headerSearch")   # Search box on the site homepage
        element.send_keys(keywords_list[i])  # Enter keyword into search box
        element.send_keys(Keys.RETURN)  # Emulate pressing Enter

        all_links_list = []  # Refresh for each product

        try:
            time.sleep(5)  # Wait till results are loaded
            x = browser.current_url

            print "On the first Results page: " + x
            logging.info("On the first Results page: " + x)

            pagination.append(x)

            # Get links to products on this Result page, and link to next Result page
            link_scraper()  # Updates 'links_list' and 'next_page_link'

            for i1 in range(len(links_list)):
                curr_link = links_list[i1]

                print "Getting product information and reviews for this product: " + curr_link
                logging.info("Getting product information and reviews for this product: " + curr_link)

                get_reviews(curr_link)

            # FOLLOWING CODE IS WORKING FOR LOOPING THROUGH ALL RESULT PAGES. COMMENTED OUT TEMPORARILY.
            #while has_next_page:  # While current Results page is not the last page
            #    print "Going to next Results page: " + next_page_link
            #    logging.info("Going to next Results page: " + next_page_link)
            #
            #    browser.get(next_page_link)
            #    time.sleep(4)
            #    pagination.append(next_page_link)
            #
            #    # Reset following variables for each Results page
            #    next_page_link = ''
            #    has_next_page = False
            #    all_links_list += links_list  # Emptying 'links_list' into 'all_links_list'
            #    links_list = []
            #
            #    link_scraper()  # Updates 'links_list' and 'next_page_link'
            #
            #    for i1 in range(len(links_list)):
            #        curr_link = links_list[i1]
            #
            #        print "Getting product information and reviews for this product: " + curr_link
            #        logging.info("Getting product information and reviews for this product: " + curr_link)
            #
            #        get_reviews(curr_link)
            ## 'while has_next_page' ends here
        # 'try' inside 'for' for looping through keywords ends here

        except TypeError:
            pass
        except:
            print "Inside 'except' of looping through keywords..."
            logging.info("Inside 'except' of looping through keywords...")

        # Done scraping for current keyword
        print "Done scraping for '" + keywords_list[i] + "'..."
        logging.info("Done scraping for '" + str(keywords_list[i]) + "'...")

        print "Total Results pages traversed: ", str(len(pagination))
        logging.info("Total Results pages traversed: " + str(len(pagination)))

        #print "Total products fetched: ", len(all_links_list)
        #logging.info("Total products fetched: " + str(len(all_links_list)))

        print "Scraper finished at... ", datetime.now().strftime("%A, %d %B %Y %I:%M:%S %p")
        logging.info("Scraper finished at... " + datetime.now().strftime("%A, %d %B %Y %I:%M:%S %p"))

        # Saving the CSV file with product information and reviews; one CSV for each product/keyword
        curr_timestamp = datetime.now().strftime("%d%B%Y_%I%M%S%p")
        temp_keyword = keywords_list[i].replace(" ", "")
        output_file_name = 'HomeDepot_' + temp_keyword + '_' + curr_timestamp + '.csv'
        full_path = dbConfig.dict["homedepotOutput"] + output_file_name
        all_reviews.to_csv(full_path, index=False, encoding='utf-8')
        print "CSV file for this product saved at location: " + full_path
        logging.info("CSV file for this product saved at location: " + full_path)

        all_kw_all_rev = all_kw_all_rev.append(all_reviews)

    return all_kw_all_rev
# #################################################################


# To fetch product information from HomeDepot at current Product page
def get_prod_info(curr_link):
    global prods_info

    browser.get(curr_link)  # Navigate to link
    time.sleep(5)

    try:  # Element may or may not be present, hence try-except used
        prod_brand = str(browser.find_element_by_class_name("product-title__brand").text)
        if "Discontinued" in prod_brand:  # Generally prefixed to the brand, if product is discontinued
            prod_brand = prod_brand[12:]  # To extract only the brand name
            prod_brand = prod_brand.strip()  # Trims white spaces from both ends
    except:
        prod_brand = '#N/A'
    print "Product Brand: " + prod_brand
    logging.info("Product Brand: " + prod_brand)

    # Product title is always present
    prod_title = browser.find_element_by_class_name("product-title__title").text
    print "Product Title: " + prod_title
    logging.info("Product Title: " + prod_title)

    try:
        model_info = browser.find_element_by_class_name("brandModelInfo").text
    except:
        model_info = '#N/A'
    print "Model Number: " + model_info
    logging.info("Model Number: " + model_info)

    try:
        rating_elem = browser.find_element_by_css_selector("div.BVRRRatingNormalOutOf")
        rating_value = rating_elem.get_attribute("textContent")
    except:
        rating_value = '#N/A'
    print "Rating: " + rating_value
    logging.info("Rating: " + rating_value)

    try:
        price = browser.find_element_by_id('ajaxPrice').text
    except:
        price = '#N/A'
    print "Price: " + price
    logging.info("Price: " + price)

    try:
        # 'prod_info' contains current product's information and is appended to main data frame 'prods_info'
        prod_info = pd.DataFrame({'pBrand': [prod_brand],
                                  'pTitle': [prod_title],
                                  'pModel': [model_info],
                                  'price': [price],
                                  'rRating': [rating_value],
                                  'pURL': [curr_link]}, index=[0])
        prods_info = prods_info.append(prod_info)
    except:
        print "Error while appending product information!"
        logging.info("Error while appending product information!")

###############################################################################################


# To scrape product information from HomeDepot
def home_depot_prod_info(keywords_list):
    global prods_info, next_page_link, has_next_page, all_links_list, links_list, browser

    print 'Keywords: ', keywords_list
    logging.info('Keywords: ' + str(keywords_list))

    # chrome_path = 'C:\Python27\selenium\webdriver\chromedriver.exe'
    chrome_path = dbConfig.dict["chromeDriver"]
    browser = webdriver.Chrome(chrome_path)

    # Create main data frame to hold all products' information
    prods_info = pd.DataFrame({'pBrand': [' '],
                               'pTitle': [' '],
                               'pModel': [' '],
                               'price': [' '],
                               'rRating': [' '],
                               'pURL': [' ']}, index=[0])

    print "Scraper started at ", datetime.now().strftime("%A, %d %B %Y %I:%M:%S %p")

    # Searches for each keyword and extracts links for each product through all product pages
    for i in range(0, len(keywords_list)):
        print "Searching for '" + keywords_list[i] + "'..."
        logging.info("Searching for '" + keywords_list[i] + "'...")

        browser.get("http://www.homedepot.com/")
        time.sleep(5)

        element = browser.find_element_by_id("headerSearch")  # Search box on the site homepage
        element.send_keys(keywords_list[i])  # Enter keyword into search box
        element.send_keys(Keys.RETURN)  # Emulate pressing Enter

        all_links_list = []  # Refresh for each product

        try:
            time.sleep(5)
            x = browser.current_url

            print "In the first Results page: ", x
            logging.info("In the first Results page: " + x)

            pagination.append(x)


            # Get links to products on this Result page, and link to next Result page
            link_scraper()  # Updates 'links_list' and 'next_page_link'

            for i1 in range(len(links_list)):
                curr_link = links_list[i1]
                print "Getting info for this product: " + curr_link
                logging.info("Getting info for this product: " + curr_link)
                get_prod_info(curr_link)
            # # FOLLOWING CODE WORKS FOR LOOPING THROUGH RESULT PAGES. COMMENTED OUT TEMPORARILY.
            #while has_next_page:
            #    print "Going to next Results page: " + next_page_link
            #    logging.info("Going to next Results page: " + next_page_link)
            #
            #    browser.get(next_page_link)
            #    time.sleep(4)
            #    pagination.append(next_page_link)
            #
            #    # Reset following variables for each Results page
            #    next_page_link = ''
            #    has_next_page = False
            #    all_links_list = all_links_list + links_list  # Emptying 'links_list' into 'all_links_list'
            #    links_list = []
            #
            #    link_scraper()  # Updates 'links_list' and 'next_page_link'
            #
            #    for i1 in range(len(links_list)):
            #        curr_link = links_list[i1]
            #
            #        print "Getting info for this product: " + curr_link
            #        logging.info("Getting info for this product: " + curr_link)
            #
            #        get_prod_info(curr_link)
            ## 'while has_next_page' ends here
        # 'try' inside 'for' for looping through keywords ends here

        except TypeError:
            pass
        except:
            print "Inside 'except' of looping through keywords..."
            logging.info("Inside 'except' of looping through keywords...")

        # Done scraping for current keyword
        print "Done scraping for '" + keywords_list[i] + "'..."
        logging.info("Done scraping for '" + str(keywords_list[i]) + "'...")

        print "Total Results pages traversed: ", str(len(pagination))
        logging.info("Total Results pages traversed: " + str(len(pagination)))

        #print "Total products fetched: ", len(all_links_list)
        #logging.info("Total products fetched: " + str(len(all_links_list)))

        print "Scraper finished at... ", datetime.now().strftime("%A, %d %B %Y %I:%M:%S %p")
        logging.info("Scraper finished at... " + datetime.now().strftime("%A, %d %B %Y %I:%M:%S %p"))

        # Saving the CSV file with product information and reviews; one CSV for each product/keyword
        curr_timestamp = datetime.now().strftime("%d%B%Y_%I%M%S%p")
        temp_keyword = keywords_list[i].replace(" ", "")
        output_file_name = 'HomeDepotProdsInfo_' + temp_keyword + '_' + curr_timestamp + '.csv'
        full_path = dbConfig.dict["homedepotOutput"] + output_file_name
        prods_info.to_csv(full_path, index=False, encoding='utf-8')
        print "CSV file for this product saved at location: " + full_path
        logging.info("CSV file for this product saved at location: " + full_path)
