import HomeDepot
import Amazon_I1
import logging
from datetime import datetime
import time
import traceback
import pandas as pd
from atlas.config import dbConfig


print("Imports complete")
# ############################################################################

# Global variables
integ_data_frame = []

# ############################################################################


# To take keywords to search for as input from user
def keywords_input():
    keyword_list = list()
    kw = raw_input("Keyword:")
    logging.info("Keyword:" + kw)
    keyword_list.append(kw)
    return keyword_list

# ############################################################################


# To remove empty rows created while integrating dataframes
def clean_integ_dataframe(final_df):
    final_df1 = final_df[final_df.pURL != " "]
    return final_df1

# ############################################################################


# Checks if user wants to run Auscer again
def scrape_again():
    global run_again
    y_n = raw_input("Do you want to scrape another site (Y/N)? ")
    logging.info("Do you want to scrape another site (Y/N)? " + y_n)
    if y_n == 'y' or y_n == 'Y':
        run_again = True
    elif y_n == 'n' or y_n == 'N':
        run_again = False
    else:
        print "Bad input! Exiting..."
        logging.info("Bad input! Exiting...")
        run_again = False
    return run_again

##############################################################################



# Main function:
def main(kw):
    # For logging
    curr_timestamp = datetime.now().strftime("%d%B%Y_%I%M%S%p")
    log_file_name = 'AuScerLog_' + curr_timestamp + '.log'
    full_path = dbConfig.dict["logUrl"] +log_file_name
    #logging.basicConfig(filename=full_path, level=logging.INFO)

    # End user UI
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    logging.info("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print "~~~~~~~~~~~~~~~~~~~~~~~ ATLAS ~~~~~~~~~~~~~~~~~~~~~~~"
    logging.info("~~~~~~~~~~~~~~~~~~~~~~~ ATLAS ~~~~~~~~~~~~~~~~~~~~~~~")
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    logging.info("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    # Initializations
    run_again = True
    what_to_scrape = None

    # Main loop
    while run_again:
        integ_data_frame = pd.DataFrame({'siteCode': [' '],
                                         'pBrand': [' '],
                                         'pTitle': [' '],
                                         'pModel': [' '],
                                         'price': [' '],
                                         'pURL': [' '],
                                         'rUser': [' '],
                                         'rTitle': [' '],
                                         'rDate': [' '],
                                         'rText': [' '],
                                         'rURL': [' ']}, index=[0])


        what_to_scrape = 2


        # Product information and reviews (elif)
        if int(what_to_scrape) == 2:
            opt = 3


        if int(opt) == 3:  # Product information and reviews from both sites
            im_y_n = 'y'
            if im_y_n == 'y' or im_y_n == 'Y':

                # common_keywords_list = keywords_input()
                common_keywords_list = kw
                time.sleep(0.5)

                print "Scraping from both sites..."
                logging.info("Scraping from both sites...")

                print "Now scraping product information and reviews from HOMEDEPOT..."
                logging.info("Now scraping product information and reviews from HOMEDEPOT...")
                integ_data_frame = integ_data_frame.append(HomeDepot.home_depot_all_info(common_keywords_list))

                print "Now scraping product information and reviews from AMAZON (using Import.io)..."
                logging.info("Now scraping product information and reviews from AMAZON (using Import.io)...")
                integ_data_frame = integ_data_frame.append(Amazon_I1.amazon_i_all_info(common_keywords_list))

                final_data_frame1 = clean_integ_dataframe(integ_data_frame)

                # Saving the CSV file with product information and reviews; one CSV for each product/keyword
                curr_timestamp = datetime.now().strftime("%d%B%Y_%I%M%S%p")
                output_file_name = 'ATLAS_' + curr_timestamp + '.csv'
                full_path = dbConfig.dict["outputUrl"] + output_file_name
                final_data_frame1.to_csv(full_path, index=False, encoding='utf-8')
                print "CSV file for this product saved at location: " + full_path
                logging.info("CSV file for this product saved at location: " + full_path)

                run_again = False
    # 'while run_again' closes here

# ####################################################################################

