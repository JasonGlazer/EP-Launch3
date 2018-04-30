import wx


class FileNameMenus(object):

    def __init__(self, menu, start_separator_id, end_separator_id):
        self.menu = menu
        self.start_separator_id = start_separator_id
        self.end_separator_id = end_separator_id
        self.menu_items_for_files = []

    def delete_file_list(self):
        menu_list = self.menu.GetMenuItems()
        mode = False
        for menu_item in menu_list:
            if menu_item.GetId() == self.end_separator_id:
                mode = False
            if mode:
                self.menu.Remove(menu_item)
            if menu_item.GetId() == self.start_separator_id:
                mode = True

    def get_file_list(self):
        list_of_menu_item_labels = []
        menu_list = self.menu.GetMenuItems()
        mode = False
        for menu_item in menu_list:
            if menu_item.GetId() == self.end_separator_id:
                mode = False
            if mode:
                list_of_menu_item_labels.append(menu_item.GetLabel())
            if menu_item.GetId() == self.start_separator_id:
                mode = True
        return list_of_menu_item_labels

    def add_file_name_list(self, list_of_file_names):
        self.delete_file_list()
        menu_list = self.menu.GetMenuItems()
        mode = False
        for position, menu_item in enumerate(menu_list):
            if mode:
                for file_count, file_name in enumerate(list_of_file_names):
                    # add the file name and derive a ID number based on the count and the first separator ID
                    new_menu_item = self.menu.Insert(position + file_count, self.start_separator_id * 20 + file_count,
                                                     file_name, kind=wx.ITEM_RADIO)
                    #new_menu_item.Check(True)
                    self.menu_items_for_files.append(new_menu_item)
                    self.menu.Bind(wx.EVT_MENU, self.handle_menu_selection, new_menu_item)
                break
            if menu_item.GetId() == self.start_separator_id:
                mode = True

    def handle_menu_selection(self, event):
        current_menu_item = self.menu.FindItemById(event.GetId())
        print('clicked menu item:', current_menu_item.GetLabel(), current_menu_item.GetId())




