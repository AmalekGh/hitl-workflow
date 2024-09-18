import ipywidgets as widgets
from IPython.display import display, clear_output


class DynamicCheckboxList:
    def __init__(self):
        self.options = ['Title', 'Theme', 'Keywords', 'Evaluation Approach']
        
        self.checkbox_container = widgets.VBox()
        self.create_checkboxes()
        
        self.text_field = widgets.Text(placeholder="Enter a new option")
        
        self.add_button = widgets.Button(description="Add Option")
        self.add_button.on_click(self.add_option)
        
        self.delete_button = widgets.Button(description="Delete Selected Options")
        self.delete_button.on_click(self.delete_selected_options)

    def create_checkboxes(self):
        self.checkbox_container.children = [widgets.Checkbox(value=False, description=option) for option in self.options]
    
    def get_selected_options(self):
        return [cb.description for cb in self.checkbox_container.children if cb.value]
    
    def add_option(self, _):
        new_option = self.text_field.value
        if new_option and new_option not in self.options:
            self.options.append(new_option)
            self.create_checkboxes()
        self.text_field.value = ''
    
    def delete_selected_options(self, _):
        selected_options = self.get_selected_options()
        for option in selected_options:
            self.options.remove(option)
        self.create_checkboxes()
    
    def display_interface(self):
        display(self.text_field, self.add_button, self.delete_button, self.checkbox_container)
    
class DocumentLimitSlider:
    def __init__(self):
        self.input_slider = widgets.IntSlider(
            value=10,
            min=1,    
            max=100,
            step=1,  
            description='Documents Limit:',
            disabled=False,
            layout=widgets.Layout(width='400px'), 
            style={'description_width': '150px'}   
        )

        self.input_slider.observe(self.save_input, names='value')

        self.limit = self.input_slider.value

    def save_input(self, change):
        self.limit = change['new']
        print(f"Selected limit: {self.limit}")

    def get_current_value(self):
        return self.limit

    def display_slider(self):
        display(self.input_slider)
        return self.get_current_value
    
class DynamicSourceList:
    def __init__(self):
        self.options = ['Arxiv', 'Semantic Scholar']
        
        self.checkbox_container = widgets.VBox()
        self.create_checkboxes()
        
        self.text_field = widgets.Text(placeholder="Enter a new option")
        
        self.add_button = widgets.Button(description="Add Option")
        self.add_button.on_click(self.add_option)
        
        self.delete_button = widgets.Button(description="Delete Selected Options")
        self.delete_button.on_click(self.delete_selected_options)

    def create_checkboxes(self):
        self.checkbox_container.children = [widgets.Checkbox(value=False, description=option) for option in self.options]
    
    def get_selected_options(self):
        return [cb.description for cb in self.checkbox_container.children if cb.value]
    
    def add_option(self, _):
        new_option = self.text_field.value
        if new_option and new_option not in self.options:
            self.options.append(new_option)
            self.create_checkboxes()
        self.text_field.value = ''
    
    def delete_selected_options(self, _):
        selected_options = self.get_selected_options()
        for option in selected_options:
            self.options.remove(option)
        self.create_checkboxes()
    
    def display_interface(self):
        display(self.text_field, self.add_button, self.delete_button, self.checkbox_container)