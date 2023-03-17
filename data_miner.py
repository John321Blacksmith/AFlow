"""
This module contains the scraping functionality.
"""
from bs4 import BeautifulSoup as Bs


class DataFetcher:
   def __init__(self, responses, item, site_dict: dict):
      self.responses = responses
      self.site_dict = site_dict
      self.item = item
      self.data_fields = site_dict[self.item]['fields']

   @staticmethod
   def get_pages_amount(response, item, site_dict: dict) -> int:
      """
      This method goes to the first page of the category, finds a total
      amount of objects, counts an amount of ones which are gotten per one 
      page and returns a calculated pages amount.
      """

      # derive a soup object
      soup = Bs(response, 'html.parser')
      
      # find objects of the single start page
      objects = soup.find_all(site_dict[item]['object']['tag'],
                              site_dict[item]['object']['class'])

      # define a number of objects per page
      objs_per_page = len(objects)

      # define a total amount of objects

      # if the amount data is represented as an object, it'll be treated as a dict
      if isinstance(site_dict[item]['generic_quantity'], dict):
         if 'inlined_tag' in site_dict[item]['generic_quantity'].keys():
            inlined_tag = site_dict[item]['generic_quantity']['inlined_tag']
            total_objs_amount = soup.find(site_dict[item]['generic_quantity']['tag'],
                                          site_dict[item]['generic_quantity']['class']).__getattr__(inlined_tag).text
         else:
            total_objs_amount = soup.find(site_dict[item]['generic_quantity']['tag'],
                                          site_dict[item]['generic_quantity']['class']).text
         
      # if as a string or smth else:
      else:
         total_objs_amount = site_dict[item]['generic_quantity']

      # convert to integer
      total_objs_amount = DataFetcher.refine_string(total_objs_amount)

      if objs_per_page != 0:
         # find how many full pages there will be
         full_pages_amount = total_objs_amount // objs_per_page

         # check if there are exessive objects
         if full_pages_amount < (total_objs_amount / objs_per_page):
            full_pages_amount += 1

         return full_pages_amount
      else:
         return 0


   def structure_data(self, content) -> list:
      """
      This method receives unstructured content of
      each page and returns the structured ones.
      """
      list_of_objects = []
   
      # go through the lists of each data and make sure if all
      # the four ones are of equal length, otherwise, find one with
      # the smallest value and count upon it in order to avoid the
      # error: IndexError: List index out of range.
      
      # here we define a number via that the iteration should go
      quantities = []
      content_keys = [key for key in content.keys()]
      for key in content_keys:
         n = len(content[key])
         if n != 0:
            quantities.append(n)
      
      # if the content is available, the next stage begins
      # othervise, the method'll return a None object instead of the list
      try:
         actual_number = DataFetcher.find_smallest_val(quantities)

         # if the data is needed to be saved, the data fields of the object are applied 
         for i in range(0, actual_number):
            obj = {
               self.data_fields[0]: content['titles'][i],
               self.data_fields[1]: content['integers'][i],
               self.data_fields[2]: content['links'][i],
               self.data_fields[3]: content['images'][i]
            }
   
            list_of_objects.append(obj)

      except IndexError:
         return None

      else:
         return list_of_objects

   @staticmethod
   def inspect_signs(sign: str, seq: str, sign_num: int) -> int:
      count = 0
      for i in range(0, len(seq)):
         if seq[i] == sign:
            count += 1
            if count == sign_num:
               return i
            else:
               continue

   @staticmethod
   def refine_string(pr_string):
      data = ''
      for letter in list(pr_string):
         if letter.isdigit():
            data += letter
      else:
         data = int(data)

      return data

   @staticmethod
   def retrieve_objects(soup, item, content_dict, site_dict: dict):
      """
      This method gets objects from the page with use of the site_dict.
      It then extracts the data from each of them and places in the content
      """
      source = site_dict[item]['source']
      objects = soup.find_all(site_dict[item]['object']['tag'],
                              site_dict[item]['object']['class'])

      # strolling through the derived list and extraction of each key data from every list object
      for i in range(0, len(objects)):
         # derive a title
         # if any object is in the list of componets every api item has, the extraction of HTML data will be performed
         if 'titles' in site_dict[item]['obj_components']:
            # if there is no a 'class' key in the 'title' object of the api item, a 'tag' key will be used only
            if 'class' not in site_dict[item]['title'].keys():
               if 'attribute' in site_dict[item]['title'].keys():
                  titles_house = objects[i].find_all(site_dict[item]['title']['tag'])
                  for t in titles_house:
                     t_attrs = t.attrs
                     for attr in t_attrs.keys():
                        if attr == site_dict[item]['title']['attribute']:
                           if t[attr] == site_dict[item]['title']['attr_value']:
                              title = t
               else:
                  title = objects[i].find(site_dict[item]['title']['tag'])

            else:
               title = objects[i].find(site_dict[item]['title']['tag'],
                                site_dict[item]['title']['class'])

            # here we have an entity of one of the four types of web page content
            if title != None:
               # if this entity is not None, it'll be sent to its family
               content_dict['titles'].append(title.text)
            else:
               content_dict['titles'].append('No data')

         # derive some integers
         if 'integers' in site_dict[item]['obj_components']:
            # if there is an order pattern in the html class-attribute, 
            # an order number is defined for each of the attribute values and inserted to the pattern
            if 'iterable' in site_dict[item]['integer'].keys():
               if site_dict[item]['integer']['iterable']:
                  # define an order number
                  num = i + 1
                  numbers = objects[i].find(site_dict[item]['integer']['tag'],
                                 site_dict[item]['integer']['class'].format(num))
            else:  
               numbers = objects[i].find(site_dict[item]['integer']['tag'],
                                  site_dict[item]['integer']['class'])

            if numbers != None:
               content_dict['integers'].append(numbers.text)
            else:
               content_dict['integers'].append('No data')

         # derive a link
         if 'links' in site_dict[item]['obj_components']:
            if 'class' in site_dict[item]['link'].keys():
               link_element = objects[i].find(site_dict[item]['link']['tag'],
                                       site_dict[item]['link']['class'])
            else:
               link_element = objects[i].find(site_dict[item]['link']['tag'])

            # if the link entity is None, the current list object itself will be used, assuming it has the 'href' attribute
            if link_element == None:
               snippet = objects[i]['href']
            # if everything is fine, the href data will be extracted from one of the elements of the list object
            else:
               snippet = link_element['href']

            # check if the link entity is comprehensive or not
            # if so, nothing changes
            if snippet.startswith('https://'):
               link = snippet
            # if it is not, a root link is cut off from the main source of the item
            else:
               # fetching an end point of the sliced string
               third_slash = DataFetcher.inspect_signs('/', source, 3)
               # then the main source string slice, an additional slash and the uncomplete href are substracted
               link = source[:third_slash] + '/' + snippet[1:]
            
            content_dict['links'].append(link)

         # derive all the images in the product model
         if 'images' in site_dict[item]['obj_components']:
            # here we find all the images inlined in the list object
            if 'class' in site_dict[item]['image']:
               images_house = objects[i].find_all(site_dict[item]['image']['tag'], site_dict[item]['image']['class'])
            else:
               images_house = objects[i].find_all(site_dict[item]['image']['tag'])

            # create a collection of images referred to the object
            img_collection = []

            # specify how many images to load
            if 'quantity' in site_dict[item]['image']:
               img_amount = site_dict[item]['image']['quantity']
            else:
               img_amount = None

            # iterate through these images to inspect then all the attributes of each one
            for i in images_house[:img_amount]:
               attrs = i.attrs
               # go through the attributes of each image
               for attr in attrs.keys():
                  # check if the current attribute is equal to the one required in the item api
                  if attr == site_dict[item]['image']['attribute']:
                     # if so, the attribute is checked if it has a comprehensive link
                     if i[attr].startswith('https://'):
                        image_link = i[attr]
                     else:
                        if i[attr].startswith('//'):
                           first_slash = DataFetcher.inspect_signs('/',
                              source, 1)
                           image_link = source[:first_slash] + '/' + i[attr][1:]
                        else:
                           third_slash = DataFetcher.inspect_signs('/',
                              source, 3)
                           image_link = source[:third_slash] + '/' + i[attr][1:]

                     img_collection.append(image_link)

            # append this entity to the images family
            content_dict['images'].append(img_collection)

   def fetch_content(self) -> dict:
      """
      This method does iteration through the taken
      tasks and extracts required data from each of them.
      It gathers unstructured content in to the four dict keys.
      """
      content = {
         'titles': [],
         'integers': [],
         'links': [],
         'images': []
      }
      # iterate through each task and get a soup
      for response in self.responses:
         soup = Bs(response, 'html.parser')
         DataFetcher.retrieve_objects(soup, self.item, content, self.site_dict)

      return content

   @staticmethod
   def find_smallest_val(seq) -> int:
      smallest_value = seq[0]

      for i in range(0, len(seq)):
         if seq[i] <= smallest_value:
            smallest_value = seq[i]
   
      return smallest_value