def get_icon(partner):
    folderIcons = 'icons/'
    icon_name = partner.lower()
    ext = '.png'
    
    partner_list = ['tokopedia', 'shopee'] # add partner name (add icon in icons folder with partner name)
    
    return ''.join([folderIcons,icon_name,ext]) if icon_name in partner_list else 'icon.png'