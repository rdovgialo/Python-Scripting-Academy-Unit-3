import argparse
from datetime import date, timedelta
from random import randint
import os
import urllib.request

def parse_command_line():
    """
    Parse the command line arguments and return the argparse object.

    args:
        None

    returns:
        args: generated argparse object with all the parsed command line arguments
    """

    #TODO: Your code goes here
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--date', metavar=('month', 'day', 'year'), nargs = 3, type=int, default = [], help='formatted date (i.e. 03 28 1998)')
    parser.add_argument('-s','--surprise', action='store_true', help='select a random date for a surprise image')
    parser.add_argument('-k','--api_key', metavar='API_KEY', default = '', nargs =1, help="NASA developer key")
    parser.add_argument('-v','--verbose', action='store_true', help='verbose mode')

    args = parser.parse_args()
    return args

def create_date(datelist, surprise):
    """
    Creates a valid date object.

    args:
        d: list containing the [month, day, year] or an empty list []
        surprise: Boolean, if True and datelist is empty, generate a random date
                  the earliest valid date is June 16 1995

    returns:
        created valid date object or None when date selected by user is invalid (i.e. in the future)
    """

    #TODO: Your code goes here
    if len(datelist) != 0:
        gdate = date(int(datelist[2]), int(datelist[0]), int(datelist[1]))
        return gdate

    elif len(datelist) ==0 and surprise:
        try:
            while True:
                try:
                    gdate = date(randint(1995, 2019), randint(1, 12), randint(1, 31))
                    if gdate > date(1995, 6, 16) and gdate < date.today():
                        break
                except ValueError:
                    gdate = date(randint(1995, 2019), randint(1, 12), randint(1, 30))
                    if gdate > date(1995, 6, 16) and gdate < date.today():
                        break
            return gdate
        except:
            return None
    elif len(datelist) ==0 and surprise == False:
        try:
            gdate = date.today() - timedelta(days=1)
            return gdate
        except:
            return None


def query_url(d, api_key):
    """
    Creates a URL to fetch an image metadata.

    args:
        d: date object containing a valid date
        api_key: string containing "DEMO_KEY" or your valid NASA developer key for higher request rate limits

    returns:
        complete url as a string

    """
    return "https://api.nasa.gov/planetary/apod?api_key={}&date={}-{}-{}".format(api_key, d.strftime('%Y'), d.strftime('%m'), d.strftime('%d'))



def save_image(d, image):
    """
    Save binary image on disk.

    Use the date of the image (d) to create a directory structure (year/month) if it doesn't exist already,
    then save the binary image under its corresponding year and month using the date (d) + '.jpg' as a file name

    HINT: Binary data can be written to files in a similar way to how strings are written to files.
          Use 'wb' (write binary) instead of 'w' in the file open clause (i.e. open(file_path, 'wb'))

    args:
        d: date object containing image date
        image: binary image itself

    returns:
        file_path: where the image was saved

    examples:
        if d = 2017-8-21, the image will be saved as: 2017/8/2017-8-21.jpg
        if d = 1998-4-15, the image will be saved as: 1998/4/1998-4-15.jpg
    """
    if os.path.isdir("{}/{}".format(os.getcwd(), str(d.year))):
        if os.path.isdir("{}/{}/{}".format(os.getcwd(), str(d.year), str(d.month))):
            nasa_image = open("{}/{}/{}/{}.jpg".format(os.getcwd(), str(d.year), str(d.month), d), 'wb')
            nasa_image.write(image)
            nasa_image.close()
        else:
            os.mkdir("{}/{}/{}".format(os.getcwd(), str(d.year), str(d.month)))
            nasa_image = open("{}/{}/{}/{}.jpg".format(os.getcwd(), str(d.year), str(d.month), d), 'wb')
            nasa_image.write(image)
            nasa_image.close()
    else:
        os.mkdir("{}/{}".format(os.getcwd(), str(d.year)))
        os.mkdir("{}/{}/{}".format(os.getcwd(), str(d.year), str(d.month)))
        nasa_image = open("{}/{}/{}/{}.jpg".format(os.getcwd(), str(d.year), str(d.month), d), 'wb')
        nasa_image.write(image)
        nasa_image.close()

    return "{}/{}/{}/{}.jpg".format(os.getcwd(), str(d.year), str(d.month), d)



def request(url):
    """
    Download the metadata located at url and return it as a dictionary.

    args:
        url: to request image metadata for a specific date

    returns:
        dictionary of the metadata downloaded from url

    examples:
        if url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date=2017-09-24"
        url_request(url) ==> returns dictionary:

        {
          "copyright": "The League of Lost Causes",
          "date": "2017-09-24",
          "explanation": "What is that light in the sky? Perhaps one of humanity's more common questions, an answer may result from a few quick observations.  For example -- is it moving or blinking? If so, and if you live near a city, the answer is typically an airplane, since planes are so numerous and so few stars and satellites are bright enough to be seen over the din of artificial city lights. If not, and if you live far from a city, that bright light is likely a planet such as Venus or Mars -- the former of which is constrained to appear near the horizon just before dawn or after dusk.  Sometimes the low apparent motion of a distant airplane near the horizon makes it hard to tell from a bright planet, but even this can usually be discerned by the plane's motion over a few minutes. Still unsure?   The featured chart gives a sometimes-humorous but mostly-accurate assessment.  Dedicated sky enthusiasts will likely note -- and are encouraged to provide -- polite corrections.   Chart translations: Spanish, Italian, Polish, Tamil, Kannada, Latvian, and Norwegian",
          "hdurl": "https://apod.nasa.gov/apod/image/1709/astronomy101_hk_750.jpg",
          "media_type": "image",
          "service_version": "v1",
          "title": "How to Identify that Light in the Sky",
          "url": "https://apod.nasa.gov/apod/image/1709/astronomy101_hk_960.jpg"
        }

    """

    # request the content of url and save the retrieved binary data
    with urllib.request.urlopen(url) as response:
        data = response.read()

    # convert data from byte to string
    data = data.decode('UTF-8')

    # convert data from string to dictionary
    data = eval(data)
    return data

def download_image(url):
    """
    Download the image located at url.

    args:
        url: where actual image is located

    returns:
        image as binary data
    """

    # request the content of url and return the retrieved binary image data
    with urllib.request.urlopen(url) as response:
        image = response.read()
    return image

def main():
    print("declaring API key ")
    # NASA developer key (You can hardcode yours for higher request rate limits!)
    API_KEY = "cZX0zRDveiz7AfGfOW23typMH3NCnS3uvQJc0ZNS"
    print("print parsing argument")
    # parse command line arguments
    args = parse_command_line()

    # update API_KEY if passed on the command line
    print("Update API key if provided")
    print(args.api_key)
    if args.api_key != '':
        API_KEY = args.api_key

    # create a request date
    print("beggin generating date")
    d = create_date(args.date, args.surprise)

    print('date generated {}'.format(d))
    # ascertain a valid date was created, otherwise exit program
    if d is None:
        print("No valid date selected!")
        exit()

    # verbose mode
    if args.verbose:
        print("Image date: {}".format(d.strftime("%b %d, %Y")))

    # generate query url
    url = query_url(d, API_KEY)

    # verbose mode
    if args.verbose:
        print("Query URL: {}".format(url))

    # download the image metadata as a Python dictionary
    metadata = request(url)

    # verbose mode
    if args.verbose:
        # display image title, other metadata can be shown here
        print("Image title: {}".format(metadata['title']))

    # get the url of the image data from the dictionary
    image_url = metadata['url']

    # verbose mode
    if args.verbose:
        print("Downloading image from:", image_url)

    # download the image itself (the returned info is binary)
    image = download_image(image_url)

    # save the downloaded image into disk in (year/month)
    # the year and month directories correspond to the date of the image (d)
    # the file name is the date (d) + '.jpg'
    save_image(d, image)

    print("Image saved")

if __name__ == '__main__':
    main()
