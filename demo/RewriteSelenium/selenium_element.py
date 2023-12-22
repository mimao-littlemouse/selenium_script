class Selenium_Element:
    mask_id = ''

    def __init__(self,mask_id) -> None:
        self.mask_id = mask_id
    
    def __str__(self) -> str:
        return self.mask_id