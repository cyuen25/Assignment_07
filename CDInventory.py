#--------------------------------------------------------------------------#
# Title: Assignment07.py
# Desc: Working with classes and functions. Also modifiy someone else's code
# Change Log: (Who, When, What)
# Cyuen, 2020-Mar-01, Created File by Making a Copy of last week's Assignment
# Cyuen, 2020-Mar-08, Modified File - Made changes based on feedback from Douglas
# Cyuen, 2020-Mar-08, Modified File - Added error handling for "add cd" and "del cd"
#--------------------------------------------------------------------------#

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.txt'  # data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    
    @staticmethod
    def  add_cd(intID, strTitle, strArtist, table):
        """This allows for user to enter a new CD
        
        Args:
            table(list of dict): 2D data structure (list of dicts) that holds the data during runtime.
            
        Return:
            None
        """
        dicRow = {'ID': int(intID), 'Title': strTitle, 'Artist': strArtist}
        lstTbl.append(dicRow)
    
    
    @staticmethod
    def delete_data(intID, table):    
        """Function is to manage the deletion of the data if the user decides to choose which ID
    
        Args:
            None
        
        Retuns:
            None
        """ 
        intRowNr = -1
        blnCDRemoved = False
        for row in lstTbl:
            intRowNr += 1
            if row['ID'] == intID:
                del lstTbl[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')


class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        try:
            objFile = open(file_name, 'r')
            table.clear()  # this clears existing data and allows to load data from file
            for line in objFile:    
                data = line.strip().split(',')
                dicRow = {'ID': int(data[0]), 'Title': data[1], 'Artist': data[2]}
                table.append(dicRow)
            objFile.close()
        except FileNotFoundError:
            print("The file {} could not be loaded".format(file_name))
                    
    @staticmethod
    def write_file(file_name, table):
        """Function to save data into a text file 
       
        Args: 
            FileName : name of the file used to save the data into
            
        Returns:        
            None.
        """
        
        objFile = open(file_name, 'w')
        for row in table:
            lstValues = list(row.values())
            lstValues[0] = str(lstValues[0])
            objFile.write(','.join(lstValues) + '\n')
        objFile.close() 
      
# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')


    @staticmethod
    # Renamed since in IO we're not adding a CD but generating it's data
    # def add_cd(table):
    def get_new_cd_data():
        """This allows for user to enter a new CD
        
        Args:
            table(list of dict): 2D data structure (list of dicts) that holds the data during runtime.
            
        Return:
            None
        """
        intID = int(input('Enter ID: '))
        strTitle = input('What is the CD\'s title? ').strip()
        strArtist = input('What is the Artist\'s name? ').strip()

        # We return to the caller the three pieces of data just generated.
        return intID, strTitle, strArtist
    
# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()
    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled: ')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        try:
            strID, strTitle, strArtist = IO.get_new_cd_data()
            DataProcessor.add_cd(strID, strTitle, strArtist, lstTbl)
            IO.show_inventory(lstTbl)
        except Exception as e:
            print('\n',e)
            print() # add fro extra space between lines
        continue  # start loop back at top.          
    # 3.4 process display current inventory
    
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top. 
    
        # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        try:
            IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
            intID = int(input('Which ID would you like to delete? ').strip())
        # 3.5.2 search thru table and delete CD
            DataProcessor.delete_data(intID, lstTbl)
            IO.show_inventory(lstTbl)
        except Exception as e:
            print('\n', e)
            print() #add for extra space between lines
        continue  # start loop back at top.
          # 3.6 process save inventory to file
    
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




