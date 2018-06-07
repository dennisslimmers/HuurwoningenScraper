import sys, os

class config:
    """Configuration class

       Used to determine the different variables for the 
       Huurwoningen scraping process, for example the minimal hiring price.
    """

    min_price = 0
    max_price = 800
    location = "leiden" # Leiden (Netherlands) as it's default
    watch_mode = False
    app_version = 0.1
    app_name = "Huurwoningen Web Scraper"

    def __init__(self, argv):
        if len(argv) > 0:
            self.parse_arguments(argv)


    def parse_arguments(self, argv):
        """Parse the provided arguments to the config values"""
        
        for i in range(0, len(argv)):
            if i <= 0:
                continue # The first argument is always the execution file, so skip it 
            else:
                arg = argv[i]
                if arg.startswith("-"):
                    # First, let's check if the provided argument is a general argument (-h & -v)
                    self.map_general_argument(arg)

                    # Then we check if the argument is provided to change the scrapers functionality (-min, -max, , -l, -w)
                    self.map_argument(arg, argv, i)


    def is_valid_argument(self, arg):
        """Checks if the given argument is a valid argument"""

        valid_args = ["-min", "-max", "-w", "-h", "-v", "-l"]

        if arg not in valid_args:
            return False
        else:
            return True


    def map_general_argument(self, arg):
        if arg == "-h":
            print(self.app_name + " v" + str(self.app_version))
            exit()
        elif arg == "-v":
            print(self.app_name + " v" + str(self.app_version))
            exit()


    def map_argument(self, arg, argv, index):
        """Map the provided argument to the existing config variable"""

        if arg == "-w":
            self.watch_mode = True
        elif arg == "-min":
            try:
                min = int(argv[index + 1])
            except:
                e = sys.exc_info()[0]
                print(e)
                exit()
            
            self.min_price = min
        elif arg == "-max":
            try:
                max = int(argv[index + 1])
            except:
                e = sys.exc_info()[0]
                print(e)
                exit()
            
            self.max_price = max
        elif arg == "-l":
            try:
                location = str(argv[index + 1])
            except:
                e = sys.exc_info()[0]
                print(e)
                exit()
            
            self.location = location


    def get_huurwoningen_url(self, config):
        """Returns the correct Huurwoningen.nl url based on the configuration values"""

        return "https://www.huurwoningen.nl/in/" + self.location + "/?min_price=" + str(self.min_price) + "&max_price=" + str(self.max_price)