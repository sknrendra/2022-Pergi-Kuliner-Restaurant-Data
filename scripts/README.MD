# Introduction
2022-Pergi-Kuliner-Restaurant-Data is a project that aims to scrape pergikuliner.com, a food discovery app based in Indonesia. The main objective was to obtain data of 1500 restaurants from the website, from their name, phone number, available facilities and ratings. To get around the JavaScript-injected HTML and achieve optimum scraping performance, the author decided to utilize Selenium with multithreading.

This repo includes copies of the following in separate top-level directories:
 - The output of the script (The dataset) which is placed on the 'data' folder.
 - The Selenium script used for the scraping job is placed on the 'script' folder. There are singlethreaded and multithreaded version of the script. The multithreaded script is named "pergikuliner_scraper_multithreaded.py" while the singlethreaded script is named "pergikuliner_scraper_singlethreaded.py"

