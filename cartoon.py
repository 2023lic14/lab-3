# missing import statements should be added here
import wikipedia
import images
import cv2
from images import get_wikipedia_page_thumbnail_url, download_image_from_url
import os


def prompt_for_image():
    """
    Prompts the user for the name of a Wikipedia page and obtains the URL of the thumbnail image of the page.
    
    return url, page_name: str, str
    """
    search_query = input("Enter name of a personality: ")
    try:
        topThree = wikipedia.search(search_query, 3)
        selection = input(
            f"Select a name from the following list: \n 1. {topThree[0]} \n 2. {topThree[1]} \n 3. {topThree[2]}\nEnter the number of the desired name: ")
        url = ""
        save_name = ""
        if selection == "1":
            url = images.get_wikipedia_page_thumbnail_url(topThree[0])
            save_name = topThree[0]
        elif selection == "2":
            url = images.get_wikipedia_page_thumbnail_url(topThree[1])
            save_name = topThree[1]
        elif selection == "3":
            url = images.get_wikipedia_page_thumbnail_url(topThree[2])
            save_name = topThree[2]
        else:
            print("Not a valid selection. Try again")
            return None, None
        download_image_from_url(url, save_name)
        print(f"Cartoon image of {save_name} saved as {save_name}.jpeg")
        return url, save_name
    except Exception as e:
        print(f"Error: Unable to find image for the given name: {e}")
        return None, None


def convert_image_to_cartoon(image_path):
    """
    Converts an image to a cartoon given the image_path.
    """
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    color = cv2.bilateralFilter(img, 9, 200, 200)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    cv2.imwrite(image_path, cartoon)


if __name__ == "__main__":
    prompt_for_image()
    image_path = input("Enter the path to the image to convert: ")
    convert_image_to_cartoon(image_path)
