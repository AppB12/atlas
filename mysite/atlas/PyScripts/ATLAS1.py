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
status_code = 500

# ############################################################################


# To remove empty rows created while integrating dataframes
def clean_integ_dataframe(final_df):
    final_df1 = final_df[final_df.pURL != " "]
    final_df1 = final_df1.dropna(axis='columns', how='all')
    return final_df1

# ############################################################################


# Main function:
def main(kw_str):
    global integ_data_frame
    
    # For logging
    curr_timestamp = datetime.now().strftime("%d%B%Y_%I%M%S%p")
    log_file_name = 'ATLASLog_' + curr_timestamp + '.log'
    full_path = dbConfig.dict["logUrl"] +log_file_name
    #logging.basicConfig(filename=full_path, level=logging.INFO)

    # End user UI
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    logging.info("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print "~~~~~~~~~~~~~~~~~~~~~~~ ATLAS ~~~~~~~~~~~~~~~~~~~~~~~"
    logging.info("~~~~~~~~~~~~~~~~~~~~~~~ ATLAS ~~~~~~~~~~~~~~~~~~~~~~~")
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    logging.info("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    integ_data_frame = pd.DataFrame({'siteCode': [' '],
                                     'pCategory': [' '],
                                     'pBrand': [' '],
                                     'pTitle': [' '],
                                     'pModel': [' '],
                                     'price': [' '],
                                     'pURL': [' '],
                                     'rUser': [' '],
                                     'rTitle': [' '],
                                     'rDate': [' '],
                                     'rRating': [' '],
                                     'rText': [' '],
                                     'rURL': [' ']}, index=[0])

    time.sleep(0.5)

    print "Scraping from both sites..."
    logging.info("Scraping from both sites...")

    print "Now scraping product information and reviews from HOMEDEPOT..."
    logging.info("Now scraping product information and reviews from HOMEDEPOT...")
    returned_list_HD = HomeDepot.home_depot_all_info(kw_str)

    integ_data_frame = integ_data_frame.append(returned_list_HD[0])
    status_code = returned_list_HD[1]

    print "Status Code for HomeDepot: " + str(returned_list_HD[1])
    
    print "Now scraping product information and reviews from AMAZON (using Import.io)..."
    logging.info("Now scraping product information and reviews from AMAZON (using Import.io)...")
    returned_list_AM = Amazon_I1.amazon_i_all_info(kw_str)

    integ_data_frame = integ_data_frame.append(returned_list_AM[0])
    
    if status_code == returned_list_AM[1]:
        status_code = returned_list_AM[1]
    else:
        status_code = 500

    print "Status Code for Amazon: " + str(returned_list_AM[1])

    final_data_frame1 = clean_integ_dataframe(integ_data_frame)


    # Saving the CSV file with product information and reviews; one CSV for each product/keyword
    curr_timestamp = datetime.now().strftime("%d%B%Y_%I%M%S%p")
    output_file_name = kw_str + '_ATLAS_' + curr_timestamp + '.csv'
    full_path = dbConfig.dict["outputPath"] + output_file_name
    final_data_frame1.to_csv(full_path, index=False, encoding='utf-8')
    print "CSV file for this product saved at location: " + full_path
    logging.info("CSV file for this product saved at location: " + full_path)

    print(final_data_frame1)
    with open(dbConfig.dict["outputUrl"], 'a') as f:
        final_data_frame1.to_csv(f, header=False, index=False, encoding='utf-8')
    f.close()
    return status_code

# ####################################################################################

