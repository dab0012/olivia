# Add the olivea_finder directory to the path
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List
from bs4 import BeautifulSoup
from olivia_finder.scrape.requests.request_handler import RequestHandler
from olivia_finder.scrape.requests.proxy_builder import GeonodeProxy
from olivia_finder.scrape.requests.proxy_handler import ProxyHandler
from olivia_finder.scrape.requests.useragent_handler import UserAgentHandler


# Get the list of fist level directories
def get_directories(url, rh: RequestHandler) -> List[str]:
    '''
    Get the list of first level directories

    Returns
    -------
    List[str]
        List of first level directories
    '''

    # Get the response
    response = rh.do_request(url)[1]

    # Parse the response
    soup = BeautifulSoup(response.text, 'html.parser')
    first_level_directories = [a['href'] for a in soup.find_all('a') if a['href'][-1] == '/']

    # Remove the parent directory
    first_level_directories.remove('../')

    return first_level_directories

def search_for_maven_metadata(url, rh: RequestHandler) -> List[str]:
    '''
    Search for maven-metadata.xml 

    Extract the fields: groupId, artifactId, version

    Returns
    -------
    List[str]
        List of dictionaries with the fields: groupId, artifactId, version
    '''

    try:

        # Get the response
        response = rh.do_request(url)[1]

        # Parse the response as xml
        soup = BeautifulSoup(response.text, 'lxml')

        # Get the data from the xml
        groupId = soup.find('groupid').text
        artifactId = soup.find('artifactid').text
        versions = soup.find_all('version')
        # get the latest version
        version = versions[-1].text
    
        return {'groupId': groupId, 'artifactId': artifactId, 'version': version}
    
    except:
        return None
    


def search_recursive(url, rh: RequestHandler) -> List[str]:
    '''
    Search recursively for maven-metadata.xml in all directories

    Returns
    -------
    List[str]
        List of dictionaries with the fields: groupId, artifactId, version
    '''

    scraped_metadata = []

    # Get the list of first level directories
    first_level_directories = get_directories(url, rh)

    # Search for maven-metadata.xml in all directories
    for directory in first_level_directories:

        # Search for maven-metadata.xml in the current directory
        target = url + directory + 'maven-metadata.xml'
        metadata = search_for_maven_metadata(target, rh)

        if metadata:
            scraped_metadata.append(metadata)
            print("found: " + target)
            print(metadata)


        # Search recursively in the current directory
        print("recursive searching in: " + url + directory)
        search_recursive(url + directory, rh)

# mvn_central_url = 'https://repo.maven.apache.org/maven2'

# print(get_first_level_directories(mvn_central_url, rh))

# Define the request handler
ph = ProxyHandler(GeonodeProxy())
uh = UserAgentHandler()
rh = RequestHandler(ph, uh)

# Search for maven-metadata.xml in all directories
search_recursive('https://repo.maven.apache.org/maven2/', rh)